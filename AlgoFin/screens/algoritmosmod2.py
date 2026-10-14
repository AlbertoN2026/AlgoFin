from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp

class AlgoritmosMod2Screen(MDScreen):
    preco_val = NumericProperty(1000)
    desconto_val = NumericProperty(10)
    rendimento_val = NumericProperty(1)
    
    saldo_vista_calc = NumericProperty(0)
    saldo_prazo_calc = NumericProperty(0)
    
    veredito_texto = StringProperty("CALCULANDO...")
    veredito_cor = ListProperty([1, 1, 1, 1])
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: A Vantagem do Dinheiro",
            "texto": "Um celular custa [b]R$ 1.000,00[/b]. A loja dá [b]10% de desconto[/b] à vista. Se você parcelar em 1x, você pode deixar os 1.000 reais rendendo no banco a [b]2% ao mês[/b].\n\nConfigure os controles para esses valores e veja o Output. O algoritmo mandou pagar à vista ou parcelar?",
            "validador": lambda p, d, r: p == 1000 and d == 10 and r == 2,
            "msg_acerto": "Lógica exata! Como o desconto da loja (10%) é MAIOR que o rendimento do banco (2%), vale muito mais a pena pagar à vista. Sobrou quase R$ 102 no seu bolso."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Armadilha da Loja",
            "texto": "O celular continua custando [b]R$ 1.000,00[/b]. Mas agora a loja ofereceu um desconto de apenas [b]1%[/b] à vista, e o seu banco está pagando [b]5%[/b] de rendimento.\n\nAjuste a máquina. O que o algoritmo recomenda fazer agora?",
            "validador": lambda p, d, r: p == 1000 and d == 1 and r == 5,
            "msg_acerto": "Análise perfeita! Como o rendimento do banco (5%) superou o desconto (1%), a árvore de decisão inverteu. É melhor deixar o dinheiro inteiro rendendo no banco e pagar o produto sem desconto no mês seguinte!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OLITEF",
            "texto": "Se a taxa de desconto de uma loja for EXATAMENTE IGUAL à taxa de rendimento mensal da sua conta bancária, o que o algoritmo matemático indicará fazer (analisando o prazo de 1 mês)?",
            "opcoes": [
                "Pagar à vista será melhor.",
                "Pagar parcelado será melhor.",
                "Tanto faz, o saldo final no bolso será exatamente o mesmo."
            ],
            "correta": 0,
            "msg_acerto": "Isso mesmo! Atenção à matemática fina: se você paga à vista com 10% de desconto (Sobra R$ 100). Ao investir esses 100 a 10%, no fim do mês você tem R$ 110. No parcelado, você investe R$ 1000 a 10% (= R$ 1100), mas tem que pagar a dívida de R$ 1000, sobrando apenas R$ 100. Pagar à vista vence!\n\n✨ Fase 8 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.preco_val = 1000
        self.desconto_val = 10
        self.rendimento_val = 1
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
                text="EXECUTAR ALGORITMO",
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
                    height=dp(80),
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

    def atualizar_preco(self, valor):
        self.preco_val = valor
        self.calcular_resultados()

    def atualizar_desconto(self, valor):
        self.desconto_val = valor
        self.calcular_resultados()

    def atualizar_rendimento(self, valor):
        self.rendimento_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        p = self.preco_val
        d = self.desconto_val / 100
        r = self.rendimento_val / 100
        
        # Cenário A (À Vista): Paga com desconto. O dinheiro que sobrou rende 1 mês no banco.
        desconto_reais = p * d
        self.saldo_vista_calc = desconto_reais * (1 + r)
        
        # Cenário B (A Prazo 1x): O dinheiro todo rende no banco por 1 mês, depois subtrai o preço cheio.
        self.saldo_prazo_calc = (p * (1 + r)) - p
        
        # Algoritmo Condicional (IF / ELSE)
        if self.saldo_vista_calc > self.saldo_prazo_calc:
            self.veredito_texto = "À VISTA!"
            self.veredito_cor = [0.4, 0.8, 0.4, 1] # Verde
        elif self.saldo_prazo_calc > self.saldo_vista_calc:
            self.veredito_texto = "A PRAZO (INVISTA)!"
            self.veredito_cor = [0.9, 0.7, 0.2, 1] # Amarelo/Laranja
        else:
            self.veredito_texto = "TANTO FAZ"
            self.veredito_cor = [0.8, 0.8, 0.8, 1] # Cinza

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.preco_val, self.desconto_val, self.rendimento_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A simulação não bate com os valores da missão. Revise os parâmetros solicitados.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Medalha Garantida!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Lógico", "Teste na máquina! Coloque o desconto em 10% e o rendimento em 10%. Quem deixa mais dinheiro sobrando na linha do Output?", False)

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
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 8:
                app.nivel_modulo2 = 8
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'