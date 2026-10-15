from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class SimulacaoInvScreen(MDScreen):
    capital_val = NumericProperty(500)
    aporte_val = NumericProperty(50)
    taxa_val = NumericProperty(1)
    tempo_val = NumericProperty(12)
    
    total_investido_calc = NumericProperty(0)
    total_juros_calc = NumericProperty(0)
    montante_final_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Fundo de Competições",
            "texto": "O Clube precisa montar um fundo para pagar viagens para as olimpíadas. Eles começaram com [b]R$ 500,00[/b] (Capital Inicial) e prometeram depositar [b]R$ 100,00[/b] (Aporte) todo mês.\n\nA uma taxa de [b]2% ao mês[/b], ajuste a máquina para descobrir qual será o Montante Final exato acumulado após [b]12 meses[/b]?",
            "validador": lambda c, a, tx, t: c == 500 and a == 100 and tx == 2 and t == 12,
            "msg_acerto": "Projeção excelente! O clube investiu R$ 1.700 do próprio bolso e ganhou quase 230 reais totalmente de graça apenas com a força dos juros!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: O Desafio do Zero",
            "texto": "E se você não tiver NENHUM capital inicial? Ajuste o Capital Inicial para [b]R$ 0,00[/b].\n\nSe você depositar apenas [b]R$ 50,00[/b] por mês, a uma taxa de [b]1% ao mês[/b], em [b]36 meses[/b] (3 anos) quanto você terá juntado no total?",
            "validador": lambda c, a, tx, t: c == 0 and a == 50 and tx == 1 and t == 36,
            "msg_acerto": "Matemática comprovada! Mesmo começando do zero, a disciplina dos aportes mensais transformou pequenos depósitos em mais de 2.150 reais."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO FINAL: A Força Invisível",
            "texto": "Observando a evolução no painel, por que um investimento com aportes mensais cresce muito mais rápido do que um investimento onde você apenas guarda o dinheiro inicial e não mexe mais?",
            "opcoes": [
                "Porque o banco te dá um prêmio por visitar o aplicativo todo mês.",
                "Porque os Juros Compostos passam a render juros também sobre os novos depósitos.",
                "Porque a taxa de juros aumenta sozinha com o tempo."
            ],
            "correta": 1,
            "msg_acerto": "Conceito dominado! Essa é a essência dos investimentos. Os juros trabalham sobre o montante atualizado, então cada novo depósito aumenta a base de cálculo para o mês seguinte.\n\n✨ Progresso Salvo! Fase 6 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.capital_val = 500
        self.aporte_val = 50
        self.taxa_val = 1
        self.tempo_val = 12
        self.calcular_resultados()
        self.carregar_etapa()
        
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True
        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_etapa(self):
        etapa = self.etapas[self.etapa_atual]
        self.titulo_missao = etapa["titulo"]
        self.texto_missao = etapa["texto"]
        
        self.ids.action_container.clear_widgets()
        
        if etapa["tipo"] == "slider":
            btn = MDRaisedButton(
                text="VERIFICAR PATRIMÔNIO",
                size_hint_x=1,
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(
                    size_hint_y=None,
                    height=dp(65),
                    padding="12dp",
                    radius=[8],
                    md_bg_color=[1, 1, 1, 1],
                    elevation=1,
                    ripple_behavior=True
                )
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                
                label = MDLabel(
                    text=f"[b]{letras[i]}[/b] {opt}",
                    markup=True,
                    font_style="Caption",
                    theme_text_color="Primary"
                )
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_capital(self, valor):
        self.capital_val = valor
        self.calcular_resultados()

    def atualizar_aporte(self, valor):
        self.aporte_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_tempo(self, valor):
        self.tempo_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # Transposição da modelagem matemática de Juros Compostos com Aportes Mensais
        taxa = self.taxa_val / 100
        n = self.tempo_val
        
        # O dinheiro que saiu do bolso = Capital Inicial + (Aporte Mensal * Tempo)
        self.total_investido_calc = self.capital_val + (self.aporte_val * n)
        
        # Cálculo do Montante gerado pelo Capital Inicial
        montante_capital = self.capital_val * ((1 + taxa) ** n)
        
        # Cálculo do Montante gerado pelos Aportes (Fórmula do Valor Futuro de uma Série)
        if taxa > 0:
            montante_aportes = self.aporte_val * (((1 + taxa) ** n - 1) / taxa)
        else:
            montante_aportes = self.aporte_val * n
            
        self.montante_final_calc = montante_capital + montante_aportes
        self.total_juros_calc = self.montante_final_calc - self.total_investido_calc

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.capital_val, self.aporte_val, self.taxa_val, self.tempo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A simulação não bate com os valores da missão. Revise os parâmetros solicitados no texto e ajuste a máquina.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Resposta Exata!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Lembre-se do que acontece quando o Montante do mês passado se torna a nova base de cálculo deste mês.", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.avancar_etapa if acertou else self.fechar_dialog

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="OK", on_release=acao)]
        )
        self.dialog.open()

    def fechar_dialog(self, *args):
        self.dialog.dismiss()

    def avancar_etapa(self, *args):
        self.dialog.dismiss()
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.carregar_etapa()
        else:
            # Salvamento automático do Nível 6
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 6:
                app.nivel_modulo2 = 6
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'