from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class AmortizacaoScreen(MDScreen):
    financiamento_val = NumericProperty(200000)
    taxa_val = NumericProperty(1.0)
    prazo_val = NumericProperty(120)
    
    sac_primeira = NumericProperty(0)
    sac_ultima = NumericProperty(0)
    sac_juros_total = NumericProperty(0)
    
    price_primeira = NumericProperty(0)
    price_ultima = NumericProperty(0)
    price_juros_total = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: Quem paga mais juros?",
            "texto": "Simule a compra de um imóvel financiando R$ 300.000,00. Ajuste a taxa para 1.0% ao mês e o prazo para 360 meses (30 anos).\n\nOlhe no painel: Qual dos dois sistemas cobra MENOS juros no total e qual cobra MAIS?",
            "validador": lambda f, t, p: f == 300000 and 0.9 < t < 1.1 and p == 360,
            "msg_acerto": "Lógica exata! A Tabela SAC cobrou R$ 541 mil de juros. Já a Tabela Price cobrou R$ 745 mil. A SAC é sempre mais barata a longo prazo!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Armadilha da Parcela",
            "texto": "Mantenha os mesmos R$ 300.000 a 1.0% em 360x.\nSe a Tabela SAC é muito mais barata no final, por que a maioria das pessoas escolhe a Tabela Price? Olhe para o valor da '1ª Parcela' de cada um.",
            "validador": lambda f, t, p: f == 300000 and 0.9 < t < 1.1 and p == 360,
            "msg_acerto": "Visão crítica! A 1ª parcela do SAC (R$ 3.833) é muito mais cara que a do Price (R$ 3.086). Os bancos usam a Tabela Price para 'caber' a parcela no salário do cliente, mas ele acaba pagando muito mais juros no total."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO BANCÁRIA",
            "texto": "O que caracteriza matematicamente o funcionamento do Sistema SAC?",
            "opcoes": [
                "As parcelas são sempre do mesmo valor do início ao fim.",
                "O valor da amortização (abate da dívida) é constante, e os juros vão caindo, fazendo a parcela diminuir mês a mês.",
                "Os juros aumentam a cada mês, deixando a parcela mais cara no final."
            ],
            "correta": 1,
            "msg_acerto": "Perfeito! O termo SAC significa Sistema de Amortização Constante. Como você abate o mesmo valor da dívida todo mês, os juros despencam rapidamente!\n\n✨ Fase 3 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.financiamento_val = 200000
        self.taxa_val = 1.0
        self.prazo_val = 120
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
                text="VERIFICAR COMPARAÇÃO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
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

    def atualizar_financiamento(self, valor):
        self.financiamento_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_prazo(self, valor):
        self.prazo_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        pv = self.financiamento_val
        i = self.taxa_val / 100
        n = self.prazo_val
        
        if n > 0:
            # Cálculos SAC
            amortizacao_sac = pv / n
            self.sac_primeira = amortizacao_sac + (pv * i)
            self.sac_ultima = amortizacao_sac + (amortizacao_sac * i)
            # Soma de uma P.A. para os juros SAC
            self.sac_juros_total = (pv * i) * (n + 1) / 2
            
            # Cálculos PRICE
            if i > 0:
                pmt_price = pv * i / (1 - (1 + i)**-n)
            else:
                pmt_price = pv / n
            self.price_primeira = pmt_price
            self.price_ultima = pmt_price
            self.price_juros_total = (pmt_price * n) - pv

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.financiamento_val, self.taxa_val, self.prazo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A simulação não bate com os valores da missão. Ajuste os sliders de Financiamento, Taxa e Prazo.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Excelente!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro", "Analise bem o painel. Se a parcela vai de um valor alto para um valor baixo, o que aconteceu com os juros?", False)

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
            # Salvando o progresso para o Nível 3!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 3:
                app.nivel_modulo3 = 3
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'