# RSI Copiloto — plano e critérios de entrega

## Objetivo
Transformar a pesquisa de RSI em um assistente utilizável no cotidiano. O ciclo opera sobre instruções e rotinas: executar, medir, registrar feedback, propor, comparar, revisar, promover e reverter. Não altera pesos de modelos nem executa código gerado.

## Entregas
1. **Base operacional:** servidor Python 3.11+, SQLite, UI responsiva, perfis pessoal/autônomo/empresa, tarefas, memória, auditoria, exportação e restauração.
2. **Assistente:** instruções versionadas, conhecimento recuperado por termos, entrega estruturada com fontes/hipóteses/próximos passos, feedback e conversão explícita em tarefas.
3. **Rotinas:** catálogo de usos e recorrência diária opcional; servidor aberto para disparar; somente produz rascunhos, com limite diário de chamadas.
4. **Laboratório LOOP-R:** candidato por feedback, comparação A/B nos mesmos três casos reservados, verificações estruturais transparentes, revisão humana obrigatória, promoção e rollback. Resultados estruturais não comprovam qualidade semântica nem ganho de negócio.
5. **Distribuição:** demo no Pages, guia PT/EN/ES, instalação com um comando, publicação no portal, busca e PRO via git.

## Casos de uso
| Público | Rotinas | Revisão humana |
|---|---|---|
| Pessoa física | Planejar a semana, estudar, organizar uma decisão | Prioridades, agenda e fatos |
| Independente | Proposta, entrega, follow-up | Escopo, preço informado, tom e destinatário |
| Pequena empresa | Atendimento, reunião, procedimento | Políticas, responsáveis, compromisso com cliente |

## Arquitetura e dados
Navegador → API local same-origin → serviços → SQLite. OpenRouter recebe somente solicitação, perfil, instrução ativa e até cinco memórias relevantes. Histórico não é enviado integralmente. API pública de terceiros só é chamada no servidor. Banco em ~/.local/share/rsi-copiloto, fora da pasta publicada; backup baixado contém dados do usuário. API local só em loopback, controle de Origin/Host e token de sessão. Uma instância = um operador; não é serviço multiusuário.

## Critérios de aceite
Testes de validação, persistência, promoção/reversão, controle de chamadas, isolamento de contexto, HTTP, scheduler; smoke com provedor real; navegação desktop/mobile, fluxo de tarefa e memória, execução e exportação; Pages respondendo; pushes confirmados no origin.

## Limites e expansão
Integrações Gmail, WhatsApp, calendário externo, ERP e permissões por organização não estão implementadas. Próxima etapa: adaptadores por serviço e autorização, autenticação multiusuário, filas distribuídas, avaliação semântica e conjuntos de teste próprios. Não confundir exportar .ics com sincronização de calendário.
