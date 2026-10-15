from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp
import random

class AbstracaoScreen(MDScreen):
    nivel_desafio = NumericProperty(0)

    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    titulo_fase = StringProperty("")
    historia_texto = StringProperty("")

    dialog = None
    dados_atuais = []

    # Banco de Dados Analítico: Abstração (Filtro de Ruídos)
    fases_abstracao = [
        {
            "titulo": "Etapa 1: A Compra do Carro",
            "tit_robo": "Filtro de Gatilhos Emocionais",
            "fala_robo": "O mercado usa emoções para ofuscar a matemática. Ignore a estética e identifique as variáveis essenciais para calcular o montante da dívida.",
            "historia": "O vendedor Carlos, muito simpático, ofereceu um [b]carro esportivo vermelho metálico[/b] maravilhoso, com bancos de couro, por [b]R$ 40.000,00[/b]. O modelo é o favorito do ano e atinge 200 km/h. Para fechar negócio hoje, ele faz o financiamento em [b]36 meses[/b], cobrando uma taxa de [b]2% ao mês[/b].",
            "dados": [
                {"texto": "Capital (PV): R$ 40.000,00", "relevante": True},
                {"texto": "Taxa de Juros (i): 2% ao mês", "relevante": True},
                {"texto": "Prazo (n): 36 meses", "relevante": True},
                {"texto": "Cor do Veículo: Vermelho Metálico", "relevante": False},
                {"texto": "Velocidade Máxima: 200 km/h", "relevante": False},
                {"texto": "Vendedor: Carlos", "relevante": False}
            ],
            "msg_acerto": "Abstração concluída com precisão! Para a matemática de juros compostos, a cor e a velocidade do carro são ruídos. O algoritmo só processa o Capital (PV), a Taxa (i) e o Tempo (n).",
            "msg_erro": "Sobrecarga de dados inúteis. Você incluiu informações que não alteram o cálculo financeiro. O modelo matemático não processa cores ou emoções, apenas números operacionais."
        },
        {
            "titulo": "Etapa 2: A Viagem de Formatura",
            "tit_robo": "Filtro de Variáveis de Planejamento",
            "fala_robo": "Um planejamento financeiro seguro exige foco. Identifique no relato abaixo quais dados você realmente precisa para estruturar a sua meta de poupança mensal.",
            "historia": "Uma turma de [b]30 alunos[/b] do 9º ano quer muito viajar para uma [b]praia paradisíaca no Nordeste[/b] em dezembro. O pacote de viagem custa exatos [b]R$ 3.000,00 por aluno[/b]. Faltam [b]10 meses[/b] para a data. O professor sugeriu colocar o dinheiro em uma aplicação segura que rende [b]1% ao mês[/b]. A mala escolhida pelos alunos custa R$ 300,00.",
            "dados": [
                {"texto": "Meta Financeira (FV): R$ 3.000,00", "relevante": True},
                {"texto": "Tempo para o resgate (n): 10 meses", "relevante": True},
                {"texto": "Rendimento da Aplicação (i): 1% ao mês", "relevante": True},
                {"texto": "Destino: Praia no Nordeste", "relevante": False},
                {"texto": "Tamanho da turma: 30 alunos", "relevante": False},
                {"texto": "Preço da mala (Acessório externo): R$ 300,00", "relevante": False}
            ],
            "msg_acerto": "Otimização perfeita! O seu objetivo de poupança individual depende apenas da Meta final, dos Meses restantes e da Taxa da aplicação. O destino e a mala não entram na fórmula do montante.",
            "msg_erro": "Ruído detectado. Elementos como o destino da viagem ou a quantidade de amigos são contextuais, mas matematicamente irrelevantes para a equação do valor futuro."
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()

        # Animações de flutuação e respiração
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True

        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_fase(self):
        fase = self.fases_abstracao[self.nivel_desafio]
        self.titulo_fase = fase["titulo"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        self.historia_texto = fase["historia"]
        
        # Carrega os dados, adiciona o status e embaralha
        self.dados_atuais = []
        for dado in fase["dados"]:
            self.dados_atuais.append({
                "texto": dado["texto"],
                "relevante": dado["relevante"],
                "selecionada": False
            })
        
        random.shuffle(self.dados_atuais)
        self.renderizar_dados()

    def renderizar_dados(self):
        self.ids.container_dados.clear_widgets()
        
        for index, dado in enumerate(self.dados_atuais):
            # Cor azulada suave se estiver selecionado
            bg_color = [0.75, 0.85, 0.95, 1] if dado["selecionada"] else [1, 1, 1, 1]
            
            card = MDCard(
                size_hint_y=None,
                height=dp(50),
                padding="12dp",
                radius=[8],
                md_bg_color=bg_color,
                elevation=1,
                ripple_behavior=True
            )
            card.bind(on_release=lambda instance, idx=index: self.alternar_selecao(idx))
            
            label = MDLabel(
                text=dado["texto"],
                font_style="Caption",
                bold=dado["selecionada"],
                theme_text_color="Primary",
                valign="center",
                halign="center"
            )
            card.add_widget(label)
            self.ids.container_dados.add_widget(card)

    def alternar_selecao(self, index):
        self.dados_atuais[index]["selecionada"] = not self.dados_atuais[index]["selecionada"]
        self.renderizar_dados()

    def validar_abstracao(self):
        fase = self.fases_abstracao[self.nivel_desafio]
        
        acertou_tudo = True
        for dado in self.dados_atuais:
            if dado["relevante"] and not dado["selecionada"]:
                acertou_tudo = False # Faltou um dado importante
            if not dado["relevante"] and dado["selecionada"]:
                acertou_tudo = False # Adicionou ruído
                
        if acertou_tudo:
            titulo = "Dados Extraídos!"
            texto = fase["msg_acerto"]

            if self.nivel_desafio < len(self.fases_abstracao) - 1:
                botao_acao = self.avancar_fase
            else:
                texto += "\n\nVocê concluiu o módulo de Abstração! Ignorar a emoção e extrair a lógica matemática é a principal defesa contra as armadilhas financeiras.\n\n✨ FASE 9 DESBLOQUEADA ✨"
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 9:
                    app.nivel_modulo1 = 9
                    app.save_data()
                botao_acao = self.concluir_laboratorio
        else:
            titulo = "Erro no Filtro Lógico"
            texto = fase["msg_erro"] + "\n\nO sistema desmarcará os dados. Refaça a extração focando estritamente na equação."
            botao_acao = self.game_over

        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="COMPREENDIDO", on_release=botao_acao)]
        )
        self.dialog.open()

    def avancar_fase(self, *args):
        self.dialog.dismiss()
        self.nivel_desafio += 1
        self.carregar_fase()

    def game_over(self, *args):
        self.dialog.dismiss()
        for dado in self.dados_atuais:
            dado["selecionada"] = False
        self.renderizar_dados()

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'