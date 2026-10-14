# Registro da conferência dos cálculos — AlgoFin

Gerado em 2026-10-14 por `conferir_calculos.py` (Python 3.13.16, Linux).
Valores analíticos calculados em aritmética racional exata (`fractions.Fraction`).

## 1. Tabela 7 da dissertação (SAC, PV = 10.000, i = 1% a.m., n = 120)

| k | valor exato | arredondado (2 casas) | impresso na dissertação | situação | E_r do float interno | E_r do valor impresso |
|---|---|---|---|---|---|---|
| 1 | 183.333333 | 183,33 | 183,33 | confere | 1.0e-16 | 1.8e-05 |
| 60 | 134.166667 | 134,17 | 134,16 | DIVERGE (truncado) | 7.1e-17 | 5.0e-05 |
| 120 | 84.166667 | 84,17 | 84,16 | DIVERGE (truncado) | 1.1e-16 | 7.9e-05 |
| Total de juros | 6050.000000 | 6050,00 | 6050,00 | confere | 6.0e-16 | 0 |

* Maior erro relativo float × exato nas 120 prestações: **8.2e-16** (a dissertação afirma 'menor que 10^-12'; o correto é da ordem de 10^-16, próximo ao épsilon da máquina, 2,2e-16).
* Saldo devedor final calculado em float: -8.810729923425242e-13. O valor exato é 0, logo o erro relativo é indefinido; erro absoluto = 8.8e-13.
* Total de juros em float: 6049.999999999996 (E_r = 6.0e-16). A dissertação registra E_r = 0,0000; o valor impresso está correto, mas o erro não é exatamente zero.
* **Diagnóstico:** os valores 134,16 e 84,16 são truncamentos de 134,1666… e 84,1666…. Arredondados corretamente, são 134,17 e 84,17. Os erros relativos da coluna 'E_r' da Tabela 7 não correspondem aos valores impressos: o erro do valor impresso é ~5e-5, não <1e-12.
* Na convenção de contratos (centavos + ajuste na última parcela) a amortização fica 83,33 e a última prestação é **84,57**, com total de juros **6050,24**. Por isso a dissertação precisa declarar qual convenção adota.

## 2. Sistema Price (PV = 10.000, i = 1% a.m., n = 120)

* Prestação: PMT = 143.4709484026 → **R$ 143,47** (exibida).
* Total de juros (exato): 7216.513808 → **R$ 7216,51**; em float: 7216.513808310482.
* Convenção de centavos: última prestação **R$ 143,68**, total de juros **R$ 7216,61**.
* Maior E_r float × exato: prestações 4.6e-16; juros 1.6e-14 (o juro do último mês é pequeno, ~1,42, e o erro relativo cresce quando o valor exato é pequeno).
* Saldo final em float: 2.3590018827235326e-12 (exato 0; erro absoluto 2.4e-12).
* Propriedade verificada: A_k = A_1 (1+i)^(k-1) (amortizações em PG), ver testes.

| k | juros | amortização | prestação | saldo final |
|---|---|---|---|---|
| 1 | 100,00 | 43,47 | 143,47 | 9956,53 |
| 2 | 99,57 | 43,91 | 143,47 | 9912,62 |
| 60 | 65,28 | 78,19 | 143,47 | 6449,74 |
| 119 | 2,83 | 140,64 | 143,47 | 142,05 |
| 120 | 1,42 | 142,05 | 143,47 | 0,00 |

**SAC × Price no mesmo cenário:** primeira prestação 183,33 × 143,47; última 84,17 × 143,47; total de juros 6050,00 × 7216,51 (diferença 1166,51).

## 3. Efeito da convenção de arredondamento (cenário C1)

| Sistema | Convenção | 1ª prestação | 60ª prestação | última prestação | total de juros |
|---|---|---|---|---|---|
| SAC | exata, exibida com 2 casas | 183,33 | 134,17 | 84,17 | 6050,00 |
| SAC | truncamento na exibição | 183,33 | 134,16 | 84,16 | 6049,99 |
| SAC | centavos por parcela + ajuste final | 183,33 | 134,17 | 84,57 | 6050,24 |
| Price | exata, exibida com 2 casas | 143,47 | 143,47 | 143,47 | 7216,51 |
| Price | truncamento na exibição | 143,47 | 143,47 | 143,47 | 7216,51 |
| Price | centavos por parcela + ajuste final | 143,47 | 143,47 | 143,68 | 7216,61 |

Conclusão: diferenças de 1 centavo (truncar × arredondar) e de dezenas de centavos na última parcela (ajuste) não são erros de modelo, mas de convenção. A dissertação deve fixar uma convenção e o app deve segui-la em todas as telas.

## 4. Casos especiais e demais modelos

| Caso | Esperado | Obtido (referência) | Situação |
|---|---|---|---|
| SAC com i = 0: prestação constante = PV/n | 83,33 (todas) | 83,33 / juros 0,00 | OK |
| Price com i = 0: PMT = PV/n (limite) | 83,33; juros 0 | 83,33; juros 0,00 | OK |
| n = 1 (SAC e Price coincidem) | 1010,00 | 1010,00 e 1010,00 | OK |
| SAC: juros em PA de razão -i·PV/n (C1) | -0,833333… | -0,833333 | OK |
| SAC: total de juros = i·PV·(n+1)/2 (C1) | 6050,00 | 6050,00 | OK |
| Price: total de juros = n·PMT − PV (C1) | 7216,51 | 7216,51 | OK |
| Juros compostos: laço (Código 1) × fórmula, C=1000, i=1%, n=12 | 1126,825030 | 1126.8250301319695 (E_r 2.2e-16) | OK |
| Juros compostos com n = 0 | 1000,00 | 1000,00 | OK |
| Juros simples C=1000, i=1%, n=12 | 1120,00 | 1120,00 | OK |
| Aportes: recorrência = fórmula fechada (M0=0, A=100, i=1%, n=12) | 1268,250301 | 1268,250301 | OK |
| Aportes com i = 0: M_n = M0 + nA | 1200,00 | 1200,00 | OK |
| Taxa equivalente: 1% a.m. → a.a. | 12,6825% | 12,6825% | OK |
| Taxa equivalente: 12% a.a. → a.m. | 0,9489% | 0,9489% | OK |
| Tempo para dobrar a 1% a.m. | 70 meses | 70 | OK |
| Figura 8: R$ 1000 na gaveta, inflação 5% | perda 47,62 (preços iniciais) / falta 50,00 (preços finais) | 47,62 / 50,00 | OK |
| Figura 7: mesada 150, gasto 20, meta 650 | 5 meses | 5 | OK |
| Poupança com meta não divisível (150, 20, 700) | 6 meses (arredondar para cima) | 6 | OK |
| Poupança com gasto = mesada | erro tratado (meta inatingível) | ValueError tratado | OK |
| Entrada '1,5' com float() puro (Código 1) | ValueError → mensagem de erro ao aluno | ValueError | OK |
| Entrada '1,5' com ler_numero_br() | 1,5 | 1,5 | OK |
| Formatação f'{x:.2f}' para 1234.5 | R$ 1.234,50 (padrão brasileiro) | 1234.50 (Código 1) × R$ 1.234,50 | OK |

## 4b. Exemplo conferível à mão (PV = 1.200, i = 2% a.m., n = 6)

| k | SAC J | SAC P | Price J | Price A | Price P | Price SD |
|---|---|---|---|---|---|---|
| 1 | 24,00 | 224,00 | 24,00 | 190,23 | 214,23 | 1009,77 |
| 2 | 20,00 | 220,00 | 20,20 | 194,04 | 214,23 | 815,73 |
| 3 | 16,00 | 216,00 | 16,31 | 197,92 | 214,23 | 617,82 |
| 4 | 12,00 | 212,00 | 12,36 | 201,87 | 214,23 | 415,94 |
| 5 | 8,00 | 208,00 | 8,32 | 205,91 | 214,23 | 210,03 |
| 6 | 4,00 | 204,00 | 4,20 | 210,03 | 214,23 | 0,00 |
| total | 84,00 | 1284,00 | 85,39 | 1200,00 | 1285,39 | |

## 4c. Sintomas de erros comuns de implementação (PV = 10.000, i = 1%, n = 120)

Use para localizar a causa de uma divergência observada no app: compare o valor da tela com a coluna 'valor produzido'.

| Sistema | Implementação | valor produzido (1ª prestação / PMT) | total de juros | última / observação |
|---|---|---|---|---|
| Price | correto | 143,47 | 7216,51 |  |
| Price | taxa em % não convertida (i = 1) | 10000,00 | — |  |
| Price | taxa convertida duas vezes (i = 0,0001) | 83,84 | — |  |
| Price | expoente positivo: PV·i/[1−(1+i)^n] | -43,47 | — |  |
| Price | PV(1+i)^n/n (montante dividido em n) | 275,03 | — |  |
| Price | PV(1+in)/n (juros simples) | 183,33 | — |  |
| Price | taxa anual 12% usada como mensal | 1200,00 | — |  |
| SAC | correto | 183,33 | 6050,00 | 84,17 |
| SAC | juros sempre sobre PV | 183,33 | 12000,00 | 183,33 |
| SAC | juros sobre o saldo já amortizado | 182,50 | 5950,00 | 83,33 |
| SAC | laço range(1, n): 119 prestações, saldo final ≠ 0 | 183,33 | 6049,17 | saldo 83.33 |

## 5. Arquivos gerados

* `saida/C1_Price_PV10000_i0.01_n120.csv`
* `saida/C1_SAC_PV10000_i0.01_n120.csv`
* `saida/C2_Price_PV1200_i0.02_n6.csv`
* `saida/C2_SAC_PV1200_i0.02_n6.csv`
* `saida/C3_Price_PV10000_i0_n120.csv`
* `saida/C3_SAC_PV10000_i0_n120.csv`
* `saida/C4_Price_PV1000_i0.01_n1.csv`
* `saida/C4_SAC_PV1000_i0.01_n1.csv`
* `saida/C5_Price_PV5000_i0.015_n24.csv`
* `saida/C5_SAC_PV5000_i0.015_n24.csv`
* `saida/ficha_conferencia_app.csv`
* `saida/tabelas_latex/tab_casos_especiais.tex`
* `saida/tabelas_latex/tab_convencoes_arredondamento.tex`
* `saida/tabelas_latex/tab_execucao_trechos.tex`
* `saida/tabelas_latex/tab_exemplo_c2.tex`
* `saida/tabelas_latex/tab_ficha_app.tex`
* `saida/tabelas_latex/tab_price_validacao.tex`
* `saida/tabelas_latex/tab_sac_validacao.tex`
* `saida/tabelas_latex/tab_sintomas.tex`

**Resultado:** 21 de 21 casos conferem com a referência.

Observação: 'Entrada 1,5 com float() puro' é marcada OK porque o teste confirma o defeito esperado (o Código 1 rejeita vírgula decimal). A correção recomendada é usar ler_numero_br().
