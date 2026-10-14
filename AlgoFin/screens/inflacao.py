from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class InflacaoScreen(MDScreen):
    preco_val = NumericProperty(100)
    inflacao_val = NumericProperty(1)
    tempo_val = NumericProperty(1)
    
    preco_corrigido_calc = NumericProperty(0)
    diferenca_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    # Banco de Missões de Inflação (Juros Compostos Reversos)
    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: A Cesta Básica",
            "texto": "Uma cesta básica de alimentos custa hoje [b]R$ 100,00[/b]. Se a inflação do país for cravada em [b]10% ao ano[/b], ajuste a máquina para descobrir: Qual será o preço dessa mesma cesta daqui a [b]2 anos[/b]?",
            "validador": lambda p, i, n: p == 100 and i == 10 and n == 2,
            "msg_acerto": "Cálculo exato! A matemática é exponencial: 100 reais + 10% no primeiro ano = 110. Depois, 110 + 10% no segundo ano = 121 reais. As coisas estão mais caras!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: Viagem no Tempo",
            "texto": "Em um jogo de videogame antigo, um item custava [b]R$ 50,00[/b]. Passaram-se exatos [b]3 anos[/b] e, devido à inflação constante, hoje esse mesmo item custa [b]R$ 66,55[/b].\n\nFaça a engenharia reversa: Ajuste o Preço para 50, o Tempo para 3 anos, e mova a Inflação até o Preço Corrigido marcar R$ 66,55. Qual foi a inflação anual?",
            "validador": lambda p, i, n: p == 50 and n == 3 and i == 10,
            "msg_acerto": "Abstração de alto nível! O fator multiplicador escondido na economia desse jogo era uma inflação constante de 10% a cada ano."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO FINAL: Salário x Inflação",
            "texto": "Imagine que você arrumou um emprego e, no final do ano, recebeu um aumento de [b]5%[/b] no seu salário. Porém, naquele mesmo ano, a inflação do Brasil foi de [b]8%[/b].\n\nO que aconteceu com você na vida real?",
            "opcoes": [
                "Fiquei mais rico, pois meu salário aumentou.",
                "Perdi poder de compra, pois as coisas subiram mais que o meu salário.",
                "Não mudou nada, as contas se anulam."
            ],
            "correta": 1,
            "msg_acerto": "Visão Crítica desbloqueada! Essa é a maior ilusão financeira de todas. Se o seu salário sobe menos que a inflação, você na verdade ficou mais pobre, pois seu dinheiro compra menos coisas.\n\n✨ Progresso Salvo! Fase 4 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.preco_val = 100
        self.inflacao_val = 1
        self.tempo_val = 1
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
                text="CONFIRMAR MODELAGEM",
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

    def atualizar_preco(self, valor):
        self.preco_val = valor
        self.calcular_resultados()

    def atualizar_inflacao(self, valor):
        self.inflacao_val = valor
        self.calcular_resultados()

    def atualizar_tempo(self, valor):
        self.tempo_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # Fórmula dos Juros Compostos: M = P * (1 + i/100)^t
        fator = (1 + (self.inflacao_val / 100)) ** self.tempo_val
        self.preco_corrigido_calc = self.preco_val * fator
        self.diferenca_calc = self.preco_corrigido_calc - self.preco_val

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.preco_val, self.inflacao_val, self.tempo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Os parâmetros não resolvem o problema atual. Ajuste o Preço Base, a Inflação e o Tempo na máquina acima.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Resposta Exata!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Cuidado! O seu poder de compra depende da relação entre o que você ganha e o quanto as coisas custam. Pense com cuidado.", False)

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
            # ==========================================================
            # AQUI ESTÁ O CÓDIGO QUE GARANTE O SALVAMENTO DO PROGRESSO!
            # ==========================================================
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 4:
                app.nivel_modulo2 = 4
                app.save_data() # Grava o nível 4 fisicamente no data.json
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'