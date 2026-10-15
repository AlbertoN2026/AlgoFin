from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class DescontosScreen(MDScreen):
    preco_val = NumericProperty(100)
    desconto_val = NumericProperty(0)
    
    valor_desconto_calc = NumericProperty(0)
    preco_final_calc = NumericProperty(100)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    # Banco de Missões Progressivas de Desconto
    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Material Escolar",
            "texto": "Uma papelaria vende um kit de materiais por [b]R$ 300,00[/b]. Para alunos do Clube de Matemática, eles oferecem [b]15% de desconto[/b].\n\nAjuste a máquina para descobrir: Qual será o [b]Preço Final[/b] que você vai pagar no caixa?",
            "validador": lambda p, d: p == 300 and d == 15,
            "msg_acerto": "Cálculo perfeito! Você poupou R$ 45,00 e o preço final ficou em R$ 255,00. O fator de multiplicação foi 0,85."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: Engenharia Reversa",
            "texto": "Um celular custava [b]R$ 800,00[/b] na vitrine. Ao chegar no caixa, o vendedor disse: 'Para você, faço por [b]R$ 600,00[/b]'.\n\nQual foi a [b]taxa de desconto[/b] que ele aplicou? Ajuste o Preço para 800 e mova o slider de Desconto até o Preço Final marcar 600.",
            "validador": lambda p, d: p == 800 and d == 25,
            "msg_acerto": "Lógica validada! Para um produto de R$ 800 cair para R$ 600, o desconto foi de R$ 200, o que equivale exatamente a 25% do valor original."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO FINAL: A Ilusão da Vitrine",
            "texto": "Uma loja de sapatos fez a seguinte promoção de Black Friday: 'Ganhe 20% de desconto hoje e, se pagar no PIX, ganhe MAIS 20% de desconto sobre o valor com desconto!'\n\nIsso significa que o desconto total da loja será de 40%?",
            "opcoes": [
                "Sim! 20% + 20% soma 40% de desconto exato.",
                "Não. O desconto real será de 36%.",
                "Não. O desconto real será de 44%."
            ],
            "correta": 1,
            "msg_acerto": "Excelente abstração matemática! Descontos sucessivos não se somam. Se algo custa 100, tira 20% = 80. Depois tira 20% de 80 = 64. O desconto total foi de 36, e não de 40!\n\n✨ Fase 3 (Inflação) Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.preco_val = 100
        self.desconto_val = 0
        self.calcular_resultados()
        self.carregar_etapa()
        
        # Animação flutuante do Robô
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
                text="CONFIRMAR VALORES",
                size_hint_x=1,
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            # Opções de Múltipla Escolha
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(
                    size_hint_y=None,
                    height=dp(50),
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

    def calcular_resultados(self):
        # Matemática: Valor Poupado = Preço * (Desconto / 100)
        self.valor_desconto_calc = self.preco_val * (self.desconto_val / 100)
        self.preco_final_calc = self.preco_val - self.valor_desconto_calc

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.preco_val, self.desconto_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Os parâmetros não resolvem o problema atual. Ajuste o Preço de Etiqueta e o Desconto corretamente no simulador.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Resposta Exata!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Pegadinha do mercado! O segundo desconto é aplicado sobre o valor que JÁ está com desconto, e não sobre o preço original. Tente de novo!", False)

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
            # Desbloqueia o Módulo 2, Fase 3 (Inflação)
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 3:
                app.nivel_modulo2 = 3
                app.save_data()
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'