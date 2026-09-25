import copy
import json
import tempfile
import unittest
from pathlib import Path
from rsi.core import Service,Store,Problem,initial,validate_backup
from test_core import FakeProvider

class MissionProvider(FakeProvider):
    manual=False
    def generate(self,system,payload):
        if 'goal' in payload and 'current' not in payload:
            self.requests.append((system,payload))
            return {'title':'Proposta comercial','steps':[
                {'title':'Preparar proposta','instruction':'Escreva a proposta pronta.','kind':'draft'},
                {'title':'Enviar ao cliente' if self.manual else 'Consolidar proposta','instruction':'Envie manualmente.' if self.manual else 'Consolide a proposta com o feedback.','kind':'manual' if self.manual else 'draft'}]}, {'model':self.model,'tokens':10,'cost':0}
        return super().generate(system,payload)

class MissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.provider=MissionProvider();self.svc=Service(Store(Path(self.tmp.name)/'test.db'),self.provider)
    def tearDown(self):self.tmp.cleanup()
    def create(self):return self.svc.action('mission.create',{'goal':'Produza uma proposta'})['result']
    def act(self,action,m,**data):return self.svc.action('mission.'+action,{'id':m['id'],'revision':m['revision'],**data})['result']
    def test_full_mission_then_loop_r(self):
        m=self.create();self.assertEqual(m['status'],'plan');self.assertEqual(len(self.provider.requests),1)
        m=self.act('start',m);self.assertEqual(m['status'],'review')
        m=self.act('revise',m,note='Inclua exclusões');self.assertEqual(len(m['steps'][0]['attempts']),2)
        m=self.act('approve',m,note='Agora ficou bom',rating=4);self.assertEqual(m['current'],1)
        payload=self.provider.requests[-1][1]['demand'];self.assertIn('Agora ficou bom',payload);self.assertIn('approved_results',payload)
        m=self.act('approve',m,note='Conferido',rating=5);self.assertEqual(m['status'],'completed')
        c=self.svc.action('candidate',{'mission':m['id'],'goal':'Evitar omissão de exclusões'})['result']
        evidence=self.provider.requests[-1][1]['mission_evidence'];self.assertEqual(evidence['steps'][0]['attempts'],2);self.assertEqual(c['mission'],m['id'])
        e=self.svc.action('evaluate',{'id':c['id']})['result']
        self.svc.action('promote',{'id':e['id'],'approved':True,'review':'Revisei os casos'})
        self.assertEqual(self.create()['version'],c['id'])
        self.assertEqual(self.svc.state()['missions'][1]['version'],'base')
    def test_stale_approval_never_executes_twice(self):
        m=self.create();stale=copy.deepcopy(m);m=self.act('start',m);calls=len(self.provider.requests)
        with self.assertRaises(Problem):self.act('start',stale)
        self.assertEqual(len(self.provider.requests),calls)
    def test_next_step_failure_keeps_approval_and_retry(self):
        m=self.act('start',self.create());self.provider.fail=True
        m=self.act('approve',m,note='Aprovado',rating=5)
        self.assertEqual(m['status'],'ready');self.assertEqual(m['steps'][0]['status'],'approved');self.assertTrue(m['error'])
        self.provider.fail=False;m=self.act('retry',m);self.assertEqual(m['status'],'review');self.assertEqual(m['current'],1)
    def test_manual_step_is_not_reported_executed(self):
        self.provider.manual=True;m=self.act('start',self.create());calls=len(self.provider.requests)
        m=self.act('approve',m);self.assertEqual(m['status'],'manual');self.assertEqual(len(self.provider.requests),calls)
        with self.assertRaises(Problem):self.act('manual',m,note='')
        m=self.act('manual',m,note='Enviei manualmente, cliente confirmou recebimento.');self.assertEqual(m['status'],'completed')
    def test_pause_resume_and_cancel(self):
        m=self.act('start',self.create());m=self.act('pause',m)
        with self.assertRaises(Problem):self.act('approve',m)
        m=self.act('resume',m);self.assertEqual(m['status'],'review');m=self.act('cancel',m)
        with self.assertRaises(Problem):self.act('retry',m)
    def test_migration_restore_and_invalid_cursor(self):
        old=initial();del old['missions'];self.svc.store.write(old)
        self.assertEqual(self.svc.state()['missions'],[]);self.assertEqual(validate_backup(old)['missions'],[])
        m=self.act('start',self.create());backup=self.svc.state();self.assertEqual(validate_backup(backup)['missions'][0]['status'],'review')
        backup['missions'][0]['current']=99
        with self.assertRaises(Problem):validate_backup(backup)
    def test_revision_requires_text_and_loop_r_requires_completion(self):
        m=self.act('start',self.create())
        with self.assertRaises(Problem):self.act('revise',m,note='')
        with self.assertRaises(Problem):self.svc.action('candidate',{'goal':'Melhore','mission':m['id']})
    def test_profile_and_budget_gates(self):
        m=self.create();self.svc.action('profile',{'profile':'empresa'})
        with self.assertRaises(Problem):self.act('start',m)
        self.svc.action('profile',{'profile':'pessoal'});self.svc.daily_limit=1
        m=self.act('start',m);self.assertEqual(m['status'],'ready');self.assertIn('Limite',m['error'])
    def test_plan_revision_and_instruction_pinning(self):
        m=self.create();m=self.act('replan',m,note='Use duas etapas');self.assertEqual(m['revision'],1)
        m=self.act('start',m)
        with self.assertRaises(Problem):self.act('replan',m,note='Outra')
        self.assertEqual(m['instruction'],self.svc.state()['versions'][0]['prompt'])

if __name__=='__main__':unittest.main()
