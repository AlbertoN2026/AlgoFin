from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class AnaliseInvestScreen(MDScreen):
    opcao_selecionada = NumericProperty(0)
    nome_empresa = StringProperty("NENHUMA (Aguardando)")
    
    roi_calc = NumericProperty(0)
    payback_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    # Dados das Empresas (Investimento_Inicial, Lucro_Anual)
    empresas = {
        1: {"nome": "PADARIA DE BAIRRO", "inv": 50000, "lucro": 30000},
        2: {"nome": "STARTUP DE APP", "inv": 200000, "lucro": 40000},
        3: {"nome": "FRANQUIA FAST FOOD", "inv": 150000, "lucro": 150000}
    }

    etapas = [
        {
            "tipo": "selecao",
            "titulo": "MISSÃO 1: O Pior Investimento",
            "texto": "Nem tudo que brilha é ouro. A 'Startup de App' parece moderna e dá 40 mil reais de lucro por ano. Clique nela e verifique o painel.\n\nDepois clique em VERIFICAR para provar que você identificou o perigo escondido nela.",
            "validador": lambda opt: opt == 2,
            "msg_acerto": "Análise perfeita! O investimento inicial dela é gigante (200 mil). Isso faz o ROI ser péssimo (apenas 20% ao ano) e o Payback ser absurdamente longo (60 meses / 5 anos). É uma armadilha financeira!"
        },
        {
            "tipo": "selecao",
            "titulo": "MISSÃO 2: O Retorno Relâmpago",
            "texto": "A 'Padaria de Bairro' dá menos lucro nominal que a Startup (30 mil vs 40 mil). Mas avalie os indicadores.\n\nQual das três empresas do painel devolve o dinheiro investido mais rápido (Menor Payback)? Selecione-a e verifique.",
            "validador": lambda opt: opt == 3,
            "msg_acerto": "Tubarão dos Negócios! A Franquia devolve 100% do seu dinheiro em exatos 12 meses (1 ano). Depois disso, tudo o que entrar é lucro livre."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OLITEF / B3",
            "texto": "Um empresário investiu R$ 100.000,00 e o negócio tem um ROI constante de 25% ao ano. Sem considerar a inflação, qual será o Payback (em anos) desse investimento?",
            "opcoes": [
                "2 anos.",
                "4 anos.",
                "25 anos."
            ],
            "correta": 1,
            "msg_acerto": "Lógica exata! Se a empresa devolve 25% do investimento por ano (ROI = 25%), serão precisos exatamente 4 anos (25% x 4 = 100%) para recuperar todo o capital inicial investido.\n\n✨ Fase 6 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.opcao_selecionada = 0
        self.nome_empresa = "NENHUMA (Aguardando)"
        self.roi_calc = 0
        self.payback_calc = 0
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
        
        if etapa["tipo"] == "selecao":
            btn = MDRaisedButton(
                text="VERIFICAR INVESTIMENTO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
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

    def selecionar_empresa(self, opcao):
        self.opcao_selecionada = opcao
        empresa = self.empresas[opcao]
        
        self.nome_empresa = empresa["nome"]
        
        # Cálculo do ROI = (Lucro_Anual / Investimento) * 100
        self.roi_calc = (empresa["lucro"] / empresa["inv"]) * 100
        
        # Cálculo do Payback em Meses = (Investimento / Lucro_Mensal)
        lucro_mensal = empresa["lucro"] / 12
        self.payback_calc = empresa["inv"] / lucro_mensal

    def validar_missao(self, *args):
        if self.opcao_selecionada == 0:
            self.mostrar_popup("Alerta", "Selecione uma empresa clicando nos cartões antes de verificar.", False)
            return
            
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.opcao_selecionada):
            self.mostrar_popup("Decisão Modelada!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Essa não é a resposta correta para a missão. Clique em outra empresa.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Excelente!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Matemático", "Faça a conta: Se devolve 25% ao ano, quantos anos demora para chegar em 100%?", False)

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
            # Salvando o progresso para a Fase 6!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 6:
                app.nivel_modulo3 = 6
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'