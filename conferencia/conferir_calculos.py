r"""
conferir_calculos.py — Gera o registro reprodutível da conferência dos cálculos.

Uso:   python3 conferir_calculos.py
Saída: pasta ./saida com
         - tabelas completas em CSV (abrem no Excel/LibreOffice, separador ';')
         - tabelas LaTeX prontas para \input{} na dissertação (saida/tabelas_latex)
         - relatorio_conferencia.md com todos os números e o diagnóstico

Depende apenas da biblioteca padrão do Python (3.8+).
"""
from __future__ import annotations

import csv
import math
import os
import platform
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from motor_referencia import (
    arredonda_centavo, trunca_centavo, erro_relativo, erro_absoluto,
    juros_simples, juros_compostos_fechado, juros_compostos_iterativo_float,
    serie_aportes_fechado, serie_aportes_recorrencia, taxa_equivalente,
    tempo_para_meta, sac, price, prestacao_price, total_juros,
    meses_para_meta_poupanca, perda_poder_compra, ler_numero_br, formata_brl,
)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
TEX = os.path.join(SAIDA, "tabelas_latex")
os.makedirs(TEX, exist_ok=True)

relatorio: list[str] = []


def r(linha: str = "") -> None:
    relatorio.append(linha)


def _arredonda(x, casas: int) -> Decimal:
    """Arredonda meio para cima (hipótese H6), a partir do valor exato quando
    x é Fraction. Formatar com f'{float(x):.2f}' NÃO serve: o Python arredonda
    os empates para o par (40,625 -> 40,62), e a convenção declarada dá 40,63."""
    if isinstance(x, Fraction):
        d = Decimal(x.numerator) / Decimal(x.denominator)
    elif isinstance(x, Decimal):
        d = x
    else:
        d = Decimal(str(x))
    return d.quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)


def br(x, casas=2) -> str:
    """Número com vírgula decimal, sem separador de milhar (para CSV/relatório)."""
    return f"{_arredonda(x, casas):f}".replace(".", ",")


def brt(x, casas=2) -> str:
    """Número para LaTeX: vírgula decimal e ponto de milhar (6.050,00)."""
    s = f"{_arredonda(x, casas):,.{casas}f}"
    return s.replace(",", "X").replace(".", "{,}").replace("X", ".")


def brl_tex(x) -> str:
    return formata_brl(x).replace("R$ ", "R\\$~")


def sci(x: float) -> str:
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    return f"{m:.1f}".replace(".", "{,}") + f"\\times 10^{{{e}}}"


def sci_md(x: float) -> str:
    return f"{x:.1e}" if x else "0"


# ----------------------------------------------------------------------------
# 1. Tabelas completas em CSV
# ----------------------------------------------------------------------------
CENARIOS = [
    ("C1", 10000, "0.01", 120, "Cenário da Tabela 7 da dissertação"),
    ("C2", 1200, "0.02", 6, "Cenário curto, conferível à mão em sala"),
    ("C3", 10000, "0", 120, "Caso especial i = 0"),
    ("C4", 1000, "0.01", 1, "Caso especial n = 1"),
    ("C5", 5000, "0.015", 24, "Cenário intermediário"),
]


def grava_csv(nome, sistema, pv, i, n):
    fn = sac if sistema == "SAC" else price
    ex, fl, ce = fn(pv, i, n, "exato"), fn(pv, i, n, "float"), fn(pv, i, n, "centavos")
    caminho = os.path.join(SAIDA, f"{nome}_{sistema}_PV{pv}_i{i}_n{n}.csv")
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["k", "saldo_inicial_exato", "juros_exato", "amortizacao_exata",
                    "prestacao_exata", "saldo_final_exato",
                    "prestacao_exibida_2casas", "prestacao_float_python",
                    "erro_relativo_float", "prestacao_conv_centavos",
                    "juros_conv_centavos", "saldo_final_conv_centavos",
                    "VALOR_EXIBIDO_NO_APP", "CONFERE_S_N"])
        for a, b, c in zip(ex, fl, ce):
            er = erro_relativo(a.prestacao, b.prestacao) if a.prestacao != 0 else ""
            w.writerow([a.k, br(a.saldo_inicial, 6), br(a.juros, 6), br(a.amortizacao, 6),
                        br(a.prestacao, 6), br(a.saldo_final, 6),
                        br(arredonda_centavo(a.prestacao)), repr(b.prestacao),
                        f"{er:.2e}" if er != "" else "", br(c.prestacao), br(c.juros),
                        br(c.saldo_final), "", ""])
    return ex, fl, ce, os.path.basename(caminho)


resultados = {}
for nome, pv, i, n, desc in CENARIOS:
    for sistema in ("SAC", "Price"):
        resultados[(nome, sistema)] = grava_csv(nome, sistema, pv, i, n)

# ----------------------------------------------------------------------------
# 2. Diagnóstico da Tabela 7 (SAC, C1)
# ----------------------------------------------------------------------------
ex, fl, ce, _ = resultados[("C1", "SAC")]
DISSERTACAO_T7 = {1: "183.33", 60: "134.16", 120: "84.16"}

r("# Registro da conferência dos cálculos — AlgoFin")
r()
r(f"Gerado em {date.today().isoformat()} por `conferir_calculos.py` "
  f"(Python {platform.python_version()}, {platform.system()}).")
r("Valores analíticos calculados em aritmética racional exata (`fractions.Fraction`).")
r()
r("## 1. Tabela 7 da dissertação (SAC, PV = 10.000, i = 1% a.m., n = 120)")
r()
r("| k | valor exato | arredondado (2 casas) | impresso na dissertação | situação | E_r do float interno | E_r do valor impresso |")
r("|---|---|---|---|---|---|---|")
linhas_t7 = []
for k in (1, 60, 120):
    e = ex[k - 1].prestacao
    f_ = fl[k - 1].prestacao
    impresso = Fraction(DISSERTACAO_T7[k])
    arred = arredonda_centavo(e)
    ok = Fraction(str(arred)) == impresso
    er_float = erro_relativo(e, f_)
    er_impr = erro_relativo(e, impresso)
    situ = "confere" if ok else "DIVERGE (truncado)"
    r(f"| {k} | {float(e):.6f} | {br(arred)} | {DISSERTACAO_T7[k].replace('.', ',')} | {situ} | {sci_md(er_float)} | {sci_md(er_impr)} |")
    linhas_t7.append((k, e, arred, DISSERTACAO_T7[k], ok, er_float, er_impr))

tj_ex, tj_fl, tj_ce = total_juros(ex), total_juros(fl), total_juros(ce)
er_tj = erro_relativo(tj_ex, tj_fl)
r(f"| Total de juros | {float(tj_ex):.6f} | {br(tj_ex)} | 6050,00 | confere | {sci_md(er_tj)} | 0 |")
r()
max_er_sac = max(erro_relativo(a.prestacao, b.prestacao) for a, b in zip(ex, fl))
ea_saldo = erro_absoluto(0, fl[-1].saldo_final)
r(f"* Maior erro relativo float × exato nas 120 prestações: **{sci_md(max_er_sac)}** "
  f"(a dissertação afirma 'menor que 10^-12'; o correto é da ordem de 10^-16, "
  f"próximo ao épsilon da máquina, 2,2e-16).")
r(f"* Saldo devedor final calculado em float: {fl[-1].saldo_final!r}. O valor exato é 0, "
  f"logo o erro relativo é indefinido; erro absoluto = {sci_md(ea_saldo)}.")
r(f"* Total de juros em float: {tj_fl!r} (E_r = {sci_md(er_tj)}). A dissertação registra "
  f"E_r = 0,0000; o valor impresso está correto, mas o erro não é exatamente zero.")
r("* **Diagnóstico:** os valores 134,16 e 84,16 são truncamentos de 134,1666… e 84,1666…. "
  "Arredondados corretamente, são 134,17 e 84,17. Os erros relativos da coluna 'E_r' da Tabela 7 "
  "não correspondem aos valores impressos: o erro do valor impresso é ~5e-5, não <1e-12.")
r(f"* Na convenção de contratos (centavos + ajuste na última parcela) a amortização fica "
  f"83,33 e a última prestação é **{br(ce[-1].prestacao)}**, com total de juros "
  f"**{br(tj_ce)}**. Por isso a dissertação precisa declarar qual convenção adota.")
r()

# LaTeX — Tabela 7 revisada
with open(os.path.join(TEX, "tab_sac_validacao.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{table}[htbp]\n\\centering\n\\small\n")
    f.write("\\caption{Validação do algoritmo SAC ($PV=10\\,000$; $i=0{,}01$; $n=120$): "
            "valor exato, valor exibido e erro relativo da implementação em ponto flutuante}\n")
    f.write("\\label{tab:sac-validacao}\n")
    f.write("\\begin{tabular}{@{}lrrrc@{}}\n\\toprule\n")
    f.write("Mês ($k$) & $P_k$ exato & Exibido (2 casas) & $E_r$ (float $\\times$ exato) & Confere \\\\\n\\midrule\n")
    for k, e, arred, _, _, er_float, _ in linhas_t7:
        f.write(f"{k} & {brt(e, 6)} & R\\$~{brt(arred)} & ${sci(er_float)}$ & sim \\\\\n")
    f.write(f"Total de juros & {brt(tj_ex, 6)} & R\\$~{brt(tj_ex)} & ${sci(er_tj)}$ & sim \\\\\n")
    f.write("\\midrule\n")
    f.write(f"\\multicolumn{{3}}{{@{{}}l}}{{Maior $E_r$ nas 120 prestações}} & ${sci(max_er_sac)}$ & \\\\\n")
    f.write(f"\\multicolumn{{3}}{{@{{}}l}}{{Saldo final (exato $=0$): erro absoluto}} & ${sci(ea_saldo)}$ & \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
    f.write("\\par\\smallskip\\footnotesize Fonte: Elaborada pelo autor (2026), a partir do script "
            "\\texttt{conferir\\_calculos.py} (Apêndice~\\ref{ap:registro}). Valores exatos em aritmética "
            "racional; exibição arredondada ao centavo (meio para cima).\n")
    f.write("\\end{table}\n")

# ----------------------------------------------------------------------------
# 3. Price (C1)
# ----------------------------------------------------------------------------
pex, pfl, pce, _ = resultados[("C1", "Price")]
pmt = prestacao_price(10000, "0.01", 120)
ptj_ex, ptj_fl, ptj_ce = total_juros(pex), total_juros(pfl), total_juros(pce)
max_er_price = max(erro_relativo(a.prestacao, b.prestacao) for a, b in zip(pex, pfl))
max_er_price_j = max(erro_relativo(a.juros, b.juros) for a, b in zip(pex, pfl))
r("## 2. Sistema Price (PV = 10.000, i = 1% a.m., n = 120)")
r()
r(f"* Prestação: PMT = {float(pmt):.10f} → **R$ {br(pmt)}** (exibida).")
r(f"* Total de juros (exato): {float(ptj_ex):.6f} → **R$ {br(ptj_ex)}**; em float: {ptj_fl!r}.")
r(f"* Convenção de centavos: última prestação **R$ {br(pce[-1].prestacao)}**, total de juros **R$ {br(ptj_ce)}**.")
r(f"* Maior E_r float × exato: prestações {sci_md(max_er_price)}; juros {sci_md(max_er_price_j)} "
  f"(o juro do último mês é pequeno, ~1,42, e o erro relativo cresce quando o valor exato é pequeno).")
r(f"* Saldo final em float: {pfl[-1].saldo_final!r} (exato 0; erro absoluto {sci_md(abs(pfl[-1].saldo_final))}).")
r("* Propriedade verificada: A_k = A_1 (1+i)^(k-1) (amortizações em PG), ver testes.")
r()
r("| k | juros | amortização | prestação | saldo final |")
r("|---|---|---|---|---|")
for k in (1, 2, 60, 119, 120):
    l = pex[k - 1]
    r(f"| {k} | {br(l.juros)} | {br(l.amortizacao)} | {br(l.prestacao)} | {br(l.saldo_final)} |")
r()
r("**SAC × Price no mesmo cenário:** primeira prestação 183,33 × 143,47; última 84,17 × 143,47; "
  f"total de juros {br(tj_ex)} × {br(ptj_ex)} (diferença {br(ptj_ex - tj_ex)}).")
r()

with open(os.path.join(TEX, "tab_price_validacao.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{table}[htbp]\n\\centering\n\\small\n")
    f.write("\\caption{Sistema Price ($PV=10\\,000$; $i=0{,}01$; $n=120$): linhas selecionadas da tabela "
            "exata e erro relativo da implementação em ponto flutuante}\n\\label{tab:price-validacao}\n")
    f.write("\\begin{tabular}{@{}lrrrr@{}}\n\\toprule\n")
    f.write("Mês ($k$) & Juros $J_k$ & Amortização $A_k$ & Prestação & Saldo $SD_k$ \\\\\n\\midrule\n")
    for k in (1, 2, 60, 119, 120):
        l = pex[k - 1]
        f.write(f"{k} & {brt(l.juros)} & {brt(l.amortizacao)} & {brt(l.prestacao)} & {brt(l.saldo_final)} \\\\\n")
    f.write(f"Total & {brt(ptj_ex)} & {brt(10000)} & {brt(pmt * 120)} & \\\\\n\\midrule\n")
    f.write(f"\\multicolumn{{4}}{{@{{}}l}}{{Maior $E_r$ nas prestações (float $\\times$ exato)}} & ${sci(max_er_price)}$ \\\\\n")
    f.write(f"\\multicolumn{{4}}{{@{{}}l}}{{Maior $E_r$ nos juros (float $\\times$ exato)}} & ${sci(max_er_price_j)}$ \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
    f.write("\\par\\smallskip\\footnotesize Fonte: Elaborada pelo autor (2026). Valores em reais, "
            "arredondados ao centavo apenas na exibição.\n\\end{table}\n")

# ----------------------------------------------------------------------------
# 4. Convenções de arredondamento (por que valores "divergem")
# ----------------------------------------------------------------------------
r("## 3. Efeito da convenção de arredondamento (cenário C1)")
r()
r("| Sistema | Convenção | 1ª prestação | 60ª prestação | última prestação | total de juros |")
r("|---|---|---|---|---|---|")
conv_rows = []
for sistema, (e_, f_, c_, _) in (("SAC", resultados[("C1", "SAC")]), ("Price", resultados[("C1", "Price")])):
    linhas = [
        ("exata, exibida com 2 casas", [arredonda_centavo(e_[k].prestacao) for k in (0, 59, 119)], arredonda_centavo(total_juros(e_))),
        ("truncamento na exibição", [trunca_centavo(f_[k].prestacao) for k in (0, 59, 119)], trunca_centavo(total_juros(f_))),
        ("centavos por parcela + ajuste final", [c_[k].prestacao for k in (0, 59, 119)], total_juros(c_)),
    ]
    for nome_c, ps, tj in linhas:
        r(f"| {sistema} | {nome_c} | {br(ps[0])} | {br(ps[1])} | {br(ps[2])} | {br(tj)} |")
        conv_rows.append((sistema, nome_c, ps, tj))
r()
r("Conclusão: diferenças de 1 centavo (truncar × arredondar) e de dezenas de centavos na última parcela "
  "(ajuste) não são erros de modelo, mas de convenção. A dissertação deve fixar uma convenção e o app "
  "deve segui-la em todas as telas.")
r()
with open(os.path.join(TEX, "tab_convencoes_arredondamento.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{table}[htbp]\n\\centering\n\\small\n")
    f.write("\\caption{Efeito da convenção de arredondamento nos valores exibidos ($PV=10\\,000$; $i=0{,}01$; $n=120$)}\n")
    f.write("\\label{tab:convencoes}\n\\begin{tabular}{@{}llrrrr@{}}\n\\toprule\n")
    f.write("Sistema & Convenção & $P_1$ & $P_{60}$ & $P_{120}$ & Juros totais \\\\\n\\midrule\n")
    for sistema, nome_c, ps, tj in conv_rows:
        f.write(f"{sistema} & {nome_c} & {brt(ps[0])} & {brt(ps[1])} & {brt(ps[2])} & {brt(tj)} \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n\\par\\smallskip\\footnotesize Fonte: Elaborada pelo autor (2026).\n\\end{table}\n")

# ----------------------------------------------------------------------------
# 5. Casos especiais e demais modelos
# ----------------------------------------------------------------------------
r("## 4. Casos especiais e demais modelos")
r()
casos = []

def caso(descr, esperado, obtido, ok):
    casos.append((descr, esperado, obtido, ok))
    r(f"| {descr} | {esperado} | {obtido} | {'OK' if ok else 'FALHA'} |")

r("| Caso | Esperado | Obtido (referência) | Situação |")
r("|---|---|---|---|")
s0 = sac(10000, "0", 120)
caso("SAC com i = 0: prestação constante = PV/n", "83,33 (todas)", br(s0[0].prestacao) + " / juros " + br(total_juros(s0)),
     all(l.prestacao == s0[0].prestacao for l in s0) and total_juros(s0) == 0)
p0 = price(10000, "0", 120)
caso("Price com i = 0: PMT = PV/n (limite)", "83,33; juros 0", br(p0[0].prestacao) + "; juros " + br(total_juros(p0)),
     p0[0].prestacao == Fraction(10000, 120) and total_juros(p0) == 0)
s1, p1 = sac(1000, "0.01", 1), price(1000, "0.01", 1)
caso("n = 1 (SAC e Price coincidem)", "1010,00", f"{br(s1[0].prestacao)} e {br(p1[0].prestacao)}",
     s1[0].prestacao == p1[0].prestacao == 1010)
caso("SAC: juros em PA de razão -i·PV/n (C1)", "-0,833333…", br(ex[1].juros - ex[0].juros, 6),
     all(ex[k + 1].juros - ex[k].juros == -Fraction(1, 100) * Fraction(10000, 120) for k in range(119)))
caso("SAC: total de juros = i·PV·(n+1)/2 (C1)", "6050,00", br(tj_ex), tj_ex == Fraction(1, 100) * 10000 * 121 / 2)
caso("Price: total de juros = n·PMT − PV (C1)", br(pmt * 120 - 10000), br(ptj_ex), ptj_ex == pmt * 120 - 10000)
mf = juros_compostos_fechado(1000, "0.01", 12)
mi = juros_compostos_iterativo_float(1000, 0.01, 12)
caso("Juros compostos: laço (Código 1) × fórmula, C=1000, i=1%, n=12", br(mf, 6), f"{mi!r} (E_r {sci_md(erro_relativo(mf, mi))})",
     erro_relativo(mf, mi) < 1e-14)
caso("Juros compostos com n = 0", "1000,00", br(juros_compostos_fechado(1000, "0.01", 0)), juros_compostos_fechado(1000, "0.01", 0) == 1000)
caso("Juros simples C=1000, i=1%, n=12", "1120,00", br(juros_simples(1000, "0.01", 12)), juros_simples(1000, "0.01", 12) == 1120)
ma, mr = serie_aportes_fechado(0, "0.01", 100, 12), serie_aportes_recorrencia(0, "0.01", 100, 12)
caso("Aportes: recorrência = fórmula fechada (M0=0, A=100, i=1%, n=12)", br(ma, 6), br(mr, 6), ma == mr)
caso("Aportes com i = 0: M_n = M0 + nA", "1200,00", br(serie_aportes_fechado(0, "0", 100, 12)),
     serie_aportes_fechado(0, "0", 100, 12) == 1200 == serie_aportes_recorrencia(0, "0", 100, 12))
caso("Taxa equivalente: 1% a.m. → a.a.", "12,6825%", br(taxa_equivalente(0.01, 12) * 100, 4) + "%",
     abs(taxa_equivalente(0.01, 12) - 0.126825030131969) < 1e-12)
caso("Taxa equivalente: 12% a.a. → a.m.", "0,9489%", br(taxa_equivalente(0.12, Fraction(1, 12)) * 100, 4) + "%",
     abs(taxa_equivalente(0.12, Fraction(1, 12)) - 0.009488792934583) < 1e-12)
caso("Tempo para dobrar a 1% a.m.", "70 meses", str(tempo_para_meta(1000, "0.01", 2000)), tempo_para_meta(1000, "0.01", 2000) == 70)
perda_ini, falta_fim = perda_poder_compra(1000, "0.05")
caso("Figura 8: R$ 1000 na gaveta, inflação 5%", "perda 47,62 (preços iniciais) / falta 50,00 (preços finais)",
     f"{br(perda_ini)} / {br(falta_fim)}", round(float(perda_ini), 2) == 47.62 and falta_fim == 50)
caso("Figura 7: mesada 150, gasto 20, meta 650", "5 meses", str(meses_para_meta_poupanca(150, 20, 650)), meses_para_meta_poupanca(150, 20, 650) == 5)
caso("Poupança com meta não divisível (150, 20, 700)", "6 meses (arredondar para cima)", str(meses_para_meta_poupanca(150, 20, 700)),
     meses_para_meta_poupanca(150, 20, 700) == 6)
try:
    meses_para_meta_poupanca(100, 100, 650)
    caso("Poupança com gasto = mesada", "erro tratado (meta inatingível)", "nenhum erro", False)
except ValueError:
    caso("Poupança com gasto = mesada", "erro tratado (meta inatingível)", "ValueError tratado", True)
try:
    float("1,5")
    ok_virg = False
except ValueError:
    ok_virg = True
caso("Entrada '1,5' com float() puro (Código 1)", "ValueError → mensagem de erro ao aluno", "ValueError" if ok_virg else "aceito", ok_virg)
caso("Entrada '1,5' com ler_numero_br()", "1,5", br(ler_numero_br("1,5"), 1), ler_numero_br("1,5") == 1.5)
caso("Formatação f'{x:.2f}' para 1234.5", "R$ 1.234,50 (padrão brasileiro)", f"{1234.5:.2f} (Código 1) × {formata_brl(1234.5)}", formata_brl(1234.5) == "R$ 1.234,50")
r()

with open(os.path.join(TEX, "tab_casos_especiais.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{longtable}{@{}L{0.40\\textwidth}L{0.20\\textwidth}L{0.20\\textwidth}c@{}}\n")
    f.write("\\caption{Casos especiais e propriedades verificadas pela implementação de referência}\\label{tab:casos-especiais}\\\\\n")
    f.write("\\toprule\nCaso & Esperado & Obtido & Situação \\\\\n\\midrule\n\\endfirsthead\n")
    f.write("\\toprule\nCaso & Esperado & Obtido & Situação \\\\\n\\midrule\n\\endhead\n")
    def esc(s):
        return (str(s).replace("\\", "\\textbackslash{}").replace("%", "\\%").replace("$", "\\$")
                .replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&")
                .replace("textbackslash\\{\\}", "textbackslash{}").replace("→", "$\\to$")
                .replace("×", "$\\times$").replace("−", "$-$").replace("·", "$\\cdot$").replace("…", "\\ldots{}"))
    # Na dissertação, as remissões a figuras e códigos usam \\ref (a numeração muda com o texto)
    REMISSOES = [
        ("laço (Código 1)", "laço (Código~\\ref{lst:mvc})"),
        ("Entrada '1,5' com float() puro (Código 1)",
         "Entrada ``1,5'' lida com \\texttt{float()}, como na versão anterior do Código~\\ref{lst:mvc}"),
        ("Entrada '1,5' com ler\\_numero\\_br()", "Entrada ``1,5'' lida com \\texttt{ler\\_numero\\_br()}"),
        ("Formatação f'\\{x:.2f\\}' para 1234.5", "Formatação de 1234,5 com o especificador \\texttt{.2f}"),
        ("1234.50 (Código 1)", "1234.50 (versão anterior)"),
        ("Figura 8:", "Problema da Figura~\\ref{fig:modulo4}:"),
        ("Figura 7:", "Missão da Figura~\\ref{fig:modulo_poupa}:"),
    ]
    for descr, esp, obt, ok in casos:
        linha = f"{esc(descr)} & {esc(esp)} & {esc(obt)} & {'OK' if ok else 'FALHA'} \\\\\n"
        for a, b in REMISSOES:
            linha = linha.replace(a, b)
        f.write(linha)
    f.write("\\bottomrule\n\\end{longtable}\n")

# ----------------------------------------------------------------------------
# 5b. Exemplo conferível à mão (C2): tabelas completas SAC e Price
# ----------------------------------------------------------------------------
sac_c2, _, _, _ = resultados[("C2", "SAC")]
pri_c2, _, _, _ = resultados[("C2", "Price")]
with open(os.path.join(TEX, "tab_exemplo_c2.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{table}[htbp]\n\\centering\n\\small\n")
    f.write("\\caption{Exemplo verificado à mão: $PV=1\\,200$; $i=2\\%$ a.m.; $n=6$ (valores em reais)}\n")
    f.write("\\label{tab:exemplo-c2}\n\\begin{tabular}{@{}c rrrr c rrrr@{}}\n\\toprule\n")
    f.write(" & \\multicolumn{4}{c}{SAC} & & \\multicolumn{4}{c}{Price} \\\\\n")
    f.write("\\cmidrule{2-5}\\cmidrule{7-10}\n")
    f.write("$k$ & $J_k$ & $A_k$ & $P_k$ & $SD_k$ & & $J_k$ & $A_k$ & $P_k$ & $SD_k$ \\\\\n\\midrule\n")
    for a, b in zip(sac_c2, pri_c2):
        f.write(f"{a.k} & {brt(a.juros)} & {brt(a.amortizacao)} & {brt(a.prestacao)} & {brt(a.saldo_final)} & & "
                f"{brt(b.juros)} & {brt(b.amortizacao)} & {brt(b.prestacao)} & {brt(b.saldo_final)} \\\\\n")
    f.write("\\midrule\n")
    f.write(f"Total & {brt(total_juros(sac_c2))} & {brt(1200)} & {brt(sum(l.prestacao for l in sac_c2))} & & & "
            f"{brt(total_juros(pri_c2))} & {brt(1200)} & {brt(sum(l.prestacao for l in pri_c2))} & \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
    f.write("\\par\\smallskip\\footnotesize Fonte: Elaborada pelo autor (2026). Na coluna Price, valores exatos "
            "exibidos com duas casas; a soma das prestações exibidas pode diferir em centavos da soma exata.\n")
    f.write("\\end{table}\n")
r("## 4b. Exemplo conferível à mão (PV = 1.200, i = 2% a.m., n = 6)")
r()
r("| k | SAC J | SAC P | Price J | Price A | Price P | Price SD |")
r("|---|---|---|---|---|---|---|")
for a, b in zip(sac_c2, pri_c2):
    r(f"| {a.k} | {br(a.juros)} | {br(a.prestacao)} | {br(b.juros)} | {br(b.amortizacao)} | {br(b.prestacao)} | {br(b.saldo_final)} |")
r(f"| total | {br(total_juros(sac_c2))} | {br(sum(l.prestacao for l in sac_c2))} | {br(total_juros(pri_c2))} | 1200,00 | {br(sum(l.prestacao for l in pri_c2))} | |")
r()

# ----------------------------------------------------------------------------
# 5c. Tabela de sintomas: valores que erros comuns de implementação produzem
#     (para localizar a origem de uma divergência observada no app)
# ----------------------------------------------------------------------------
PV1, I1, N1 = 10000.0, 0.01, 120
sintomas = []
def pmt_f(pv, i, n):
    return pv * i / (1 - (1 + i) ** (-n))
sintomas.append(("Price", "correto", pmt_f(PV1, I1, N1), (N1 * pmt_f(PV1, I1, N1) - PV1)))
sintomas.append(("Price", "taxa em % não convertida (i = 1)", pmt_f(PV1, 1.0, N1), None))
sintomas.append(("Price", "taxa convertida duas vezes (i = 0,0001)", pmt_f(PV1, 0.0001, N1), None))
sintomas.append(("Price", "expoente positivo: PV·i/[1−(1+i)^n]", PV1 * I1 / (1 - (1 + I1) ** N1), None))
sintomas.append(("Price", "PV(1+i)^n/n (montante dividido em n)", PV1 * (1 + I1) ** N1 / N1, None))
sintomas.append(("Price", "PV(1+in)/n (juros simples)", PV1 * (1 + I1 * N1) / N1, None))
sintomas.append(("Price", "taxa anual 12% usada como mensal", pmt_f(PV1, 0.12, N1), None))
# SAC
def sac_tot(fn_j, n=N1, pv=PV1, i=I1):
    c = pv / n; sd = pv; ps = []; tj = 0
    for k in range(1, n + 1):
        j = fn_j(sd, c, pv, i)
        ps.append(c + j); tj += j; sd -= c
    return ps, tj
ps, tj = sac_tot(lambda sd, c, pv, i: sd * i)
sintomas.append(("SAC", "correto", ps[0], tj, ps[-1]))
ps, tj = sac_tot(lambda sd, c, pv, i: pv * i)
sintomas.append(("SAC", "juros sempre sobre PV", ps[0], tj, ps[-1]))
ps, tj = sac_tot(lambda sd, c, pv, i: (sd - c) * i)
sintomas.append(("SAC", "juros sobre o saldo já amortizado", ps[0], tj, ps[-1]))
# laço com range(1, n): uma prestação a menos
c = PV1 / N1; sd = PV1; tj = 0
for k in range(1, N1):
    tj += sd * I1; sd -= c
sintomas.append(("SAC", "laço range(1, n): 119 prestações, saldo final ≠ 0", PV1 / N1 + PV1 * I1, tj, f"saldo {sd:.2f}"))

r("## 4c. Sintomas de erros comuns de implementação (PV = 10.000, i = 1%, n = 120)")
r()
r("Use para localizar a causa de uma divergência observada no app: compare o valor da tela com a coluna 'valor produzido'.")
r()
r("| Sistema | Implementação | valor produzido (1ª prestação / PMT) | total de juros | última / observação |")
r("|---|---|---|---|---|")
for row in sintomas:
    sist, desc, v1 = row[0], row[1], row[2]
    tj = row[3] if len(row) > 3 and row[3] is not None else None
    ult = row[4] if len(row) > 4 else ""
    ult = br(ult) if isinstance(ult, float) else ult
    r(f"| {sist} | {desc} | {br(v1)} | {br(tj) if tj is not None else '—'} | {ult} |")
r()
with open(os.path.join(TEX, "tab_sintomas.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — não editar à mão\n")
    f.write("\\begin{table}[htbp]\n\\centering\n\\small\n")
    f.write("\\caption{Valores produzidos por erros comuns de implementação ($PV=10\\,000$; $i=1\\%$; $n=120$), "
            "usados para localizar a origem de divergências}\n\\label{tab:sintomas}\n")
    f.write("\\begin{tabular}{@{}llrr@{}}\n\\toprule\n")
    f.write("Sistema & Implementação & $P_1$ ou $PMT$ & Juros totais \\\\\n\\midrule\n")
    for row in sintomas:
        sist, desc, v1 = row[0], row[1], row[2]
        tj = row[3] if len(row) > 3 and row[3] is not None else None
        d = (desc.replace("%", "\\%").replace("·", "$\\cdot$").replace("−", "$-$")
             .replace("(1+i)^n", "$(1+i)^n$").replace("≠", "$\\neq$").replace("range(1, n)", "\\texttt{range(1, n)}"))
        f.write(f"{sist} & {d} & {brt(v1)} & {brt(tj) if tj is not None else '---'} \\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n\\par\\smallskip\\footnotesize Fonte: Elaborada pelo autor (2026).\n\\end{table}\n")

# ----------------------------------------------------------------------------
# 6. Ficha para conferir o aplicativo (valores que o app DEVE exibir)
# ----------------------------------------------------------------------------
ficha = []
for nome, pv, i, n, desc in CENARIOS:
    for sistema in ("SAC", "Price"):
        e_, _, _, _ = resultados[(nome, sistema)]
        ks = sorted(k for k in {1, 2, max(1, n // 2), n} if k <= n)
        for k in ks:
            l = e_[k - 1]
            ficha.append((nome, sistema, br(pv), br(Fraction(i) * 100, 1) + "%", n, k,
                          br(l.juros), br(l.amortizacao), br(l.prestacao), br(l.saldo_final)))
with open(os.path.join(SAIDA, "ficha_conferencia_app.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["cenario", "sistema", "PV", "taxa", "n", "k", "juros_esperado", "amortizacao_esperada",
                "prestacao_esperada", "saldo_esperado", "PRESTACAO_EXIBIDA_NO_APP", "JUROS_EXIBIDOS_NO_APP",
                "CONFERE_S_N", "PRINT_DA_TELA_ARQUIVO", "OBSERVACAO"])
    for row in ficha:
        w.writerow(list(row) + ["", "", "", "", ""])

with open(os.path.join(TEX, "tab_ficha_app.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por conferir_calculos.py — as colunas App e Ok são preenchidas pelo autor após rodar o aplicativo (ver ficha_conferencia_app.csv)\n")
    f.write("\\begin{longtable}{@{}llrrrrrrcc@{}}\n")
    f.write("\\caption{Ficha de conferência das telas do AlgoFin: valores de referência dos juros ($J_k$) e da prestação ($P_k$) "
            "na parcela $k$, valor exibido pelo aplicativo (App) e resultado da comparação (Ok)}\\label{tab:ficha-app}\\\\\n")
    cab = "Cen. & Sist. & $PV$ & $i$ & $n$ & $k$ & $J_k$ & $P_k$ & App & Ok \\\\\n"
    f.write("\\toprule\n" + cab + "\\midrule\n\\endfirsthead\n\\toprule\n" + cab + "\\midrule\n\\endhead\n")
    for (nome, sistema, pv, tx, n, k, j, a, p, s) in ficha:
        tx_tex = tx.replace("%", r"\%")
        f.write(f"{nome} & {sistema} & {pv} & {tx_tex} & {n} & {k} & {j} & {p} & & \\\\\n")
    f.write("\\bottomrule\n\\end{longtable}\n")

# ----------------------------------------------------------------------------
# 7. Fecha relatório
# ----------------------------------------------------------------------------
falhas = [c for c in casos if not c[3]]
r("## 5. Arquivos gerados")
r()
for nome in sorted(os.listdir(SAIDA)):
    if nome.endswith(".csv"):
        r(f"* `saida/{nome}`")
for nome in sorted(os.listdir(TEX)):
    r(f"* `saida/tabelas_latex/{nome}`")
r()
r(f"**Resultado:** {len(casos) - len(falhas)} de {len(casos)} casos conferem com a referência."
  + ("" if not falhas else " Falhas: " + "; ".join(c[0] for c in falhas)))
r()
r("Observação: 'Entrada 1,5 com float() puro' é marcada OK porque o teste confirma o defeito "
  "esperado (o Código 1 rejeita vírgula decimal). A correção recomendada é usar ler_numero_br().")

# ----------------------------------------------------------------------------
# 8. Padroniza as tabelas geradas no estilo da dissertação (\hline; Fonte em \small)
# ----------------------------------------------------------------------------
import re as _re
for _nome in os.listdir(TEX):
    _p = os.path.join(TEX, _nome)
    _t = open(_p, encoding="utf-8").read()
    _t = (_t.replace("\\toprule", "\\hline").replace("\\midrule", "\\hline")
            .replace("\\bottomrule", "\\hline")
            .replace("\\cmidrule{2-5}\\cmidrule{7-10}", "\\cline{2-5}\\cline{7-10}")
            .replace("[htbp]", "[htb]").replace("@{}", ""))
    _t = _re.sub(r"\\par\\smallskip\\footnotesize (Fonte:[^\n]*)",
                 lambda m: "\\par\\vspace{0.1cm}\n{\\small " + m.group(1).strip().replace("Fonte: elaborad", "Fonte: Elaborad") + "}", _t)
    open(_p, "w", encoding="utf-8").write(_t)

with open(os.path.join(SAIDA, "relatorio_conferencia.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(relatorio) + "\n")

print("\n".join(relatorio))
sys.exit(1 if falhas else 0)
