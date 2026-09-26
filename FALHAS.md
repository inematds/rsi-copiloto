| 2026-09-26 | Bump de versão atualizou também a descrição histórica do serviço e dos testes reais | Separar validação histórica v1.1.0 de testes locais e publicação v1.2.0; não afirmar reinício nem smoke novo | prompt |
| data | o que quebrou | menor correção | prompt ou infra |
| 2026-09-26 | Tradução DOM repetia escritas idênticas em ES e travava a interface ao trocar de idioma | Só gravar texto/opção quando o valor traduzido diferir do atual | prompt |
| 2026-09-26 | Tradução DOM repetia escritas idênticas em ES e travava a interface ao trocar de idioma | Só gravar texto/opção quando o valor traduzido diferir do atual | prompt |
| 2026-09-25 | A entrega inicial terminava em rascunho/memória e não continuava a missão após aprovação, deixando LOOP-R desconectado | Adicionar estado de missão e ligar avaliações ao laboratório existente, preservando o motor e os dados | prompt |
| 2026-09-25 | IA tratou referência a etapa anterior como fonte de memória no smoke de missões | Informar lista exata de IDs permitidos e excluir referências internas; manter rejeição de fontes inventadas | prompt |
| 2026-09-25 | Teste mobile esperou texto da versão em elemento oculto da barra lateral | Aguardar versão ativa persistida em vez de visibilidade de elemento desktop | infra |
| 2026-09-25 | Primeiro Actions executou antes de habilitar Pages no repo novo | Habilitar build_type=workflow na API e repetir a execução falha | infra |
| 2026-09-25 | Blocos de código do template de guia alargavam o grid em 360px | Aplicar min-width:0 aos filhos de grid e step; manter scroll dentro do pre | infra |
| 2026-09-25 | Inserção no portal buscou array sem anotação TypeScript | Localizar declaração tipada real antes de inserir; validação interrompeu sem alterar arquivos | infra |
| 2026-09-25 | Teste de importação consultava toast antes de terminar a leitura assíncrona do arquivo | Esperar a mensagem correspondente antes de validar o resultado | infra |
| 2026-09-25 | Restauração aceitava objetos incompletos que poderiam quebrar a tela | Validar campos e estruturas aninhadas antes de substituir dados; preservar estado em erro | infra |
| 2026-09-25 | Metadados da navegação ficavam abaixo de 11px no celular | Ajustar piso tipográfico e posicionar seletor em linha própria | infra |
| 2026-09-25 | Avaliação com contexto isolado poderia persistir estado sem memórias se a API falhasse | Isolar somente o payload da chamada, mantendo o estado canônico intacto; teste de regressão | infra |
