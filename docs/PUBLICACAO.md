# Publicação — RSI Copiloto v1.0.0

25/09/2026. Projeto novo e independente de `rsi`, criado por instrução do usuário. Os arquivos existentes de `rsi` não foram alterados.

## Endereços verificados

- Aplicativo público: https://inematds.github.io/rsi-copiloto/app/
- Guia PT: https://inematds.github.io/rsi-copiloto/guia/
- Guia EN: https://inematds.github.io/rsi-copiloto/guia/en/
- Guia ES: https://inematds.github.io/rsi-copiloto/guia/es/
- Código: https://github.com/inematds/rsi-copiloto
- Aplicativo local com IA: http://127.0.0.1:8765/app/

App, guias, JavaScript, catálogo de rotinas e imagens retornaram HTTP 200. Workflow GitHub Actions `36106240022` concluído com sucesso após habilitar Pages. Smoke no site publicado confirmou navegação, criação de tarefa e persistência após recarga, sem erros de página.

Serviço local `rsi-copiloto.service` ativo no systemd do usuário, credencial detectada em runtime, banco novo sem dados de teste e nenhuma rotina automática ativada.

## Pushes confirmados

| Repositório | Commit | Alteração |
|---|---|---|
| inematds/rsi-copiloto | `78c97b0` | Sistema, guia e deploy inicial |
| NeiMaldaner/portal | `2ba8504` | Projeto, novidade e guias EN/ES (id de tradução 10005) |
| inematds/inemabuscas | `63da589` | Projeto no índice de busca |
| inematds/inemapro | `63dd5e2` | Classificação, base e catálogo PRO |

Portal: aparece no quadro Últimas Atualizações de Projetos e nas seções de traduções EN/ES conforme o deploy automático via git. O grid de projetos está oculto na home; não foi religado. PRO recebe catálogo e busca. Nenhum painel ou status de Vercel foi consultado; a conclusão dessa publicação é o push no origin.

## Validação da cadeia de catálogo

11 testes do portal, build Next.js com Webpack e TypeScript passaram. Webpack foi usado porque Turbopack não aceita o symlink de dependências da cópia isolada. 41 testes do content-base passaram. Regeneração da base acrescentou exatamente um ID, sem remoções: **18.405 → 18.406 itens**.

| Fonte | Itens |
|---|---:|
| Resumos | 2.469 |
| Wiki | 157 |
| Projetos | 252 |
| Cursos | 290 |
| Clipes | 12.399 |
| Lives | 1.393 |
| Telegram | 6 |
| Prompts | 1.440 |

A base deduplicada classifica 100% dos cursos/projetos. Novo ID: `projeto:rsi-copiloto-guia`, nível avançado, áreas agentes-ia e negocios-estrategia-ia. Catálogo bruto do PRO: 291 cursos e 253 projetos (antes da deduplicação da base).

## Preservação de outras sessões

A publicação usou cópias isoladas em `/tmp/rsi-publish/`, mantendo intactas as alterações pendentes nos checkouts compartilhados. `inemabuscas` tem o remoto de rastreamento próprio; o alias origin antigo da pasta original aponta ao monorepo. O origin foi ajustado somente na cópia isolada. O pipeline da skill atualiza-portal foi executado por etapas com os diretórios isolados e as mesmas validações, sem chamar o script de caminhos fixos sobre as pastas compartilhadas.
