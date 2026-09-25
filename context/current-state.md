# Estado atual — 2026-09-25

RSI Copiloto v1.1.0: corrigido o escopo conforme o usuário. Missão → plano → aprovação → entrega → avaliação/correção → próxima etapa → conclusão. LOOP-R ligado às evidências da missão: medir notas/correções, criticar/propor, testar A/B, validar e promover sob revisão humana; novas missões usam a instrução aprovada, missões iniciadas ficam na versão original.

32 testes backend, E2E de missão até promoção na demo, regressão de UI (36 combinações) e smoke IA real passaram. Guias PT/EN/ES atualizados. Serviço local v1.1.0 em http://127.0.0.1:8765/app/, backup privado do banco antes da migração. Site público segue demonstração SEM IA; versão local gera conteúdo real.

URLs existentes preservadas: https://inematds.github.io/rsi-copiloto/app/ e /guia/. O portal já aponta para esse guia; nenhuma nova entrada é necessária. Publicação da atualização pelo origin inematds/rsi-copiloto. Sem edições nos checkouts compartilhados de portal/busca/PRO nesta atualização.

Limites: produzir texto, análise e documentos; ações externas aparecem como manuais e exigem resultado registrado pelo operador. Sem treinamento de pesos. Métricas estruturais não comprovam qualidade semântica. Ver docs/OPERACAO.md, docs/VALIDACAO.md e docs/SMOKE-MISSOES.json.
