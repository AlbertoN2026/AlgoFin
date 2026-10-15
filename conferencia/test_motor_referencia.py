"""
Testes automatizados (biblioteca padrão, sem dependências).

Uso:  python3 -m unittest -v test_motor_referencia.py

Cada teste corresponde a uma propriedade matemática enunciada na
fundamentação (Capítulo 3 revisado). Se o código do AlgoFin for adaptado
para expor funções equivalentes, basta trocar o import abaixo para testar
o próprio app.
"""
import unittest
from decimal import Decimal
from fractions import Fraction as F

import motor_referencia as m


class TestSAC(unittest.TestCase):
    def setUp(self):
        self.L = m.sac(10000, "0.01", 120, "exato")

    def test_amortizacao_constante_e_soma_pv(self):
        self.assertTrue(all(l.amortizacao == F(10000, 120) for l in self.L))
        self.assertEqual(sum(l.amortizacao for l in self.L), 10000)

    def test_saldo_final_zero(self):
        self.assertEqual(self.L[-1].saldo_final, 0)

    def test_juros_em_pa(self):
        razao = -F(1, 100) * F(10000, 120)
        for a, b in zip(self.L, self.L[1:]):
            self.assertEqual(b.juros - a.juros, razao)

    def test_formula_fechada_prestacao(self):
        pv, i, n = F(10000), F(1, 100), 120
        for l in self.L:
            self.assertEqual(l.prestacao, pv / n + i * (pv - (l.k - 1) * pv / n))

    def test_total_juros(self):
        self.assertEqual(m.total_juros(self.L), F(1, 100) * 10000 * 121 / 2)

    def test_valores_tabela7(self):
        self.assertEqual(m.arredonda_centavo(self.L[0].prestacao), Decimal("183.33"))
        self.assertEqual(m.arredonda_centavo(self.L[59].prestacao), Decimal("134.17"))
        self.assertEqual(m.arredonda_centavo(self.L[119].prestacao), Decimal("84.17"))

    def test_float_proximo_do_exato(self):
        Lf = m.sac(10000, 0.01, 120, "float")
        for a, b in zip(self.L, Lf):
            self.assertLess(m.erro_relativo(a.prestacao, b.prestacao), 1e-14)

    def test_centavos_zera_saldo(self):
        Lc = m.sac(10000, "0.01", 120, "centavos")
        self.assertEqual(Lc[-1].saldo_final, 0)
        self.assertEqual(sum(l.amortizacao for l in Lc), 10000)

    def test_taxa_zero(self):
        L0 = m.sac(10000, "0", 120)
        self.assertEqual(m.total_juros(L0), 0)
        self.assertTrue(all(l.prestacao == F(10000, 120) for l in L0))


class TestPrice(unittest.TestCase):
    def setUp(self):
        self.L = m.price(10000, "0.01", 120, "exato")
        self.pmt = m.prestacao_price(10000, "0.01", 120)

    def test_prestacao(self):
        self.assertEqual(m.arredonda_centavo(self.pmt), Decimal("143.47"))

    def test_saldo_final_zero(self):
        self.assertEqual(self.L[-1].saldo_final, 0)

    def test_amortizacoes_em_pg(self):
        a1 = self.L[0].amortizacao
        for l in self.L:
            self.assertEqual(l.amortizacao, a1 * F(101, 100) ** (l.k - 1))

    def test_total_juros(self):
        self.assertEqual(m.total_juros(self.L), 120 * self.pmt - 10000)

    def test_taxa_zero_e_limite(self):
        self.assertEqual(m.prestacao_price(10000, "0", 120), F(10000, 120))
        # limite i -> 0: PMT ~ (PV/n)[1 + i(n+1)/2], logo tende a PV/n
        self.assertAlmostEqual(float(m.prestacao_price(10000, "0.000000000001", 120)), 10000 / 120, places=6)

    def test_n_igual_1(self):
        self.assertEqual(m.prestacao_price(1000, "0.01", 1), 1010)

    def test_centavos_zera_saldo(self):
        Lc = m.price(10000, "0.01", 120, "centavos")
        self.assertEqual(Lc[-1].saldo_final, 0)


class TestJurosEAportes(unittest.TestCase):
    def test_iterativo_igual_fechado(self):
        for n in (0, 1, 12, 120, 360):
            mf = m.juros_compostos_fechado(1000, "0.01", n)
            mi = m.juros_compostos_iterativo_float(1000, 0.01, n)
            self.assertLess(m.erro_relativo(mf, mi), 1e-13)

    def test_aportes_recorrencia_igual_fechado(self):
        for i in ("0", "0.005", "0.01", "0.02"):
            for n in (0, 1, 12, 60):
                self.assertEqual(m.serie_aportes_recorrencia(500, i, 100, n),
                                 m.serie_aportes_fechado(500, i, 100, n))

    def test_taxa_equivalente_ida_e_volta(self):
        anual = m.taxa_equivalente(0.01, 12)
        self.assertAlmostEqual(m.taxa_equivalente(anual, 1 / 12), 0.01, places=14)

    def test_tempo_para_dobrar(self):
        self.assertEqual(m.tempo_para_meta(1000, "0.01", 2000), 70)


class TestCasosDeBorda(unittest.TestCase):
    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            m.sac(10000, "0.01", 0)
        with self.assertRaises(ValueError):
            m.price(-1, "0.01", 12)
        with self.assertRaises(ValueError):
            m.sac(1000, "-0.01", 12)

    def test_erro_relativo_indefinido_em_zero(self):
        with self.assertRaises(ZeroDivisionError):
            m.erro_relativo(0, 1e-13)
        self.assertAlmostEqual(m.erro_absoluto(0, 1e-13), 1e-13)

    def test_poupanca(self):
        self.assertEqual(m.meses_para_meta_poupanca(150, 20, 650), 5)
        self.assertEqual(m.meses_para_meta_poupanca(150, 20, 700), 6)
        with self.assertRaises(ValueError):
            m.meses_para_meta_poupanca(100, 120, 650)

    def test_inflacao(self):
        perda, falta = m.perda_poder_compra(1000, "0.05")
        self.assertEqual(m.arredonda_centavo(perda), Decimal("47.62"))
        self.assertEqual(falta, 50)

    def test_leitura_br(self):
        self.assertEqual(m.ler_numero_br("1,5"), 1.5)
        self.assertEqual(m.ler_numero_br("1.234,56"), 1234.56)
        self.assertEqual(m.ler_numero_br("R$ 10"), 10.0)
        self.assertEqual(m.ler_numero_br("2%"), 2.0)
        self.assertEqual(m.ler_numero_br("1.000"), 1000.0)   # milhar brasileiro
        self.assertEqual(m.ler_numero_br("10.000,00"), 10000.0)
        self.assertEqual(m.ler_numero_br("1.5"), 1.5)
        with self.assertRaises(ValueError):
            m.ler_numero_br("   ")

    def test_formata_brl(self):
        self.assertEqual(m.formata_brl(1234.5), "R$ 1.234,50")
        self.assertEqual(m.formata_brl(0.005), "R$ 0,01")
        # empate exato (C5, SAC, juros da parcela 12): meio para cima, hipótese H6
        self.assertEqual(m.formata_brl(F(325, 8)), "R$ 40,63")
        self.assertEqual(m.formata_brl(1000000), "R$ 1.000.000,00")


if __name__ == "__main__":
    unittest.main(verbosity=2)
