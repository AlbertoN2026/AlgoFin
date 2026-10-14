from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class EquivalenciaScreen(MDScreen):
    divida_futura_val = NumericProperty(5000)
    taxa_val = NumericProperty(1.0)
    meses_val = NumericProperty(12)
    
    valor_presente_calc = NumericProperty(0)
    desconto_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Abatimento Justo",
            "texto": "O Clube de Matemática tem um boleto de R$ 5.000 para pagar daqui a 12 meses. Eles decidiram pagar hoje!\n\nAjuste o Valor Futuro para 5000, o Tempo para 12 meses e considere a Taxa de Juros do mercado como 2.0%. Qual deve ser o valor matemático JUSTO cobrado hoje?",
            "validador": lambda d, t, m: d == 5000 and 1.9 < t < 2.1 and m == 12,
            "msg_acerto": "Lógica exata! Retirando os juros embutidos (desconto racional composto), os R$ 5.000 daqui a 1 ano equivalem a cerca de R$ 3.942 pagos hoje."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Pegadinha do Banco",
            "texto": "Você tem um financiamento de R$ 10.000 para pagar em 6 meses (Antecipação: 6). A taxa do contrato é de 3.0% ao mês.\n\nO banco liga oferecendo um 'super desconto': 'Pague hoje por R$ 9.000,00'. Ajuste a máquina. Esse acordo é bom para você?",
            "validador": lambda d, t, m: d == 10000 and 2.9 < t < 3.1 and m == 6,
            "msg_acerto": "Visão crítica! O painel mostra que o valor justo seria em torno de R$ 8.374. O banco está fingindo te dar um desconto, mas na verdade está cobrando mais do que a dívida vale hoje!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OLITEF",
            "texto": "Ao utilizarmos a equivalência de capitais para trazer um Valor Futuro para o Presente, o que acontece com o Valor Presente se a Taxa de Juros (i) da economia aumentar muito?",
            "opcoes": [
                "O Valor Presente fica MAIOR, encarecendo a dívida hoje.",
                "O Valor Presente fica MENOR, pois o 'peso' dos juros retirados do futuro será maior.",
                "O Valor Presente não se altera, pois a dívida original já estava fechada."
            ],
            "correta": 1,
            "msg_acerto": "Pensamento estruturado impecável! É por isso que, quando a taxa Selic sobe, os títulos de renda fixa perdem valor de mercado (marcação a mercado). Quanto maior a taxa, menor o valor presente!\n\n✨ Fase 4 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.divida_futura_val = 5000
        self.taxa_val = 1.0
        self.meses_val = 12
        self.calcular_resultados()
        self.carregar_etapa()
        
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + Animation(elevation=1, duration=1.5, transition='in_out_sine')
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
                text="VERIFICAR VALOR PRESENTE", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(85), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_divida(self, valor):
        self.divida_futura_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_meses(self, valor):
        self.meses_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # VP = VF / (1 + i)^n
        i = self.taxa_val / 100
        n = self.meses_val
        
        self.valor_presente_calc = self.divida_futura_val / ((1 + i) ** n)
        self.desconto_calc = self.divida_futura_val - self.valor_presente_calc

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.divida_futura_val, self.taxa_val, self.meses_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Os valores no painel não combinam com a missão. Ajuste os sliders de Valor Futuro, Taxa e Antecipação.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Excelente!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro", "Faça o teste prático na máquina acima. Aumente a taxa de juros e observe o que acontece com o 'Justo para pagar hoje'.", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.avancar_etapa if acertou else self.fechar_dialog
        self.dialog = MDDialog(title=titulo, text=texto, buttons=[MDFlatButton(text="OK", on_release=acao)])
        self.dialog.open()

    def fechar_dialog(self, *args):
        self.dialog.dismiss()

    def avancar_etapa(self, *args):
        self.dialog.dismiss()
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.carregar_etapa()
        else:
            # ==========================================================
            # SALVANDO O PROGRESSO PARA A FASE 4! 
            # ==========================================================
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 4:
                app.nivel_modulo3 = 4
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'