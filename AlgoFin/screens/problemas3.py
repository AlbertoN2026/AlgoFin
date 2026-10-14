from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp

class Problemas3Screen(MDScreen):
    unidades_val = NumericProperty(100)
    
    receita_calc = NumericProperty(0)
    custo_total_calc = NumericProperty(0)
    lucro_calc = NumericProperty(0)
    cor_lucro = ListProperty([0.9, 0.3, 0.3, 1])
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    # Parâmetros da Questão 14 da OBMF (Livraria Saber)
    PRECO_VENDA = 50.00
    CUSTO_FIXO = 7800.00
    CUSTO_VARIAVEL = 20.00

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: Questão 14 (OBMF)",
            "texto": "A Livraria Saber tem um Custo Fixo de R$ 7.800 (aluguel/salários). Cada livro custa R$ 20 para ser feito e é vendido por R$ 50.\n\nAjuste as unidades vendidas no painel. Quantos livros exatos eles precisam vender para atingir o Ponto de Equilíbrio (Lucro Líquido = R$ 0,00)?",
            "validador": lambda u: u == 260,
            "msg_acerto": "Lógica exata! A cada livro vendido, a loja ganha R$ 30 livres (Margem de Contribuição). Dividindo o custo fixo de 7.800 por 30, descobrimos que são necessários exatamente 260 livros só para pagar as contas!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Meta de Lucro",
            "texto": "A dona da livraria quer ter um Lucro Líquido de exatos R$ 4.200,00 neste mês.\n\nDeslize o controle e descubra: quantas unidades ela precisa vender para bater essa meta financeira?",
            "validador": lambda u: u == 400,
            "msg_acerto": "Investigação Perfeita! Para ter 4.200 de lucro, ela precisa cobrir os 7.800 de custo fixo, o que dá uma necessidade total de 12.000. Dividindo por 30 (margem), chegamos aos 400 livros vendidos!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO 26 (OBMF)",
            "texto": "Uma empresa vende camisetas por R$ 20. O custo fixo é R$ 500 e o custo para fabricar cada camiseta é R$ 10. Sendo 'x' o número de camisetas, qual equação representa o ponto de equilíbrio (Receita = Custo)?",
            "opcoes": [
                "A equação é 20x = 500 - 10x.",
                "A equação é 20x = 500 + 10x.",
                "A equação é 20x - 500 = 10x."
            ],
            "correta": 1,
            "msg_acerto": "Medalhista OBMF! A Receita (20x) deve ser igual ao Custo Fixo (500) mais o Custo Variável (10x). Resolvendo: 20x - 10x = 500 -> 10x = 500 -> x = 50 camisetas.\n\n✨ A Fase Final (10) Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.unidades_val = 100
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
                text="VERIFICAR DRE", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(70), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_unidades(self, valor):
        self.unidades_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # Matemática Corporativa (DRE Simplificado)
        self.receita_calc = self.unidades_val * self.PRECO_VENDA
        self.custo_total_calc = self.CUSTO_FIXO + (self.unidades_val * self.CUSTO_VARIAVEL)
        self.lucro_calc = self.receita_calc - self.custo_total_calc
        
        # Colorindo o Lucro/Prejuízo
        if self.lucro_calc > 0:
            self.cor_lucro = [0.4, 0.8, 0.4, 1] # Verde (Lucro)
        elif self.lucro_calc < 0:
            self.cor_lucro = [0.9, 0.3, 0.3, 1] # Vermelho (Prejuízo)
        else:
            self.cor_lucro = [0.8, 0.8, 0.8, 1] # Cinza (Empate / Break-Even)

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.unidades_val):
            self.mostrar_popup("Missão Cumprida!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência Analítica", "Os números não batem. Observe atentamente a linha do 'LUCRO LÍQUIDO' e deslize até encontrar o valor solicitado.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Lógica Impecável!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Algébrico", "Lembre-se da fórmula: Receita = Custo Fixo + (Custo Variável Unitário * Quantidade).", False)

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
            # Salvando o progresso para a Fase 10!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 10:
                app.nivel_modulo3 = 10
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'