import copy
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from rsi.core import Service,Store,Problem,initial,retrieve,validate_backup,structural_score
from rsi.server import make_handler

class FakeProvider:
    key='test-only';model='fixture'
    def __init__(self): self.requests=[];self.fail=False
    def generate(self,system,payload):
        self.requests.append((system,payload))
        if self.fail: raise Problem('Falha simulada',502)
        if 'current' in payload:
            return {'name':'Mais claro','prompt':'Explicite as lacunas e os próximos passos.','rationale':'Melhoria proposta com base no feedback.'},{'tokens':20,'cost':0,'model':self.model,'seconds':0}
        return {'title':'Entrega de teste','answer':'Organize as informações fornecidas, prepare o rascunho e revise o resultado antes de compartilhar. Não há preço confirmado.','assumptions':['Preço não fornecido.'],'actions':['Conferir escopo','Confirmar dados'],'sources':[m['id'] for m in payload['context']]},{'tokens':20,'cost':0,'model':self.model,'seconds':0}

class CoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.provider=FakeProvider();self.store=Store(Path(self.tmp.name)/'db.sqlite3');self.svc=Service(self.store,self.provider)
    def tearDown(self): self.tmp.cleanup()
    def action(self,a,**d): return self.svc.action(a,d)['result']
    def test_task_persists_and_profile_isolated(self):
        t=self.action('task.add',title='Proposta',due='2026-10-01');self.action('task.toggle',id=t['id'])
        self.assertEqual(Service(Store(self.store.path),self.provider).state()['tasks'][0]['status'],'done')
        self.action('profile',profile='empresa');self.assertEqual(self.svc.state()['tasks'][0]['profile'],'pessoal')
    def test_invalid_inputs_do_not_mutate(self):
        for action,d in [('task.add',{'title':'','due':''}),('task.add',{'title':'A','due':'amanhã'}),('profile',{'profile':'x'}),('run',{'prompt':1})]:
            with self.assertRaises(Problem): self.svc.action(action,d)
        self.assertFalse(self.store.read()['tasks']);self.assertFalse(self.provider.requests)
    def test_memory_scoping_and_sources(self):
        self.action('memory.add',title='Proposta pessoal',body='Revisar a proposta.')
        self.action('profile',profile='empresa')
        mem=self.action('memory.add',title='Proposta empresa',body='Proposta com duas revisões.')
        run=self.action('run',prompt='Faça uma proposta')
        self.assertEqual(run['output']['sources'],[mem['id']]);self.assertEqual(len(self.provider.requests[-1][1]['context']),1)
    def test_apply_is_idempotent_and_feedback(self):
        run=self.action('run',prompt='Planeje');self.action('run.apply',id=run['id'])
        with self.assertRaises(Problem):self.action('run.apply',id=run['id'])
        self.assertEqual(len(self.store.read()['tasks']),2)
        self.action('feedback',id=run['id'],rating=4,note='Mais curto')
        self.assertEqual(self.store.read()['runs'][0]['feedback']['rating'],4)
        with self.assertRaises(Problem):self.action('feedback',id=run['id'],rating=True)
    def test_budget_counts_failed_attempts_and_restart(self):
        self.svc.daily_limit=1;self.provider.fail=True
        with self.assertRaises(Problem):self.action('run',prompt='Teste')
        self.assertEqual(self.store.read()['usage'][0]['status'],'error')
        self.provider.fail=False
        with self.assertRaises(Problem) as cm:self.action('run',prompt='Teste')
        self.assertEqual(cm.exception.status,429);self.assertEqual(len(self.provider.requests),1)
    def test_missing_key_does_not_reserve(self):
        self.provider.key=''
        with self.assertRaises(Problem):self.action('run',prompt='Teste')
        self.assertFalse(self.store.read()['usage'])
    def test_evolution_review_promotion_rollback(self):
        c=self.action('candidate',goal='Mais clareza');e=self.action('evaluate',id=c['id'])
        self.assertEqual(len(e['cases']),3);self.assertEqual(len(self.provider.requests),7)
        self.assertEqual(e['scores'],{'baseline':100.0,'candidate':100.0})
        with self.assertRaises(Problem):self.action('promote',id=e['id'],review='Bom',approved=False)
        self.action('promote',id=e['id'],review='Conferi os três casos',approved=True)
        self.assertEqual(self.store.read()['active'],c['id'])
        self.action('rollback',id='base');self.assertEqual(self.store.read()['active'],'base')
        with self.assertRaises(Problem):self.action('promote',id=e['id'],review='Bom',approved=True)
    def test_holdout_does_not_leak_or_erase_memory_on_error(self):
        self.action('memory.add',title='Segredo comercial',body='Cliente privado')
        c=self.action('candidate',goal='Clareza')
        self.assertNotIn('Cliente privado',json.dumps(self.provider.requests[-1]))
        self.provider.fail=True
        with self.assertRaises(Problem):self.action('evaluate',id=c['id'])
        self.assertEqual(len(self.store.read()['memories']),1)
        self.assertEqual(self.provider.requests[-1][1]['context'],[])
    def test_stale_candidate_blocked(self):
        a=self.action('candidate',goal='Clareza');b=self.action('candidate',goal='Curto')
        e=self.action('evaluate',id=a['id']);self.action('promote',id=e['id'],review='Revisado',approved=True)
        with self.assertRaises(Problem):self.action('evaluate',id=b['id'])
    def test_evaluation_requires_six_available_calls(self):
        c=self.action('candidate',goal='Clareza');self.svc.daily_limit=6
        with self.assertRaises(Problem):self.action('evaluate',id=c['id'])
        self.assertEqual(len(self.provider.requests),1)
    def test_backup_preserves_call_budget_and_disables_routines(self):
        self.action('run',prompt='Olá');backup=initial()
        self.action('restore',backup=backup)
        self.assertEqual(len(self.store.read()['usage']),1)
        with self.assertRaises(Problem):validate_backup({'schema':1})
    def test_malformed_backup_is_rejected_without_replacement(self):
        self.action('task.add',title='Preservar')
        b=self.store.read();b['runs']=[{'id':'bad'}]
        with self.assertRaises(Problem):self.action('restore',backup=b)
        self.assertEqual(self.store.read()['tasks'][0]['title'],'Preservar')
    def test_imported_score_cannot_inject_markup(self):
        c=self.action('candidate',goal='Teste');self.action('evaluate',id=c['id'])
        b=self.store.read();b['experiments'][0]['scores']['candidate']='100; color:red'
        with self.assertRaises(Problem):self.action('restore',backup=b)
    def test_imported_eval_cannot_authorize(self):
        c=self.action('candidate',goal='Teste');e=self.action('evaluate',id=c['id']);backup=self.store.read()
        self.action('restore',backup=backup)
        with self.assertRaises(Problem):self.action('promote',id=e['id'],approved=True,review='Revisado')
    def test_scheduler_generates_draft_only_once(self):
        r=self.action('routine.add',name='Rotina',prompt='Planeje o dia')
        s=self.store.read();s['routines'][0]['enabled']=True;self.store.write(s)
        self.svc.tick();self.svc.tick()
        self.assertEqual(len(self.store.read()['runs']),1);self.assertFalse(self.store.read()['tasks'])
    def test_scheduler_disables_on_failure(self):
        self.action('routine.add',name='Rotina',prompt='Planeje');s=self.store.read();s['routines'][0]['enabled']=True;self.store.write(s)
        self.provider.fail=True;self.svc.tick();self.assertFalse(self.store.read()['routines'][0]['enabled'])
    def test_concurrent_tasks_not_lost(self):
        threads=[threading.Thread(target=self.action,args=('task.add',),kwargs={'title':f'Tarefa {i}'}) for i in range(12)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(len(self.store.read()['tasks']),12)
    def test_fabricated_sources_rejected(self):
        original=self.provider.generate
        def fabricated(system,payload):
            result,meta=original(system,payload);result['sources']=['inventada'];return result,meta
        self.provider.generate=fabricated
        with self.assertRaises(Problem):self.action('run',prompt='Olá')
        self.assertFalse(self.store.read()['runs']);self.assertEqual(len(self.store.read()['usage']),1)

class HTTPTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.svc=Service(Store(Path(cls.tmp.name)/'http.db'),FakeProvider())
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),lambda *a:None);cls.port=cls.server.server_port
        cls.server.RequestHandlerClass=make_handler(cls.svc,cls.port,'test-session')
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.tmp.cleanup()
    def req(self,path,method='GET',body=None,headers=None):
        return urlopen(Request(f'http://127.0.0.1:{self.port}'+path,data=body,method=method,headers=headers or {}))
    def test_static_and_session(self):
        with self.req('/app/') as r:self.assertIn(b'RSI Copiloto',r.read())
        with self.req('/api/session') as r:self.assertEqual(json.load(r)['token'],'test-session')
    def test_no_secrets_or_traversal_served(self):
        for path in ['/rsi/core.py','/.git/config','/app/../rsi/core.py','/app/%2e%2e/rsi/core.py']:
            with self.assertRaises(HTTPError) as cm:self.req(path)
            self.assertEqual(cm.exception.code,404)
    def test_cross_origin_token_and_host(self):
        for headers in [{},{'X-RSI-Token':'test-session','Origin':'https://evil.example'},{'X-RSI-Token':'test-session','Host':'evil.example'}]:
            with self.assertRaises(HTTPError) as cm:self.req('/api/action','POST',b'{}',headers)
            self.assertEqual(cm.exception.code,403)
    def test_api_mutation(self):
        body=json.dumps({'action':'task.add','data':{'title':'API task'}}).encode()
        with self.req('/api/action','POST',body,{'X-RSI-Token':'test-session','Content-Type':'application/json'}) as r:self.assertEqual(json.load(r)['result']['title'],'API task')
    def test_json_errors_and_media_type(self):
        for body,ctype,status in [(b'[]','application/json',400),(b'{','application/json',400),(b'{}','text/plain',415)]:
            with self.assertRaises(HTTPError) as cm:self.req('/api/action','POST',body,{'X-RSI-Token':'test-session','Content-Type':ctype})
            self.assertEqual(cm.exception.code,status)

if __name__=='__main__':unittest.main()
