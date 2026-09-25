| data | o que quebrou | menor correção | prompt ou infra |
| 2026-09-25 | Blocos de código do template de guia alargavam o grid em 360px | Aplicar min-width:0 aos filhos de grid e step; manter scroll dentro do pre | infra |
| 2026-09-25 | Inserção no portal buscou array sem anotação TypeScript | Localizar declaração tipada real antes de inserir; validação interrompeu sem alterar arquivos | infra |
| 2026-09-25 | Teste de importação consultava toast antes de terminar a leitura assíncrona do arquivo | Esperar a mensagem correspondente antes de validar o resultado | infra |
| 2026-09-25 | Restauração aceitava objetos incompletos que poderiam quebrar a tela | Validar campos e estruturas aninhadas antes de substituir dados; preservar estado em erro | infra |
| 2026-09-25 | Metadados da navegação ficavam abaixo de 11px no celular | Ajustar piso tipográfico e posicionar seletor em linha própria | infra |
| 2026-09-25 | Avaliação com contexto isolado poderia persistir estado sem memórias se a API falhasse | Isolar somente o payload da chamada, mantendo o estado canônico intacto; teste de regressão | infra |
