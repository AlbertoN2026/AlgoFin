import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class ProblemasOlitefScreen(MDScreen):
    acertos_val = NumericProperty(0)
    
    titulo_questao = StringProperty("")
    texto_questao = StringProperty("")
    
    dialog = None
    questao_atual = None
    questoes_disponiveis = []

    # Banco de Questões extraído dos PDFs
    banco_questoes = [
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Antes da invenção do ___, as pessoas trocavam um bem pelo outro em uma atividade conhecida como ___. O primeiro produto usado como dinheiro foi o ___, de onde vem o nome ___.",
            "opcoes": [
                "Pix, escambo, açúcar, troca.",
                "real, escambo, papel, rendimento.",
                "escambo, dinheiro, sal, salário.",
                "dinheiro, escambo, sal, salário."
            ],
            "correta": 3
        },
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Carolina entrou no site do Banco Central e viu que a Taxa Selic estava em 13,25% ao ano. Isso significa que:",
            "opcoes": [
                "A inflação no último ano foi de 13,25%.",
                "A taxa básica de juros na economia é de 13,25%.",
                "O mercado de ações irá crescer 13,25% no próximo ano.",
                "A taxa máxima para os empréstimos no Brasil é de 13,25%."
            ],
            "correta": 1
        },
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Sob o regime de juros ___, o dinheiro cresce de maneira linear. Sob o regime de juros ___, o dinheiro cresce de forma ___. No Brasil, o regime de juros ___ é o mais usado.",
            "opcoes": [
                "composto, simples, exponencial, simples.",
                "simples, composto, crescente, simples.",
                "simples, composto, exponencial, composto."
            ],
            "correta": 2
        },
        {
            "titulo": "QUESTÃO OBMF",
            "texto": "Vovô Mário, de 65 anos, tem R$ 30.000 guardados e quer investir para não perder o poder de compra com o tempo. Ele é cuidadoso e não quer correr riscos. Qual opção é a mais adequada?",
            "opcoes": [
                "O CDB a 95% do CDI, porque ele rende mais que a poupança e é seguro.",
                "Ação de uma loja de roupas, porque ela pode dar muito lucro se a empresa crescer.",
                "O Tesouro Selic, porque ele é seguro, rende de acordo com a taxa básica de juros e ajuda a proteger da inflação."
            ],
            "correta": 2
        },
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Yasmin aplicou R$ 1.000,00 que sempre rende R$ 100,00 a cada ano. Flávia fez o mesmo investimento, mas dobrou de valor em seis anos. O título de Flávia paga juros ___ enquanto o de Yasmin paga juros ___.",
            "opcoes": [
                "Yasmin - Juros Simples e Flávia - Juros Compostos.",
                "Yasmin - Juros Compostos e Flávia - Juros Simples.",
                "Yasmin - Juros Simples e Flávia - Juros Complexos."
            ],
            "correta": 0
        },
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Alex comprou 'pedacinhos' de uma empresa, Domingos comprou um fundo que possuía os mesmos ativos que o índice Ibovespa B3 e Leôncio investiu em títulos ligados ao Agronegócio. Qual ativo cada um comprou?",
            "opcoes": [
                "Alex - FII; Domingos - Fiagro; Leôncio - Ações.",
                "Alex - Ações; Domingos - ETF; Leôncio - Fiagro.",
                "Alex - ETF; Domingos - FII; Leôncio - Fiagro."
            ],
            "correta": 1
        },
        {
            "titulo": "QUESTÃO OLITEF (Nível 1)",
            "texto": "Sobre Tesouro Selic x Poupança: I. O Tesouro Selic tem rentabilidade diária. II. A poupança é mais segura que o Tesouro Selic. III. A poupança é isenta do imposto de renda. Quais afirmativas estão corretas?",
            "opcoes": [
                "I e II.",
                "I, II e III.",
                "I e III."
            ],
            "correta": 2
        }
    ]

    def on_enter(self):
        self.acertos_val = 0
        self.questoes_disponiveis = list(self.banco_questoes)
        random.shuffle(self.questoes_disponiveis)
        
        self.carregar_nova_questao()
        
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True
        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_nova_questao(self):
        # Se as questões acabarem, embaralha de novo (garante o looping)
        if not self.questoes_disponiveis:
            self.questoes_disponiveis = list(self.banco_questoes)
            random.shuffle(self.questoes_disponiveis)
            
        self.questao_atual = self.questoes_disponiveis.pop(0)
        self.titulo_questao = self.questao_atual["titulo"]
        self.texto_questao = self.questao_atual["texto"]
        
        self.ids.action_container.clear_widgets()
        
        letras = ["A) ", "B) ", "C) ", "D) ", "E) "]
        for i, opt in enumerate(self.questao_atual["opcoes"]):
            card = MDCard(
                size_hint_y=None,
                height=dp(85),
                padding="12dp",
                radius=[8],
                md_bg_color=[1, 1, 1, 1],
                elevation=1,
                ripple_behavior=True
            )
            card.bind(on_release=lambda instance, idx=i: self.validar_resposta(idx))
            
            label = MDLabel(
                text=f"[b]{letras[i]}[/b] {opt}",
                markup=True,
                font_style="Caption",
                theme_text_color="Primary"
            )
            card.add_widget(label)
            self.ids.action_container.add_widget(card)

    def validar_resposta(self, index_escolhido):
        if index_escolhido == self.questao_atual["correta"]:
            self.acertos_val += 1
            if self.acertos_val >= 5:
                self.mostrar_popup("🏆 VOCÊ VENCEU O MÓDULO II!", "Sensacional! Você dominou o Simulador, a Matemática Financeira e os Juros Compostos. Você está pronto para investir no mundo real!", True)
            else:
                self.mostrar_popup("Resposta Exata!", "Muito bem, lógica financeira aplicada com sucesso! Faltam poucas para a vitória.", False)
        else:
            self.mostrar_popup("Ops, resposta incorreta!", "Preste atenção aos fundamentos de juros e economia. Tente a próxima questão para recuperar seus pontos!", False)

    def mostrar_popup(self, titulo, texto, zerou_modulo):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.finalizar_modulo if zerou_modulo else self.continuar_jogo

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="OK", on_release=acao)]
        )
        self.dialog.open()

    def continuar_jogo(self, *args):
        self.dialog.dismiss()
        self.carregar_nova_questao()
        
    def finalizar_modulo(self, *args):
        self.dialog.dismiss()
        app = MDApp.get_running_app()
        # Salva o nível máximo ou libera o próximo grande módulo
        if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 10:
            app.nivel_modulo2 = 10
            app.save_data() 
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'