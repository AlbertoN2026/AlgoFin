"""Model do AlgoFin: Matemática Financeira e formatação no padrão brasileiro.

Funções puras, sem dependência do Kivy: podem ser testadas fora do aplicativo
(ver conferencia/test_modelo_app.py no repositório).

Convenção de exibição (hipótese H6 da dissertação): os cálculos são feitos em
ponto flutuante, sem arredondamento intermediário, e cada valor é arredondado
ao centavo apenas na exibição, com empates para cima (ROUND_HALF_UP).
"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

PRAZO_MAXIMO = 600  # meses (50 anos): limite das tabelas de amortização


# ---------------------------------------------------------------------------
# Leitura e formatação de números
# ---------------------------------------------------------------------------
def ler_numero_br(texto):
    """Lê números digitados no padrão brasileiro ou com ponto decimal.

    '1,5' -> 1.5 ; '1.234,56' -> 1234.56 ; '1.000' -> 1000.0 ;
    '1.5' -> 1.5 ; 'R$ 10' -> 10.0 ; '2%' -> 2.0.
    Um único ponto seguido de exatamente três dígitos é lido como separador
    de milhar (padrão brasileiro). Campo vazio ou texto inválido: ValueError.
    """
    t = str(texto).strip()
    for simbolo in ("R$", "%", " "):
        t = t.replace(simbolo, "")
    if not t:
        raise ValueError("campo vazio")
    partes = t.split(".")
    if "," in t:                          # vírgula decimal
        t = t.replace(".", "").replace(",", ".")
    elif len(partes) > 2 or (len(partes) == 2 and len(partes[1]) == 3):
        t = t.replace(".", "")            # ponto de milhar
    return float(t)


def arredonda(valor, casas=2):
    """Arredonda para exibição, com empates para cima (meio para cima).

    Um valor em ponto flutuante é antes aproximado a seis casas decimais, o que
    remove o resíduo das operações: os juros exatos de R$ 3,125 (cenário C5,
    24.ª parcela do SAC) chegam aqui como 3,1249999999999996 e, sem esse passo,
    seriam exibidos como R$ 3,12 em vez de R$ 3,13.
    """
    if isinstance(valor, Fraction):
        d = Decimal(valor.numerator) / Decimal(valor.denominator)
    else:
        d = Decimal(str(valor))
    if isinstance(valor, float):
        d = d.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    quantum = Decimal(1).scaleb(-casas)
    return d.quantize(quantum, rounding=ROUND_HALF_UP)


def formata_numero(valor, casas=2):
    """1234.5 -> '1.234,50' (separador de milhar e vírgula decimal)."""
    d = arredonda(valor, casas)
    texto = f"{abs(d):,.{casas}f}"        # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if d < 0 else "") + texto


def formata_brl(valor):
    """1234.5 -> 'R$ 1.234,50' ; -3 -> '-R$ 3,00'."""
    texto = formata_numero(valor, 2)
    if texto.startswith("-"):
        return "-R$ " + texto[1:]
    return "R$ " + texto


def formata_percentual(valor, casas=2):
    """1.5 -> '1,5%' ; 12.6825 -> '12,68%' (sem zeros finais desnecessários)."""
    texto = formata_numero(valor, casas)
    if "," in texto:
        texto = texto.rstrip("0").rstrip(",")
    return texto + "%"


# ---------------------------------------------------------------------------
# Juros compostos
# ---------------------------------------------------------------------------
def montante_composto(capital, taxa, periodos):
    """Recorrência M(k+1) = M(k)(1 + i).
    Invariante: após k voltas do laço, saldo = M(k)."""
    if capital < 0 or taxa < 0 or periodos < 0:
        raise ValueError("valores negativos")
    saldo = capital
    for _ in range(periodos):
        saldo = saldo * (1 + taxa)
    return saldo


def taxa_equivalente(taxa, periodos):
    """Taxa equivalente com juros compostos: (1 + i)^k - 1.
    Mensal -> anual: k = 12 ; anual -> mensal: k = 1/12."""
    if taxa <= -1:
        raise ValueError("taxa inválida")
    return (1 + taxa) ** periodos - 1


# ---------------------------------------------------------------------------
# Sistemas de amortização (mesmas recorrências da implementação de referência,
# em ponto flutuante, sem arredondamento intermediário)
# ---------------------------------------------------------------------------
def _checa_financiamento(pv, i, n):
    if pv <= 0:
        raise ValueError("O valor financiado deve ser maior que zero.")
    if i < 0:
        raise ValueError("A taxa não pode ser negativa.")
    if n != int(n) or n < 1:
        raise ValueError("O prazo deve ser um número inteiro de meses, a partir de 1.")
    if n > PRAZO_MAXIMO:
        raise ValueError(f"Use um prazo de até {PRAZO_MAXIMO} meses.")


def tabela_sac(pv, i, n):
    """SAC: amortização constante A = PV/n; J_k = i·SD_(k-1); P_k = A + J_k.
    Devolve uma lista de linhas (mês, prestação, amortização, juros, saldo)."""
    _checa_financiamento(pv, i, n)
    n = int(n)
    amortizacao = pv / n
    saldo = pv
    linhas = []
    for mes in range(1, n + 1):
        juros = saldo * i
        prestacao = amortizacao + juros
        saldo = saldo - amortizacao
        linhas.append((mes, prestacao, amortizacao, juros, saldo))
    return linhas


def prestacao_price(pv, i, n):
    """PMT = PV·i / [1 - (1+i)^(-n)]; com i = 0, PMT = PV/n."""
    if i == 0:
        return pv / n
    return pv * i / (1 - (1 + i) ** (-n))


def tabela_price(pv, i, n):
    """Price: prestação constante; J_k = i·SD_(k-1); A_k = PMT - J_k.
    Devolve uma lista de linhas (mês, prestação, amortização, juros, saldo)."""
    _checa_financiamento(pv, i, n)
    n = int(n)
    pmt = prestacao_price(pv, i, n)
    saldo = pv
    linhas = []
    for mes in range(1, n + 1):
        juros = saldo * i
        amortizacao = pmt - juros
        saldo = saldo - amortizacao
        linhas.append((mes, pmt, amortizacao, juros, saldo))
    return linhas
