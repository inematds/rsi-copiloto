# Evidências de validação — v1.0.0

Data: 25/09/2026. Dados sintéticos; nenhum conteúdo privado usado no teste pago.

- **23 testes Python passaram:** persistência SQLite, separação de memória por perfil, fontes inventadas, conversão de tarefas sem duplicação, feedback, orçamento e falhas, avaliações sem vazamento de contexto, revisão obrigatória, promoção e rollback, candidatos obsoletos, backups inválidos, agendador, concorrência e proteção HTTP/arquivos.
- **Navegador Chromium via Playwright:** ciclo completo na demo, dados persistidos após recarga, troca de perfil, exportação .ics/JSON, restauração válida e rejeição de backup corrompido. Oito telas em 360px e 1440px, dark/light (32 combinações), sem overflow horizontal nem exceções de página. Adaptador HTTP local também exercitado com criação/remoção de tarefa.
- **IA real, OpenRouter:** oito chamadas com `openai/gpt-5.4-nano`, 7.715 tokens, custo reportado US$ 0,00632155. Entrega citou uma memória válida; proposta de instrução e comparação A/B concluídas. JSON medido em [SMOKE-IA.json](SMOKE-IA.json).
- **Resultado do experimento:** 100/100 nas duas versões na régua estrutural. Não há evidência de ganho de qualidade; nenhuma promoção foi feita no smoke. O teste comprova integração e contratos, não eficácia geral.
- **Publicação:** workflow testa Python, sintaxe JS e arquivos de site antes de publicar somente `app/`, `guia/`, `capa/` e redirecionamento da raiz.

## Reproduzir

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
python3 -m rsi.server --db /tmp/rsi-test.sqlite3 --no-scheduler
# Em outro terminal, com pacote Playwright Node instalado:
node tests/browser.cjs
# Pago, opcional:
python3 -m scripts.smoke_live
```

`RSI_PLAYWRIGHT` pode apontar para o pacote Playwright já instalado. O script de navegador roda em contexto novo; use banco de teste no servidor. Screenshots da inspeção visual foram feitas em desktop e mobile; a tela desktop está no guia.
