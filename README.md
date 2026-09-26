# RSI Copiloto

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![RSI Copiloto](guia/assets/banner.jpg)](https://inematds.github.io/rsi-copiloto/guia/)

Assistente local com IA, memória, tarefas e ciclos de melhoria supervisionada para pessoas físicas, profissionais independentes e pequenas empresas. **Projeto separado da [pesquisa RSI](https://inematds.github.io/rsi/guia/)**.

**[Experimentar demonstração](https://inematds.github.io/rsi-copiloto/app/)** · **[Guia de uso](https://inematds.github.io/rsi-copiloto/guia/)**

A demonstração usa exemplos programados e armazenamento do navegador. A versão local chama IA real via OpenRouter e persiste dados em SQLite. A demonstração agora oferece interface PT/EN/ES; o guia e o README também estão traduzidos.

## Rodar

Python 3.11+ e Git. Sem dependências Python adicionais.

```bash
git clone https://github.com/inematds/rsi-copiloto.git
cd rsi-copiloto
python3 -m rsi.server
```

Abra **http://127.0.0.1:8765/app/**. O servidor atende somente em loopback; uso individual.

A credencial `OPENROUTER_API_KEY` é lida do ambiente ou do arquivo apontado por `RSI_ENV_FILE`. Na máquina do autor, também procura `~/projetos/openpcbotv2/.env` e `~/projetos/wifi/.env`. Não copie chaves para este repositório.

```bash
RSI_ENV_FILE="$HOME/.config/minhas-credenciais.env" python3 -m rsi.server
```

O arquivo indicado precisa conter `OPENROUTER_API_KEY`. Configuração opcional: `RSI_MODEL` (padrão `openai/gpt-5.4-nano`), `RSI_DAILY_CALLS` (50 tentativas/dia UTC), `RSI_DB`, `--port`, `--db`, `--no-scheduler`. Até 2.400 tokens de saída por chamada. Limite de chamadas não equivale a teto financeiro.

## O que funciona

- Três espaços: pessoal, autônomo e pequena empresa; nove rotinas prontas.
- Entregas com lacunas, fontes de memória, próximos passos, tokens e custo informado.
- Tarefas, conhecimento por perfil e contexto recuperado por palavras.
- Feedback, proposta de instrução, comparação atual/candidata em três casos, revisão humana, promoção e reversão.
- Rotinas diárias opcionais com servidor aberto; falha pausa a rotina.
- Histórico, backup JSON/restauração, tarefas CSV e calendário `.ics`.

O ciclo melhora instruções e processos, **não os pesos do modelo**. Os checks são estruturais, não provam verdade ou ganho de negócio. A instrução ativa vale para os três espaços. A IA não envia mensagens, movimenta dinheiro nem executa comandos. Integrações externas e múltiplos usuários são etapas futuras.

## Dados

SQLite em `~/.local/share/rsi-copiloto/state.sqlite3`, fora do diretório publicado. A API recebe demanda, perfil, instrução e até cinco memórias relevantes. Backup contém dados dos três espaços: mantenha-o privado. Importar pausa recorrências e exige nova avaliação antes de promover instruções; o limite diário de uso local é preservado.

## Verificar

```bash
python3 -m unittest discover -s tests -v
# Opcional: teste real pago, até oito chamadas, somente dados fictícios.
python3 -m scripts.smoke_live
```

[Plano](docs/PLANO-IMPLEMENTACAO.md) · [Operação](docs/OPERACAO.md) · [Validação](docs/VALIDACAO.md) · [Changelog](CHANGELOG.md)

Projeto aberto e gratuito de pesquisa e educação do [INEMA.CLUB](https://inema.club).

## Missão e LOOP-R: dois ciclos conectados.

Você define a missão. A IA propõe de uma a cinco etapas. Confira o plano e clique em “Aprovar plano e executar primeira etapa”. A entrega aparece na mesma missão, aguardando sua avaliação.

Clique em “Aprovar e executar próxima etapa” para o copiloto continuar usando a entrega e sua avaliação. “Corrigir esta etapa” refaz o trabalho atual. Você também pode pausar, recarregar a página e retomar. Salvar na memória é opcional: o histórico da missão já é preservado.

**Executar → Medir → Criticar → Propor → Testar → Validar → Promover → Repetir**

Ao concluir, veja sua nota média e a quantidade de correções. Clique em “Iniciar LOOP-R desta missão”. A IA recebe essas evidências, critica as falhas e propõe uma instrução candidata. No laboratório, compare atual e candidata, leia as respostas, registre seu parecer e só então promova.

Novas missões usam a instrução promovida. Missões já iniciadas mantêm sua versão. É evolução supervisionada de instruções e procedimentos, sem treino dos pesos do modelo. Os três testes gerais verificam estrutura; não comprovam ganho de qualidade ou resultado financeiro.

Na demonstração pública, as entregas são exemplos programados. O fluxo completo funciona; para executar o conteúdo da sua missão com IA, use a versão local.
