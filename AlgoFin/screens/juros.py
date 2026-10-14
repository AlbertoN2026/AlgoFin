import webbrowser
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable

class JurosScreen(MDScreen):
    
    def abrir_guia_juros(self):
        link_guia_drive = "https://drive.google.com/file/d/1q0BBVIQBe0oijaN3paxsF3VWts2Sn9gi/view?usp=sharing"
        webbrowser.open(link_guia_drive)

    def abrir_guia_sac(self):
        link_guia_sac = "https://drive.google.com/file/d/1w5LFSEPdVU5d_fhjAkZftvvge2eQfbFM/view?usp=sharing"
        webbrowser.open(link_guia_sac)

    def atualizar_grafico(self, meses):
        taxa = 0.02
        capital = 100
        montante = capital * ((1 + taxa) ** meses)
        juros_gerados = montante - capital
        proporcao = juros_gerados / capital
        
        self.ids.barra_juros.size_hint_x = max(0.01, proporcao * 0.5)
        self.ids.lbl_legenda.text = f"Mês {int(meses)}: O depósito base gerou [b]{(proporcao*100):.0f}%[/b] de lucro!"

    def simular_juros(self):
        try:
            texto_capital = self.ids.input_capital.text
            texto_taxa = self.ids.input_taxa.text
            texto_tempo = self.ids.input_tempo.text
            
            if not texto_capital or not texto_taxa or not texto_tempo:
                self.ids.lbl_resultado_juros.text = "Por favor, preencha todos os campos."
                return
                
            capital = float(texto_capital)
            taxa_decimal = float(texto_taxa) / 100.0
            tempo = int(texto_tempo)
            
            saldo_acumulado = capital
            
            for mes in range(1, tempo + 1):
                saldo_acumulado = saldo_acumulado + (saldo_acumulado * taxa_decimal)
                
            juros_totais = saldo_acumulado - capital
            
            resultado = (
                f"Montante Final: R$ {saldo_acumulado:.2f}\n"
                f"Apenas de Juros: R$ {juros_totais:.2f}\n\n"
                f"O computador fez {tempo} ciclos (loops) para descobrir isto!"
            )
            self.ids.lbl_resultado_juros.text = resultado
            
        except ValueError:
            self.ids.lbl_resultado_juros.text = "Erro: Introduza apenas números."

    def gerar_tabela_sac(self):
        self.ids.container_tabela.clear_widgets()

        try:
            texto_capital = self.ids.input_sac_capital.text
            texto_taxa = self.ids.input_sac_taxa.text
            texto_tempo = self.ids.input_sac_tempo.text

            if not texto_capital or not texto_taxa or not texto_tempo:
                return

            capital = float(texto_capital)
            taxa_decimal = float(texto_taxa) / 100.0
            tempo = int(texto_tempo)

            amortizacao_constante = capital / tempo
            saldo_devedor = capital
            
            linhas_tabela = []

            for mes in range(1, tempo + 1):
                juros_do_mes = saldo_devedor * taxa_decimal
                prestacao = amortizacao_constante + juros_do_mes
                saldo_devedor -= amortizacao_constante
                
                if saldo_devedor < 0.01:
                    saldo_devedor = 0

                linha = (
                    str(mes),
                    f"R$ {prestacao:.2f}",
                    f"R$ {amortizacao_constante:.2f}",
                    f"R$ {juros_do_mes:.2f}",
                    f"R$ {saldo_devedor:.2f}"
                )
                linhas_tabela.append(linha)

            tabela = MDDataTable(
                use_pagination=True,
                rows_num=5,
                column_data=[
                    ("Mês", dp(15)),
                    ("Parcela", dp(25)),
                    ("Amort.", dp(25)),
                    ("Juros", dp(25)),
                    ("Saldo", dp(30)),
                ],
                row_data=linhas_tabela,
                elevation=1
            )

            self.ids.container_tabela.add_widget(tabela)

        except ValueError:
            pass