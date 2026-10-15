# Execução dos trechos de código da dissertação

## Simulador de juros (Código 1)

| Caso | Entrada | Versão anterior | Versão corrigida |
|---|---|---|---|
| Valores típicos | C='1000', i='1', n='12' | Montante Final: R$ 1126.83 | Montante final: R$ 1.126,83 |
| Taxa com vírgula decimal | C='1000', i='1,5', n='12' | Erro: Introduza apenas numeros. | Montante final: R$ 1.195,62 |
| Capital com ponto de milhar | C='1.000', i='1', n='12' | Montante Final: R$ 1.13 | Montante final: R$ 1.126,83 |
| Capital negativo | C='-1000', i='1', n='12' | Montante Final: R$ -1126.83 | Mensagem de orientação (números não negativos, meses inteiros, exemplos) |
| Taxa negativa | C='1000', i='-5', n='12' | Montante Final: R$ 540.36 | Mensagem de orientação (números não negativos, meses inteiros, exemplos) |
| Tempo zero | C='1000', i='1', n='0' | Montante Final: R$ 1000.00 | Montante final: R$ 1.000,00 |
| Taxa zero | C='1000', i='0', n='12' | Montante Final: R$ 1000.00 | Montante final: R$ 1.000,00 |
| Tempo não inteiro | C='1000', i='1', n='12,5' | Erro: Introduza apenas numeros. | Mensagem de orientação (números não negativos, meses inteiros, exemplos) |
| Campo vazio | C='', i='1', n='12' | Preencha todos os campos. | Preencha os três campos. |

## Persistência (Código 2)

| Cenário | Versão anterior | Versão corrigida |
|---|---|---|
| Salvar o perfil e reabrir | salvar: ok; reabrir: exceção NameError | salvar: ok; reabrir: ok; dados recuperados |
| Primeiro uso, sem arquivo salvo | exceção NameError | ok; valores padrão definidos |
| Arquivo de dados corrompido | exceção NameError; com os importado: erro silenciado e nenhum atributo definido | ok; valores padrão e aviso ao estudante |
| Falha na gravação | sem aviso ao estudante; erro só no console (print) | retornou False; aviso ao estudante |
