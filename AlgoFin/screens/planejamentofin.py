from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class PlanejamentoFinScreen(MDScreen):
    renda_val = NumericProperty(2000)
    necessidades_val = NumericProperty(1000)
    desejos_val = NumericProperty(600)
    
    poupanca_calc = NumericProperty(400)
    
    perc_necessidades = NumericProperty(50)
    perc_desejos = NumericProperty(30)
    perc_poupanca = NumericProperty(20)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Primeiro Salário",
            "texto": "O Carlos conseguiu um estágio ganhando [b]R$ 1.000,00[/b]. Ele quer seguir a regra 50-30-20 à risca.\n\nAjuste a Renda Mensal para 1000. Depois, ajuste os gastos para que as porcentagens no painel fiquem EXATAMENTE em 50% Necessidades, 30% Desejos e 20% Poupança.",
            "validador": lambda r, n, d, p: r == 1000 and n == 500 and d == 300,
            "msg_acerto": "Orçamento perfeitamente equilibrado! Ele gastará R$ 500 com o básico, R$ 300 com lazer e garantirá R$ 200 para o futuro todos os meses."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: Corte de Gastos",
            "texto": "A Renda da família Silva é de [b]R$ 3.000,00[/b]. Eles estão gastando [b]R$ 1.800,00 em Necessidades[/b] (60%).\n\nAjuste a Renda para 3000 e as Necessidades para 1800. Para que a Poupança atinja os 20% obrigatórios, para quanto eles devem reduzir os [b]Desejos[/b]?",
            "validador": lambda r, n, d, p: r == 3000 and n == 1800 and d == 600,
            "msg_acerto": "Corte cirúrgico! Se as necessidades estão altas (60%), o único jeito de salvar os 20% da poupança é sacrificando o lazer, reduzindo os desejos para 20% (R$ 600)."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO FINAL: A Função da Poupança",
            "texto": "Na regra 50-30-20, a última fatia de 20% do orçamento é sagrada. Do ponto de vista da Educação Financeira, qual é o principal objetivo de separar esse dinheiro todo mês?",
            "opcoes": [
                "Para poder gastar tudo no shopping no final do ano.",
                "Criar uma reserva de emergência e investir para o futuro.",
                "Para pagar contas básicas atrasadas."
            ],
            "correta": 1,
            "msg_acerto": "Pensamento a longo prazo validado! A poupança protege você de imprevistos e usa a força dos Juros Compostos a seu favor.\n\n✨ Progresso Salvo! Fase 5 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.renda_val = 2000
        self.necessidades_val = 1000
        self.desejos_val = 600
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
                text="VERIFICAR ORÇAMENTO",
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
                    height=dp(60),
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

    def atualizar_renda(self, valor):
        self.renda_val = valor
        self.calcular_resultados()

    def atualizar_necessidades(self, valor):
        self.necessidades_val = valor
        self.calcular_resultados()

    def atualizar_desejos(self, valor):
        self.desejos_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # A poupança é o que sobra da renda
        self.poupanca_calc = self.renda_val - self.necessidades_val - self.desejos_val
        
        if self.renda_val > 0:
            self.perc_necessidades = (self.necessidades_val / self.renda_val) * 100
            self.perc_desejos = (self.desejos_val / self.renda_val) * 100
            self.perc_poupanca = (self.poupanca_calc / self.renda_val) * 100
        else:
            self.perc_necessidades = 0
            self.perc_desejos = 0
            self.perc_poupanca = 0

    def validar_missao(self, *args):
        # Impede que a poupança seja negativa (ficar devendo)
        if self.poupanca_calc < 0:
            self.mostrar_popup("Alerta de Endividamento!", "Você está gastando mais do que ganha! Reduza as necessidades ou os desejos.", False)
            return

        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.renda_val, self.necessidades_val, self.desejos_val, self.poupanca_calc):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "O orçamento ainda não bate com a regra solicitada na missão. Ajuste os sliders com cuidado.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Resposta Exata!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Lembre-se: a poupança é a fundação do crescimento patrimonial. Tente de novo!", False)

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
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 5:
                app.nivel_modulo2 = 5
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'