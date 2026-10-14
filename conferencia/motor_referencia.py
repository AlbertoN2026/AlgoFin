"""
motor_referencia.py — Implementação de REFERÊNCIA dos modelos financeiros do AlgoFin.

Finalidade: servir de oráculo para conferir os valores exibidos pelo aplicativo
e os valores impressos na dissertação. Não substitui o código do app; serve
para compará-lo.

Três modos de cálculo para cada sistema de amortização:
  * "exato"    -> aritmética racional (fractions.Fraction), sem arredondamento.
                  É o "valor analítico" (v_real) da dissertação.
  * "float"    -> ponto flutuante IEEE 754 (precisão dupla), sem arredondamento
                  intermediário. Reproduz o que um laço em Python puro faz.
  * "centavos" -> cada juro e cada prestação arredondados ao centavo
                  (meio para cima) e a ÚLTIMA amortização ajustada para zerar o
                  saldo. É a convenção usual de contratos reais.

Hipóteses gerais (devem constar na dissertação):
  H1. Taxa i constante, efetiva por período, i >= 0.
  H2. Pagamentos/aportes postecipados (no fim de cada período).
  H3. n inteiro, n >= 1. PV > 0.
  H4. Sem tributos, tarifas, seguros ou correção monetária (o "CET" não é
      modelado).
  H5. Juros calculados sobre o saldo devedor do início do período.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from typing import List, Union

Numero = Union[int, float, Fraction, Decimal]
CENTAVO = Decimal("0.01")


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------
def para_fracao(x: Numero) -> Fraction:
    """Converte para Fraction usando a representação DECIMAL (str), para que
    0.01 vire exatamente 1/100 e não o binário mais próximo."""
    if isinstance(x, Fraction):
        return x
    return Fraction(str(x))


def arredonda_centavo(x: Numero) -> Decimal:
    """Arredonda ao centavo, meio para cima (ROUND_HALF_UP)."""
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x)).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def trunca_centavo(x: Numero) -> Decimal:
    """Trunca ao centavo (o que produz 134,16 e 84,16 na Tabela 7)."""
    d = Decimal(str(float(x)))
    return d.quantize(CENTAVO, rounding="ROUND_DOWN")


def erro_relativo(v_real: Numero, v_aprox: Numero) -> float:
    """E_r = |v_real - v_aprox| / |v_real|. Indefinido quando v_real = 0:
    nesse caso a função levanta ZeroDivisionError e deve-se usar o erro
    absoluto (ver erro_absoluto)."""
    vr = para_fracao(v_real)
    va = Fraction(v_aprox) if isinstance(v_aprox, float) else para_fracao(v_aprox)
    if vr == 0:
        raise ZeroDivisionError("Erro relativo indefinido para v_real = 0; use o erro absoluto.")
    return float(abs(vr - va) / abs(vr))


def erro_absoluto(v_real: Numero, v_aprox: Numero) -> float:
    vr = para_fracao(v_real)
    va = Fraction(v_aprox) if isinstance(v_aprox, float) else para_fracao(v_aprox)
    return float(abs(vr - va))


# ----------------------------------------------------------------------------
# Juros simples, compostos, aportes e taxas equivalentes
# ----------------------------------------------------------------------------
def juros_simples(c: Numero, i: Numero, n: int) -> Fraction:
    """M = C (1 + i n)."""
    c, i = para_fracao(c), para_fracao(i)
    return c * (1 + i * n)


def juros_compostos_fechado(c: Numero, i: Numero, n: int) -> Fraction:
    """M = C (1 + i)^n — forma fechada, custo O(1) em operações de potência."""
    c, i = para_fracao(c), para_fracao(i)
    return c * (1 + i) ** n


def juros_compostos_iterativo_float(c: float, i: float, n: int) -> float:
    """Reproduz exatamente o laço do Código 1 da dissertação: O(n)."""
    saldo = float(c)
    for _ in range(1, n + 1):
        saldo = saldo + saldo * i
    return saldo


def serie_aportes_recorrencia(m0: Numero, i: Numero, a: Numero, n: int) -> Fraction:
    """M_{k+1} = M_k (1 + i) + A, aporte no fim de cada período."""
    m, i, a = para_fracao(m0), para_fracao(i), para_fracao(a)
    for _ in range(n):
        m = m * (1 + i) + a
    return m


def serie_aportes_fechado(m0: Numero, i: Numero, a: Numero, n: int) -> Fraction:
    """M_n = M_0 (1+i)^n + A [(1+i)^n - 1]/i ;  se i = 0:  M_n = M_0 + n A."""
    m0, i, a = para_fracao(m0), para_fracao(i), para_fracao(a)
    if i == 0:
        return m0 + n * a
    f = (1 + i) ** n
    return m0 * f + a * (f - 1) / i


def taxa_equivalente(i: Numero, k: Numero) -> float:
    """Taxa equivalente para um período k vezes maior: (1+i)^k - 1.
    Ex.: mensal -> anual com k = 12; anual -> mensal com k = 1/12."""
    return (1 + float(i)) ** float(k) - 1


def tempo_para_meta(c: Numero, i: Numero, meta: Numero) -> int:
    """Menor n inteiro com C(1+i)^n >= meta (i > 0). Busca iterativa."""
    c, i, meta = para_fracao(c), para_fracao(i), para_fracao(meta)
    if meta <= c:
        return 0
    if i <= 0:
        raise ValueError("Com i <= 0 o montante nunca atinge uma meta maior que o capital.")
    n, m = 0, c
    while m < meta:
        m *= (1 + i)
        n += 1
    return n


# ----------------------------------------------------------------------------
# Sistemas de amortização
# ----------------------------------------------------------------------------
@dataclass
class Linha:
    k: int
    saldo_inicial: object
    juros: object
    amortizacao: object
    prestacao: object
    saldo_final: object


def _checa_entradas(pv, i, n):
    if n < 1 or int(n) != n:
        raise ValueError("n deve ser inteiro >= 1")
    if para_fracao(pv) <= 0:
        raise ValueError("PV deve ser positivo")
    if para_fracao(i) < 0:
        raise ValueError("i deve ser >= 0")


def sac(pv: Numero, i: Numero, n: int, modo: str = "exato") -> List[Linha]:
    """Sistema de Amortização Constante.
    C = PV/n ; J_k = i [PV - (k-1)C] ; P_k = C + J_k ; SD_k = PV - kC."""
    _checa_entradas(pv, i, n)
    linhas: List[Linha] = []
    if modo == "exato":
        pv_, i_ = para_fracao(pv), para_fracao(i)
        c = pv_ / n
        saldo = pv_
        for k in range(1, n + 1):
            j = saldo * i_
            p = c + j
            linhas.append(Linha(k, saldo, j, c, p, saldo - c))
            saldo -= c
    elif modo == "float":
        pv_, i_ = float(pv), float(i)
        c = pv_ / n
        saldo = pv_
        for k in range(1, n + 1):
            j = saldo * i_
            p = c + j
            linhas.append(Linha(k, saldo, j, c, p, saldo - c))
            saldo -= c
    elif modo == "centavos":
        pv_, i_ = Decimal(str(pv)), Decimal(str(i))
        c = arredonda_centavo(pv_ / n)
        saldo = pv_
        for k in range(1, n + 1):
            j = arredonda_centavo(saldo * i_)
            amort = saldo if k == n else c          # ajuste na última parcela
            p = amort + j
            linhas.append(Linha(k, saldo, j, amort, p, saldo - amort))
            saldo -= amort
    else:
        raise ValueError("modo deve ser 'exato', 'float' ou 'centavos'")
    return linhas


def prestacao_price(pv: Numero, i: Numero, n: int) -> Fraction:
    """PMT = PV i / [1 - (1+i)^{-n}] ; se i = 0: PMT = PV/n (limite)."""
    pv_, i_ = para_fracao(pv), para_fracao(i)
    if i_ == 0:
        return pv_ / n
    f = (1 + i_) ** n
    return pv_ * i_ * f / (f - 1)


def price(pv: Numero, i: Numero, n: int, modo: str = "exato") -> List[Linha]:
    """Sistema Francês (Price): prestação constante.
    J_k = i SD_{k-1} ; A_k = PMT - J_k ; A_k = A_1 (1+i)^{k-1}."""
    _checa_entradas(pv, i, n)
    linhas: List[Linha] = []
    if modo == "exato":
        pv_, i_ = para_fracao(pv), para_fracao(i)
        pmt = prestacao_price(pv_, i_, n)
        saldo = pv_
        for k in range(1, n + 1):
            j = saldo * i_
            a = pmt - j
            linhas.append(Linha(k, saldo, j, a, pmt, saldo - a))
            saldo -= a
    elif modo == "float":
        pv_, i_ = float(pv), float(i)
        pmt = pv_ / n if i_ == 0 else pv_ * i_ / (1 - (1 + i_) ** (-n))
        saldo = pv_
        for k in range(1, n + 1):
            j = saldo * i_
            a = pmt - j
            linhas.append(Linha(k, saldo, j, a, pmt, saldo - a))
            saldo -= a
    elif modo == "centavos":
        pv_, i_ = Decimal(str(pv)), Decimal(str(i))
        pmt = arredonda_centavo(prestacao_price(pv, i, n))
        saldo = pv_
        for k in range(1, n + 1):
            j = arredonda_centavo(saldo * i_)
            if k == n:                                # ajuste na última parcela
                a = saldo
                p = a + j
            else:
                a = pmt - j
                p = pmt
            linhas.append(Linha(k, saldo, j, a, p, saldo - a))
            saldo -= a
    else:
        raise ValueError("modo deve ser 'exato', 'float' ou 'centavos'")
    return linhas


def total_juros(linhas: List[Linha]):
    total = linhas[0].juros * 0
    for l in linhas:
        total += l.juros
    return total


# ----------------------------------------------------------------------------
# Módulo de Poupança (blocos): meses para atingir a meta
# ----------------------------------------------------------------------------
def meses_para_meta_poupanca(mesada: Numero, gasto: Numero, meta: Numero) -> int:
    """Menor n com n (mesada - gasto) >= meta. Sem juros (crescimento linear).
    Caso especial: poupança mensal <= 0 nunca atinge a meta -> ValueError
    (no app, sem essa guarda, o laço 'Juntar R$ meta' não termina)."""
    mesada, gasto, meta = para_fracao(mesada), para_fracao(gasto), para_fracao(meta)
    poupanca = mesada - gasto
    if meta <= 0:
        return 0
    if poupanca <= 0:
        raise ValueError("Poupança mensal <= 0: a meta nunca é atingida (laço infinito).")
    q, r = divmod(meta, poupanca)
    return int(q) + (1 if r else 0)


# ----------------------------------------------------------------------------
# Inflação e poder de compra (questão da Figura 8)
# ----------------------------------------------------------------------------
def perda_poder_compra(valor: Numero, inflacao: Numero):
    """Retorna (perda medida em preços do início do período,
                falta medida em preços do fim do período)."""
    v, f = para_fracao(valor), para_fracao(inflacao)
    poder_real = v / (1 + f)            # quanto o dinheiro compra, em preços iniciais
    return v - poder_real, v * f        # 47,62... e 50,00 para R$ 1.000 a 5%


# ----------------------------------------------------------------------------
# Leitura de números digitados por estudantes brasileiros
# ----------------------------------------------------------------------------
def ler_numero_br(texto: str) -> float:
    """Le numeros digitados no padrao brasileiro ou com ponto decimal.
    '1,5' -> 1.5 ; '1.234,56' -> 1234.56 ; '1.000' -> 1000 ; '10.000' -> 10000 ;
    '1.5' -> 1.5 ; 'R$ 10' -> 10 ; '2%' -> 2.
    Regra para ponto sem virgula: um unico ponto seguido de exatamente 3 digitos
    e separador de milhar (padrao brasileiro); varios pontos tambem."""
    t = texto.strip().replace("R$", "").replace("%", "").replace(" ", "")
    if not t:
        raise ValueError("campo vazio")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    elif t.count(".") > 1 or (t.count(".") == 1 and len(t.split(".")[1]) == 3):
        t = t.replace(".", "")
    return float(t)

def formata_brl(x: Numero) -> str:
    """Formata no padrão brasileiro: R$ 1.234,56 (f'{x:.2f}' produziria 1234.56)."""
    d = arredonda_centavo(x)
    sinal = "-" if d < 0 else ""
    inteiro, frac = f"{abs(d):.2f}".split(".")
    grupos = []
    while inteiro:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    return f"{sinal}R$ {'.'.join(grupos)},{frac}"
