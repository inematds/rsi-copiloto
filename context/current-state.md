# Estado atual — 2026-09-25
v1.0.0 concluída, separada da pesquisa rsi a pedido explícito do usuário. Sistema publicado em https://inematds.github.io/rsi-copiloto/app/; guia PT/EN/ES em /guia/. Backend local via systemd rsi-copiloto em 127.0.0.1:8765, configurado para ler credenciais existentes em runtime, banco fora do Git.

23 testes backend, ciclo E2E Chromium (32 combinações de tela/tema/viewport) e smoke pago com 8 chamadas passaram. Guias e assets HTTP 200. Portal, busca e PRO receberam push; ver docs/PUBLICACAO.md para SHAs e contagens. Alterações de outras sessões nos repositórios compartilhados foram preservadas por publicar via /tmp/rsi-publish.

Não há pendência de entrega. Limites deliberados: aplicação individual, interface PT, demo pública sem IA, sem conectores externos; avaliação estrutural não prova ganho semântico. Próximos incrementos estão em docs/PLANO-IMPLEMENTACAO.md. Não refazer chamadas pagas ou pesquisa sem necessidade.
