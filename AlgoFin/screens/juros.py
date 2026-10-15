"""Tela "Juros e Amortização" (Controller).

Lê os campos da View (kv/juros.kv), delega os cálculos ao Model
(modelo_financeiro.py) e devolve o resultado formatado no padrão brasileiro.
"""
import webbrowser

from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from modelo_financeiro import (
    formata_brl,
    formata_numero,
    formata_percentual,
    ler_numero_br,
    montante_composto,
    tabela_price,
    tabela_sac,
    taxa_equivalente,
)

LINHAS_POR_PAGINA = 12
CARACTERES_NUMERICOS = "0123456789,.-"
COLUNAS = (("Mês", 0.55, "center"), ("Parcela", 1, "right"),
           ("Amort.", 1, "right"), ("Juros", 1, "right"), ("Saldo", 1, "right"))
MSG_FORMATO = ("Use números não negativos e o tempo em meses inteiros. "
               "Exemplos: 1.500,00 para o capital; 1,5 para a taxa.")


class JurosScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._linhas = []
        self._pagina = 0
        self._titulo_tabela = ""

    # ------------------------------------------------------------------
    # Campos de texto: aceita dígitos, vírgula, ponto e sinal de menos.
    # O sinal é aceito para que o estudante receba a mensagem que explica
    # por que valores negativos não valem (em vez de a tecla não responder).
    # ------------------------------------------------------------------
    def filtro_decimal(self, substring, from_undo=False):
        return "".join(c for c in substring if c in CARACTERES_NUMERICOS)

    def abrir_guia_juros(self):
        webbrowser.open("https://drive.google.com/file/d/1q0BBVIQBe0oijaN3paxsF3VWts2Sn9gi/view?usp=sharing")

    def abrir_guia_sac(self):
        webbrowser.open("https://drive.google.com/file/d/1w5LFSEPdVU5d_fhjAkZftvvge2eQfbFM/view?usp=sharing")

    # ------------------------------------------------------------------
    # Aba Teoria: depósito de R$ 100,00 a 2% ao mês
    # ------------------------------------------------------------------
    def atualizar_grafico(self, meses):
        meses = int(meses)
        capital = 100.0
        montante = montante_composto(capital, 0.02, meses)
        proporcao = (montante - capital) / capital
        self.ids.barra_juros.size_hint_x = max(0.01, proporcao * 0.5)
        self.ids.lbl_mes_grafico.text = (
            f"Mês {meses}: R$ 100,00 viraram [b]{formata_brl(montante)}[/b]. "
            f"Os juros já são {formata_percentual(proporcao * 100, 0)} do depósito.")

    # ------------------------------------------------------------------
    # Aba Praticar: simulador de juros compostos (Código 1 da dissertação)
    # ------------------------------------------------------------------
    def simular_juros(self):
        rotulo = self.ids.lbl_resultado_juros
        campos = (self.ids.input_capital.text,
                  self.ids.input_taxa.text,
                  self.ids.input_tempo.text)
        if not all(c.strip() for c in campos):
            rotulo.text = "Preencha os três campos."
            return
        try:
            capital = ler_numero_br(campos[0])
            taxa = ler_numero_br(campos[1]) / 100.0  # % -> forma unitária
            tempo = ler_numero_br(campos[2])
            if tempo != int(tempo):
                raise ValueError("tempo não inteiro")
            montante = montante_composto(capital, taxa, int(tempo))
        except ValueError:
            rotulo.text = MSG_FORMATO
            return
        juros = montante - capital
        rotulo.text = (f"Montante final: {formata_brl(montante)}\n"
                       f"Só de juros: {formata_brl(juros)}\n\n"
                       f"O computador repetiu o cálculo {int(tempo)} "
                       f"vezes (um ciclo por mês).")

    # ------------------------------------------------------------------
    # Aba Praticar: taxas equivalentes (RF03)
    # ------------------------------------------------------------------
    def converter_taxa(self, sentido):
        rotulo = self.ids.lbl_taxa_equiv
        texto = self.ids.input_taxa_equiv.text
        if not texto.strip():
            rotulo.text = "Digite uma taxa em %, por exemplo 1 ou 1,5."
            return
        try:
            t = ler_numero_br(texto)
            if t < 0:
                raise ValueError("taxa negativa")
        except ValueError:
            rotulo.text = "Use uma taxa não negativa, em %. Exemplos: 1; 1,5; 12."
            return
        if sentido == "mensal_anual":
            eq = taxa_equivalente(t / 100.0, 12) * 100
            rotulo.text = (f"{formata_percentual(t)} ao mês equivale a "
                           f"[b]{formata_percentual(eq)} ao ano[/b], com juros compostos.\n"
                           f"Compare com a taxa proporcional: 12 × {formata_percentual(t)} = "
                           f"{formata_percentual(12 * t)}.")
        else:
            eq = taxa_equivalente(t / 100.0, 1 / 12) * 100
            rotulo.text = (f"{formata_percentual(t)} ao ano equivale a "
                           f"[b]{formata_percentual(eq)} ao mês[/b], com juros compostos.\n"
                           f"Compare com a taxa proporcional: {formata_percentual(t)} ÷ 12 = "
                           f"{formata_percentual(t / 12)}.")

    # ------------------------------------------------------------------
    # Aba Amortização: tabelas do SAC e do Price
    # ------------------------------------------------------------------
    def gerar_tabela(self, sistema):
        aviso = self.ids.lbl_msg_tabela
        campos = (self.ids.input_sac_capital.text,
                  self.ids.input_sac_taxa.text,
                  self.ids.input_sac_tempo.text)
        if not all(c.strip() for c in campos):
            aviso.text = "Preencha o valor financiado, a taxa e o prazo."
            return
        try:
            pv = ler_numero_br(campos[0])
            taxa_pct = ler_numero_br(campos[1])
            n = ler_numero_br(campos[2])
        except ValueError:
            aviso.text = ("Use números no padrão brasileiro. Exemplos: 1.500,00 "
                          "para o valor; 1,5 para a taxa; 12 para o prazo.")
            return
        try:
            calcula = tabela_sac if sistema == "SAC" else tabela_price
            linhas = calcula(pv, taxa_pct / 100.0, n)
        except ValueError as erro:
            aviso.text = str(erro)
            return

        aviso.text = ""
        nome = "SAC" if sistema == "SAC" else "Price"
        self._titulo_tabela = (f"{nome}: {formata_brl(pv)} a "
                               f"{formata_percentual(taxa_pct)} ao mês "
                               f"em {int(n)} meses")
        self._linhas = linhas
        self._pagina = 0
        self._montar_tabela()

    def mudar_pagina(self, destino):
        ultima = max(0, (len(self._linhas) - 1) // LINHAS_POR_PAGINA)
        paginas = {"primeira": 0, "anterior": self._pagina - 1,
                   "proxima": self._pagina + 1, "ultima": ultima}
        self._pagina = min(max(paginas[destino], 0), ultima)
        self._montar_tabela()

    def _montar_tabela(self):
        container = self.ids.container_tabela
        container.clear_widgets()
        if not self._linhas:
            return

        n = len(self._linhas)
        ultima = (n - 1) // LINHAS_POR_PAGINA
        ini = self._pagina * LINHAS_POR_PAGINA
        fim = min(ini + LINHAS_POR_PAGINA, n)

        card = MDCard(orientation="vertical", padding=dp(8), spacing=dp(4),
                      radius=[12], elevation=1, size_hint_y=None)
        card.bind(minimum_height=card.setter("height"))

        card.add_widget(self._rotulo(self._titulo_tabela, "Subtitle2", bold=True))
        card.add_widget(self._rotulo("Valores em reais (R$).", "Caption"))

        grade = MDGridLayout(cols=len(COLUNAS), size_hint_y=None)
        grade.bind(minimum_height=grade.setter("height"))
        for titulo, peso, alinhamento in COLUNAS:
            grade.add_widget(self._celula(titulo, peso, alinhamento, cabecalho=True))
        for linha in self._linhas[ini:fim]:
            mes, valores = linha[0], linha[1:]
            fundo = (0.95, 0.95, 0.97, 1) if mes % 2 == 0 else (1, 1, 1, 1)
            grade.add_widget(self._celula(str(mes), COLUNAS[0][1], "center", fundo=fundo))
            for (_, peso, alinhamento), valor in zip(COLUNAS[1:], valores):
                grade.add_widget(self._celula(formata_numero(valor), peso,
                                              alinhamento, fundo=fundo))
        card.add_widget(grade)

        barra = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(2))
        for icone, destino, desativado in (("page-first", "primeira", self._pagina == 0),
                                           ("chevron-left", "anterior", self._pagina == 0)):
            barra.add_widget(self._botao_pagina(icone, destino, desativado))
        barra.add_widget(MDLabel(text=f"Meses {ini + 1} a {fim} de {n}",
                                 halign="center", font_style="Caption"))
        for icone, destino, desativado in (("chevron-right", "proxima", self._pagina == ultima),
                                           ("page-last", "ultima", self._pagina == ultima)):
            barra.add_widget(self._botao_pagina(icone, destino, desativado))
        card.add_widget(barra)

        total_juros = sum(linha[3] for linha in self._linhas)
        total_pago = sum(linha[1] for linha in self._linhas)
        card.add_widget(self._rotulo(
            f"Total de juros: {formata_brl(total_juros)}   ·   "
            f"Total pago: {formata_brl(total_pago)}", "Caption"))

        container.add_widget(card)

    # --- pequenos construtores de widgets -------------------------------
    @staticmethod
    def _rotulo(texto, estilo, bold=False):
        rotulo = MDLabel(text=texto, font_style=estilo, bold=bold,
                         size_hint_y=None, markup=True)
        rotulo.bind(texture_size=lambda inst, tam: setattr(inst, "height", tam[1]))
        return rotulo

    @staticmethod
    def _celula(texto, peso, alinhamento, cabecalho=False, fundo=None):
        celula = MDLabel(text=texto, halign=alinhamento, font_style="Body2",
                         bold=cabecalho, size_hint_x=peso, size_hint_y=None,
                         height=dp(30))
        if fundo:
            celula.md_bg_color = fundo
        return celula

    def _botao_pagina(self, icone, destino, desativado):
        return MDIconButton(icon=icone, disabled=desativado,
                            pos_hint={"center_y": 0.5},
                            on_release=lambda *_: self.mudar_pagina(destino))
