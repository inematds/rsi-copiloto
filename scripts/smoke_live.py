"""Optional paid smoke: uses eight calls, a temporary DB, and synthetic inputs only."""
import json
import tempfile
from pathlib import Path
from rsi.core import Provider, Service, Store

def main():
    provider=Provider()
    with tempfile.TemporaryDirectory() as tmp:
        svc=Service(Store(Path(tmp)/'smoke.db'),provider)
        def act(a,**d):return svc.action(a,d)['result']
        act('profile',profile='autonomo')
        act('memory.add',title='Política de proposta',body='Toda proposta de posts inclui duas rodadas de revisão. Preço somente após validar escopo.')
        run=act('run',prompt='Prepare uma proposta de 4 posts para uma loja fictícia. Ainda não temos preço. Use a política de proposta.')
        assert run['output']['answer'] and run['output']['sources']
        act('feedback',id=run['id'],rating=4,note='Boa proposta. Explicite sempre o que falta confirmar antes de começar.')
        candidate=act('candidate',goal='Explicitar lacunas e colocar um próximo passo verificável no fim.')
        exp=act('evaluate',id=candidate['id'])
        s=svc.state()
        report={'version':s['version'],'provider':'OpenRouter','model':provider.model,'calls':len(s['usage']),
                'tokens':sum(x.get('tokens',0) for x in s['usage']),
                'reported_cost_usd':sum(x.get('cost') or 0 for x in s['usage']),
                'sources_used':len(run['output']['sources']),'comparison_scores':exp['scores'],
                'eligible':exp['eligible'],'promotion':'not performed — requires human review',
                'conclusion':'Live generation, memory citation, candidate proposal and six comparison responses validated. Structural scores are not business-quality evidence.'}
        Path('docs/SMOKE-IA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
