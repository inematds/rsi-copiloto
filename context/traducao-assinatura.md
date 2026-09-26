# Tradução da interface pública para EN/ES

Em 2026-09-26, tradução e implementação foram feitas pelo subagente configurado GPT-6 Luna pela assinatura. Nenhuma API, chave ou chamada de tradutor foi usada.

## Cobertura

Foram criadas as superfícies `app/en/` e `app/es/` com o CSS e a lógica compartilhados. A interface traduz rótulos, navegação, formulários, mensagens de validação e erro do cliente, metadados, catálogo, saídas fixas de demonstração e fluxos de missão. Guias e READMEs em inglês e espanhol apontam para a interface correspondente. O seletor mantém rota, query e hash. O conteúdo criado pelo usuário permanece literal ao trocar idioma; exemplos locais novos usam o idioma escolhido. Os marcadores ativos passaram a `1.2.0`, sem alterar schema ou contrato do backend.

Mensagens geradas pelo backend/IA e erros locais do servidor continuam no idioma original, assim como dados já persistidos e texto livre do usuário. A demonstração pública segue sem IA real.

## Verificação observada

- `node --check` passou para `app/i18n.js`, `app/app.js`, `app/missions.js`, `app/demo.js` e `app/backup.js`.
- `python3 scripts/check_site.py` passou: três guias, 9 seções cada, arquivos estáticos e links multilíngues válidos.
- `python3 -m unittest discover -s tests -v` passou: 32 testes.
- Browser local, com tráfego externo bloqueado: fluxo completo de missão em EN e ES, aprovação, correção, etapa seguinte e conclusão; evolução LOOP-R, laboratório, backup, CRUD e troca de idioma com hash/query; 9 rotas em 360 e 1440 px sem erros de página ou overflow.
- Verificador independente confirmou que tarefas intituladas “Missões” e “Instrução inicial” permaneceram iguais após alternar EN/ES e que nenhuma tarefa ficou invisível.
- Scanner de rotas não encontrou resíduos em português; os resultados restantes são construções válidas em espanhol iniciadas por “Preparar”.
- `git diff --check` passou.

Uma repetição em espanhol encontrou e corrigiu escritas idênticas do MutationObserver que congelavam a página. A falha está registrada em `FALHAS.md`.
