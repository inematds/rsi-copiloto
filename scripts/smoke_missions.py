"""Paid, synthetic, temporary-db mission and LOOP-R smoke; no production promotion."""
import json,tempfile
from pathlib import Path
from rsi.core import Service,Store
with tempfile.TemporaryDirectory() as tmp:
    svc=Service(Store(Path(tmp)/'smoke.db'))
    m=svc.action('mission.create',{'goal':'Crie dois documentos para uma loja fictícia: primeiro uma proposta de 4 posts com escopo e exclusões; depois uma mensagem curta de apresentação da proposta. Organize em duas etapas de produção de texto, sem envio externo. Preço e prazo ainda não definidos.'})['result']
    def action(name,**kwargs):
        global m
        m=svc.action('mission.'+name,{'id':m['id'],'revision':m['revision'],**kwargs})['result']
        assert not m['error'],m['error']
    assert all(x['kind']=='draft' for x in m['steps'])
    action('start');action('revise',note='Explicite que fotos e aprovação do material são responsabilidade do cliente fictício. Não invente preço.')
    while m['status']=='review': action('approve',note='Fluxo verificado com dados fictícios; seguir para a próxima etapa.',rating=4)
    assert m['status']=='completed'
    c=svc.action('candidate',{'goal':'Incluir dependências e exclusões em propostas futuras.','mission':m['id']})['result']
    e=svc.action('evaluate',{'id':c['id']})['result']
    s=svc.state()
    report={'version':s['version'],'model':svc.provider.model,'steps':len(m['steps']),'attempts':[len(x['attempts']) for x in m['steps']],
        'status':m['status'],'candidate_linked_to_mission':c['mission']==m['id'],'scores':e['scores'],
        'calls':len(s['usage']),'tokens':sum(x.get('tokens',0) for x in s['usage']),
        'reported_cost_usd':sum(x.get('cost') or 0 for x in s['usage']),
        'promotion':'not performed; production promotion requires human review',
        'scope':'Integration test, not evidence of improved business quality.'}
    Path('docs/SMOKE-MISSOES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
