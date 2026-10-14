import webbrowser
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

KV_PLANEJAMENTO = '''
<PlanejamentoScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.97, 1
        
        MDTopAppBar:
            title: "1. Organização Financeira"
            elevation: 2
            left_action_items: [["arrow-left", lambda x: root.voltar()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "24dp"
                size_hint_y: None
                height: self.minimum_height

                # ==========================================
                # O ROBÔ ANIMADO
                # ==========================================
                MDBoxLayout:
                    id: balao_robo
                    opacity: 0
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: "12dp"
                    
                    MDIcon:
                        icon: "robot-outline"
                        font_size: "54sp"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        pos_hint: {"top": 1}
                        
                    MDCard:
                        orientation: 'vertical'
                        md_bg_color: 0.85, 0.92, 0.98, 1
                        radius: [0, 20, 20, 20]
                        padding: "16dp"
                        spacing: "8dp"
                        size_hint_y: None
                        height: self.minimum_height
                        elevation: 1
                        
                        MDLabel:
                            text: "Você sabia que a falta de dinheiro pode ser apenas um BUG (erro) no algoritmo de vida?"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Primary"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            
                        MDLabel:
                            text: "Vamos testar sua capacidade de 'Debugar' (consertar) a rotina financeira de alguns jovens!"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None

                        MDFlatButton:
                            text: "LER MATERIAL TEÓRICO"
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primary_color
                            on_release: root.abrir_pdf_teoria()

                # ==========================================
                # CAÇA AOS BUGS (AS 3 QUESTÕES)
                # ==========================================
                MDLabel:
                    id: titulo_missao
                    opacity: 0
                    text: f"Missão {root.indice_questao + 1} de 3: Caça ao Bug"
                    font_style: "H6"
                    bold: True
                    size_hint_y: None
                    height: self.texture_size[1]

                MDCard:
                    id: card_missao
                    opacity: 0
                    orientation: 'vertical'
                    padding: "16dp"
                    spacing: "12dp"
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [15]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 2
                        
                    MDLabel:
                        text: root.historia_texto
                        font_style: "Body2"
                        theme_text_color: "Error"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None
                        
                    MDLabel:
                        text: root.pergunta_texto
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Primary"
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None

                # Opções como Cartões Interativos (Não cortam o texto e são todos neutros)
                MDBoxLayout:
                    id: box_opcoes
                    opacity: 0
                    orientation: 'vertical'
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDCard:
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "12dp"
                        md_bg_color: 0.9, 0.9, 0.9, 1
                        ripple_behavior: True
                        on_release: root.verificar_resposta(0)
                        MDLabel:
                            text: root.btn_a_texto
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            font_style: "Caption"

                    MDCard:
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "12dp"
                        md_bg_color: 0.9, 0.9, 0.9, 1
                        ripple_behavior: True
                        on_release: root.verificar_resposta(1)
                        MDLabel:
                            text: root.btn_b_texto
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            font_style: "Caption"

                    MDCard:
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "12dp"
                        md_bg_color: 0.9, 0.9, 0.9, 1
                        ripple_behavior: True
                        on_release: root.verificar_resposta(2)
                        MDLabel:
                            text: root.btn_c_texto
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            font_style: "Caption"
                            
                    MDCard:
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "12dp"
                        md_bg_color: 0.9, 0.9, 0.9, 1
                        ripple_behavior: True
                        on_release: root.verificar_resposta(3)
                        MDLabel:
                            text: root.btn_d_texto
                            size_hint_y: None
                            height: self.texture_size[1]
                            text_size: self.width, None
                            font_style: "Caption"
'''

Builder.load_string(KV_PLANEJAMENTO)

class PlanejamentoScreen(MDScreen):
    indice_questao = NumericProperty(0)
    historia_texto = StringProperty("")
    pergunta_texto = StringProperty("")
    btn_a_texto = StringProperty("")
    btn_b_texto = StringProperty("")
    btn_c_texto = StringProperty("")
    btn_d_texto = StringProperty("")
    
    dialog = None

    questoes = [
        {
            "historia": "Lucas ganha R$ 100.\n1. Gasta R$ 40 em lanches\n2. Gasta R$ 30 em figurinhas\n3. Tenta guardar para um jogo de R$ 60, mas o dinheiro nunca dá.",
            "pergunta": "Qual é a melhor forma de REPROGRAMAR a lógica do Lucas?",
            "opcoes": [
                "A) Cortar totalmente os lanches e figurinhas.",
                "B) Pedir mais mesada para os pais.",
                "C) Mover a Ação de 'Guardar R$ 60' para ser a AÇÃO NÚMERO 1.",
                "D) Gastar tudo no primeiro dia para não ter que guardar."
            ],
            "correta": 2,
            "feedback_erro": "Isso não resolve o 'Bug' estrutural de forma inteligente. Tente alterar a ORDEM das ações no algoritmo dele!",
            "feedback_acerto": "Brilhante! Na computação, a ORDEM dos comandos muda tudo. Em finanças também: 'Pague a si mesmo primeiro'!"
        },
        {
            "historia": "Mariana separou exatamente R$ 50 para o lanche da semana. Na quarta, o pneu da bicicleta furou (R$ 15). Ela ficou sem comer na quinta e na sexta.",
            "pergunta": "Qual Bug de programação ocorreu no orçamento da Mariana?",
            "opcoes": [
                "A) Ela usou valores engessados sem criar uma 'Variável de Emergência'.",
                "B) O erro foi ela não ter ido a pé para a escola todos os dias.",
                "C) Ela deveria ter gastado os R$ 50 todos na segunda-feira.",
                "D) Ela deveria ter vendido a bicicleta para comprar lanche."
            ],
            "correta": 0,
            "feedback_erro": "Agir por impulso não é um bom algoritmo financeiro. Onde está a segurança do código?",
            "feedback_acerto": "Exato! Em programação, prevemos erros com comandos de exceção. Em finanças, o nome disso é 'Reserva de Emergência'!"
        },
        {
            "historia": "Pedro foi ao shopping e viu a placa: 'Leve 2, pague 1'. Achou grande vantagem e foi repetindo a compra até o cartão da mãe bloquear.",
            "pergunta": "Qual estrutura lógica falhou na mente do Pedro?",
            "opcoes": [
                "A) Ele deveria ter calculado se a loja estava tendo prejuízo.",
                "B) Ele deveria ter comprado online que é sempre mais barato.",
                "C) Ele parou de comprar muito cedo, deveria ter aproveitado mais.",
                "D) Ele entrou num 'Loop Infinito' sem uma condição de parada (limite de orçamento)."
            ],
            "correta": 3,
            "feedback_erro": "Lembre-se das aulas de lógica: toda repetição (loop) precisa de um limite (condição de parada)!",
            "feedback_acerto": "Perfeito! Ele caiu no 'Loop do Consumo'. Todo algoritmo de gastos precisa de um comando 'SE (gasto < limite)' para funcionar!"
        }
    ]

    def on_enter(self):
        self.indice_questao = 0
        self.carregar_questao()
        
        self.ids.balao_robo.opacity = 0
        self.ids.titulo_missao.opacity = 0
        self.ids.card_missao.opacity = 0
        self.ids.box_opcoes.opacity = 0
        
        anim1 = Animation(opacity=1, duration=0.8)
        anim2 = Animation(opacity=1, duration=0.8)
        anim3 = Animation(opacity=1, duration=0.8)
        
        anim1.start(self.ids.balao_robo)
        Clock.schedule_once(lambda dt: anim2.start(self.ids.titulo_missao), 0.5)
        Clock.schedule_once(lambda dt: anim2.start(self.ids.card_missao), 0.5)
        Clock.schedule_once(lambda dt: anim3.start(self.ids.box_opcoes), 1.0)

    def carregar_questao(self):
        q = self.questoes[self.indice_questao]
        self.historia_texto = q["historia"]
        self.pergunta_texto = q["pergunta"]
        self.btn_a_texto = q["opcoes"][0]
        self.btn_b_texto = q["opcoes"][1]
        self.btn_c_texto = q["opcoes"][2]
        self.btn_d_texto = q["opcoes"][3]

    def abrir_pdf_teoria(self):
        link = "https://seu-link-aqui.com"
        webbrowser.open(link)

    def verificar_resposta(self, opcao_escolhida):
        q = self.questoes[self.indice_questao]
        
        if opcao_escolhida == q["correta"]:
            if self.indice_questao < len(self.questoes) - 1:
                titulo = "Código Compilado!"
                texto = q["feedback_acerto"] + "\n\nPrepare-se para o próximo Bug..."
                self.indice_questao += 1
                self.carregar_questao()
            else:
                titulo = "Sistema Financeiro Salvo!"
                texto = q["feedback_acerto"] + "\n\nVocê eliminou todos os Bugs e otimizou os orçamentos! \n\n⭐ FASE 2 DESBLOQUEADA!"
                
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 2:
                    app.nivel_modulo1 = 2
                    app.save_data()
        else:
            titulo = "Erro de Sintaxe Financeira!"
            texto = q["feedback_erro"]
        
        if not self.dialog:
            self.dialog = MDDialog(
                title=titulo,
                text=texto,
                buttons=[MDFlatButton(text="FECHAR", on_release=lambda x: self.dialog.dismiss())]
            )
        else:
            self.dialog.title = titulo
            self.dialog.text = texto
        
        self.dialog.open()

    def voltar(self):
        self.manager.current = 'modulo1'