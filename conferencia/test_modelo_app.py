"""Confere o Model do aplicativo (AlgoFin/modelo_financeiro.py) contra a
implementação de referência exata (motor_referencia.py).

Para cada cenário da ficha (C1 a C5) e cada sistema (SAC e Price), todas as
linhas da tabela exibida pelo aplicativo (prestação, amortização, juros e
saldo, arredondados ao centavo na exibição) devem coincidir com os valores
exatos arredondados pela mesma convenção (hipótese H6).

Uso (na raiz do repositório):  python -m unittest discover -s conferencia -v
"""
import os
import sys
import unittest
from fractions import Fraction as F

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "AlgoFin"))

import modelo_financeiro as app  # noqa: E402
import motor_referencia as ref   # noqa: E402

CENARIOS = [  # (nome, PV, taxa em %, n) — os mesmos de conferir_calculos.py
    ("C1", "10000", "1", 120),
    ("C2", "1200", "2", 6),
    ("C3", "10000", "0", 120),
    ("C4", "1000", "1", 1),
    ("C5", "5000", "1,5", 24),
]


def exibido_ref(valor):
    """Valor exato arredondado ao centavo, no formato da tela (1.234,56)."""
    return app.formata_numero(ref.arredonda_centavo(valor))


class TabelasDoAplicativo(unittest.TestCase):
    def _confere(self, sistema_app, sistema_ref):
        for nome, pv_txt, taxa_txt, n in CENARIOS:
            # entradas lidas como o aplicativo as lê (campos de texto)
            pv = app.ler_numero_br(pv_txt)
            i = app.ler_numero_br(taxa_txt) / 100.0
            linhas_app = sistema_app(pv, i, n)
            linhas_ref = sistema_ref(F(pv_txt.replace(",", ".")),
                                     F(taxa_txt.replace(",", ".")) / 100, n, "exato")
            self.assertEqual(len(linhas_app), len(linhas_ref))
            for (mes, p, a, j, s), r in zip(linhas_app, linhas_ref):
                with self.subTest(cenario=nome, mes=mes):
                    self.assertEqual(mes, r.k)
                    self.assertEqual(app.formata_numero(p), exibido_ref(r.prestacao))
                    self.assertEqual(app.formata_numero(a), exibido_ref(r.amortizacao))
                    self.assertEqual(app.formata_numero(j), exibido_ref(r.juros))
                    self.assertEqual(app.formata_numero(s), exibido_ref(r.saldo_final))

    def test_sac(self):
        self._confere(app.tabela_sac, ref.sac)

    def test_price(self):
        self._confere(app.tabela_price, ref.price)

    def test_ficha_c2(self):
        """Valores da ficha C2 já conferidos nas telas (resultados_telas.csv)."""
        sac = app.tabela_sac(1200.0, 0.02, 6)
        self.assertEqual([app.formata_numero(l[1]) for l in sac],
                         ["224,00", "220,00", "216,00", "212,00", "208,00", "204,00"])
        price = app.tabela_price(1200.0, 0.02, 6)
        self.assertEqual(app.formata_numero(price[0][1]), "214,23")
        self.assertEqual([app.formata_numero(l[2]) for l in price],
                         ["190,23", "194,04", "197,92", "201,87", "205,91", "210,03"])

    def test_entradas_invalidas(self):
        for pv, i, n in ((0, 0.01, 12), (-100, 0.01, 12), (100, -0.01, 12),
                         (100, 0.01, 0), (100, 0.01, 12.5), (100, 0.01, 601)):
            with self.subTest(pv=pv, i=i, n=n):
                with self.assertRaises(ValueError):
                    app.tabela_sac(pv, i, n)
                with self.assertRaises(ValueError):
                    app.tabela_price(pv, i, n)


class SimuladorDeJuros(unittest.TestCase):
    def test_roteiro_f09_f10(self):
        m = app.montante_composto(app.ler_numero_br("1000"), app.ler_numero_br("1") / 100, 12)
        self.assertEqual(app.formata_brl(m), "R$ 1.126,83")
        self.assertEqual(app.formata_brl(m - 1000), "R$ 126,83")
        m = app.montante_composto(app.ler_numero_br("1.000"), app.ler_numero_br("1,5") / 100, 12)
        self.assertEqual(app.formata_brl(m), "R$ 1.195,62")

    def test_leitura_e_formatacao(self):
        self.assertEqual(app.ler_numero_br("1.234,56"), 1234.56)
        self.assertEqual(app.ler_numero_br("1.000"), 1000.0)
        self.assertEqual(app.ler_numero_br("1.5"), 1.5)
        self.assertEqual(app.ler_numero_br("R$ 10"), 10.0)
        with self.assertRaises(ValueError):
            app.ler_numero_br("  ")
        with self.assertRaises(ValueError):
            app.ler_numero_br("abc")
        self.assertEqual(app.formata_brl(1234.5), "R$ 1.234,50")
        self.assertEqual(app.formata_brl(F(325, 8)), "R$ 40,63")   # empate: para cima
        self.assertEqual(app.formata_brl(-3), "-R$ 3,00")
        self.assertEqual(app.formata_brl(-1e-12), "R$ 0,00")
        self.assertEqual(app.formata_percentual(12.682503), "12,68%")
        self.assertEqual(app.formata_percentual(1.5), "1,5%")
        self.assertEqual(app.formata_percentual(2), "2%")


if __name__ == "__main__":
    unittest.main()
