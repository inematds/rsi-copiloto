# Estado atual — 2026-09-26

RSI Copiloto v1.2.0: corrigido o escopo conforme o usuário. Missão → plano → aprovação → entrega → avaliação/correção → próxima etapa → conclusão. LOOP-R ligado às evidências da missão: medir notas/correções, criticar/propor, testar A/B, validar e promover sob revisão humana; novas missões usam a instrução aprovada, missões iniciadas ficam na versão original.

Na validação histórica da v1.1.0 em 25/09, passaram 32 testes backend, E2E da demo, regressão de UI e smoke IA real. Na v1.2.0, passaram novamente os 32 testes com provedores simulados e os fluxos locais EN/ES descritos em context/traducao-assinatura.md; nenhuma chamada de IA real foi feita. O serviço local não foi reiniciado nem consultado nesta tradução: sua última versão confirmada continua sendo v1.1.0 em http://127.0.0.1:8765/app/. Site público segue demonstração SEM IA.

URLs existentes preservadas: https://inematds.github.io/rsi-copiloto/app/ e /guia/. O portal já aponta para esse guia; nenhuma nova entrada é necessária. Tradução v1.2.0 enviada ao origin inematds/rsi-copiloto no commit 00af515. As URLs /app/en/ e /app/es/ responderam HTTP 200 com idioma correto e versão 1.2.0. Os fluxos desta revisão foram testados localmente; o smoke público de missão/LOOP-R pertence à validação anterior da v1.1.0. Sem edições nos checkouts compartilhados de portal/busca/PRO nesta atualização.

Limites: produzir texto, análise e documentos; ações externas aparecem como manuais e exigem resultado registrado pelo operador. Sem treinamento de pesos. Métricas estruturais não comprovam qualidade semântica. Ver docs/OPERACAO.md, docs/VALIDACAO.md e docs/SMOKE-MISSOES.json.


v1.2.0: interface pública do app traduzida para EN/ES com demo e catálogos localizados; armazenamento e estrutura do estado permanecem compartilhados.
