# Operação — RSI Copiloto v1.0.0

## Instalação individual

`python3 -m rsi.server` inicia em `127.0.0.1:8765`. Python 3.11+, biblioteca padrão. Rode na raiz do repositório. Para acesso sem IA, use o app no GitHub Pages ou acrescente `?demo` à URL local. Se o servidor local falhar, o aplicativo mostra o erro e não troca silenciosamente para demonstração.

Credenciais são lidas em runtime na ordem: variável `OPENROUTER_API_KEY`, arquivo `RSI_ENV_FILE`, `~/projetos/openpcbotv2/.env`, `~/projetos/wifi/.env`. O arquivo precisa ter a linha de definição dessa variável. Não cole chaves no navegador ou no Git. O programa não executa o arquivo de ambiente como código.

## Configuração

| Opção | Padrão | Efeito |
|---|---|---|
| `RSI_MODEL` | `openai/gpt-5.4-nano` | ID do modelo no OpenRouter |
| `RSI_DAILY_CALLS` | 50 | Tentativas por dia UTC; faixa 1–500 |
| `RSI_ENV_FILE` | busca nos locais documentados | Arquivo existente com credencial |
| `RSI_DB` / `--db` | `~/.local/share/rsi-copiloto/state.sqlite3` | Banco privado |
| `--port` | 8765 | Porta local |
| `--no-scheduler` | desligado | Desativa execução automática de rotinas |

Cada chamada tem timeout de 90 segundos e saída limitada a 2.400 tokens. Não há retry automático de geração; falhas contam no limite. Uma comparação usa seis chamadas, precedida de verificação de capacidade disponível. O limite persiste no banco e não é zerado por importação de backup. Arquivo de banco novo tem contagem própria. O custo exibido é o valor informado pelo provedor e pode estar ausente em falhas; não é um limite financeiro.

## Fluxo e autonomia

1. Registrar fatos em Conhecimento; busca literal por palavras seleciona até cinco memórias do perfil ou compartilhadas.
2. Pedir uma entrega. Só demanda, perfil, instrução e contexto selecionado vão ao provedor.
3. Revisar a saída. As fontes precisam corresponder às memórias enviadas; a aplicação rejeita IDs inventados.
4. Converter próximos passos em tarefas, copiar ou baixar a entrega. Nenhuma ação externa é executada.
5. Avaliar e propor nova instrução. O modelo recebe até oito feedbacks recentes, sem o conjunto de avaliação.
6. Comparar em três casos fixos, sem memórias reais. Check de estrutura: 100 pontos possíveis.
7. Ler os dois lados, registrar parecer e aprovar. Candidata obsoleta ou com regressão é bloqueada. Uma instrução já promovida não é promovida duas vezes. Rollback preserva histórico.

A instrução ativa é global aos três perfis. A separação de perfis é organização de contexto, não controle de acesso entre pessoas. Para medir resultado empresarial, registre também retrabalho, utilidade, tempo e erros em um piloto humano; o sistema não calcula esses ganhos.

## Agendador

Executa uma verificação a cada 30 segundos. Ao ativar uma rotina, a primeira execução é agendada para 24h depois. Se o computador estiver desligado, na volta ocorre no máximo uma execução por rotina vencida, não um lote de dias acumulados. O próximo disparo é reservado antes de chamar a API. Falha pausa a rotina. Apenas rascunhos são produzidos, consumindo o limite diário. Tarefas não são automaticamente concluídas.

## Dados e cópias

Banco em SQLite com permissão 0600. Estado é gravado em transações; solicitações são serializadas por processo. Rode somente uma instância por banco. Exportar backup inclui todos os perfis, memórias, entregas, avaliações e registros locais. Não coloque esse arquivo em um repositório público. Para copiar o SQLite diretamente, pare o servidor primeiro. O backup JSON pela interface pode ser feito com o serviço rodando.

Restaurar substitui os dados dos três perfis, preserva a contagem de chamadas do banco atual, pausa rotinas e desabilita a promoção a partir de experimentos importados. Importação limita o arquivo a 5 MB e valida o formato. O histórico mantém até 500 eventos e não oferece assinatura ou imutabilidade.

## Segurança e fronteiras

Servidor ligado apenas a loopback, valida Host, Origin nas mutações, token por instância, conteúdo JSON e tamanho das solicitações. Apenas `app`, `guia` e `capa` são servidos. Sem execução de shell, código da IA ou ferramentas externas. Renderização escapa conteúdo e exportação CSV neutraliza prefixos de fórmula. Isso é uma base individual; não exponha como serviço multiusuário sem implementar autenticação, autorização, limites por organização e revisão de segurança.

## Testes e manutenção

```bash
python3 -m unittest discover -s tests -v
# Opcional pago; oito chamadas com exemplos fictícios em banco temporário.
python3 -m scripts.smoke_live
# Com Playwright Node já instalado (apontar RSI_PLAYWRIGHT para o pacote se necessário):
node tests/browser.cjs
```

O teste de navegador espera servidor em 8765 com banco de teste. Use `--db /tmp/rsi-test.sqlite3 --no-scheduler`; ele cria e remove uma tarefa e exercita o armazenamento de demonstração em contexto isolado.

## Evolução de produto

Integrações externas, múltiplos usuários, coleta de métricas de negócio, avaliação semântica e novos conjuntos reservados são extensões futuras. O plano de implementação registra o escopo atual. Conceitos e fontes sobre RSI estão no projeto original: https://inematds.github.io/rsi/guia/.

## Serviço local com systemd (Linux)

O arquivo `deploy/rsi-copiloto.service` usa a instalação em `~/projetos/rsi-copiloto`. Se instalou em outro local, ajuste `WorkingDirectory` antes de instalar. Não contém segredos.

```bash
mkdir -p ~/.config/systemd/user
cp deploy/rsi-copiloto.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now rsi-copiloto
systemctl --user status rsi-copiloto
# Para encerrar e desativar a inicialização:
systemctl --user disable --now rsi-copiloto
```

Um serviço de usuário inicia na sessão do usuário; operar sem sessão ativa exige configurar linger separadamente. Nenhuma rotina é ativada por instalar o serviço.
