from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class AlgoritmosIterativosScreen(MDScreen):
    capital_val = NumericProperty(1000)
    taxa_val = NumericProperty(5.0)
    mes_val = NumericProperty(1)
    
    saldo_anterior = NumericProperty(0)
    juros_mes = NumericProperty(0)
    saldo_atual = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Primeiro Ciclo",
            "texto": "Imagine uma dívida no cartão de crédito de R$ 1.000,00 a uma taxa de 10% ao mês. Ajuste a máquina. Deslize a iteração para o MÊS 1.\n\nQual foi o valor de juros processados APENAS neste primeiro ciclo?",
            "validador": lambda c, t, m: c == 1000 and t == 10.0 and m == 1,
            "msg_acerto": "Isso! No mês 1, o saldo anterior era R$ 1000. O banco aplicou 10% e gerou exatos R$ 100,00 de juros. Fácil, né? Agora prepare-se para o susto."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Bola de Neve no Loop",
            "texto": "Mantenha a Dívida em 1000 e a Taxa em 10%. Agora, sem limpar o saldo, deslize a iteração até o MÊS 12 (1 ano de dívida).\n\nPreste muita atenção na linha vermelha. Qual foi o valor de juros processados SOMENTE durante a execução do mês 12?",
            "validador": lambda c, t, m: c == 1000 and t == 10.0 and m == 12,
            "msg_acerto": "Análise perfeita! Repare a loucura: no mês 1 o banco cobrou R$ 100 de juros. Mas no ciclo 12, por causa da base atualizada, SÓ NAQUELE MÊS ele te cobrou mais de R$ 285 de juros!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO DE COMPUTAÇÃO",
            "texto": "Quando você contrata um financiamento de 30 anos (360 meses), o banco não faz a conta manualmente. Que tipo de comando computacional é responsável por repetir a soma de juros mês após mês até o fim do contrato?",
            "opcoes": [
                "Uma Estrutura Condicional (IF / ELSE).",
                "Um Laço de Repetição ou Iteração (FOR / WHILE).",
                "Uma função matemática linear simples."
            ],
            "correta": 1,
            "msg_acerto": "Lógica aprovada! Um loop 'FOR (mes = 1; mes <= 360)' roda o cálculo atualizando o saldo 360 vezes em frações de segundo. Isso é o coração do sistema bancário!\n\n✨ Fase 7 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.capital_val = 1000
        self.taxa_val = 10.0
        self.mes_val = 1
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
                text="VERIFICAR LOG DE EXECUÇÃO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(80), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_capital(self, valor):
        self.capital_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_mes(self, valor):
        self.mes_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        i = self.taxa_val / 100
        
        # Para saber o que aconteceu ESPECIFICAMENTE no mês selecionado,
        # primeiro calculamos o saldo de TUDO o que aconteceu ATÉ o mês passado.
        self.saldo_anterior = self.capital_val * ((1 + i) ** (self.mes_val - 1))
        
        # O juro do mês atual é aplicado APENAS sobre o saldo anterior (Bola de neve)
        self.juros_mes = self.saldo_anterior * i
        
        # O Saldo Atual é a soma do Mês Anterior com o Juro do Mês Atual
        self.saldo_atual = self.saldo_anterior + self.juros_mes

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.capital_val, self.taxa_val, self.mes_val):
            self.mostrar_popup("Algoritmo Correto!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro no Algoritmo", "Os dados não conferem com o que foi pedido. Revise o Capital, a Taxa e, principalmente, o Mês da Iteração.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Conceito Dominado!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Sintático", "Lembre-se da estrutura que permite repetir um bloco de código várias vezes seguidas.", False)

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
            # Salvando o progresso para a Fase 7!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 7:
                app.nivel_modulo3 = 7
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'