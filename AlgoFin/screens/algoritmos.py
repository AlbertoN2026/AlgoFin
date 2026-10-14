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

class AlgoritmosScreen(MDScreen):
    nivel_desafio = NumericProperty(0)
    
    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    titulo_fase = StringProperty("")
    
    dialog = None
    sequencia_correta = []
    sequencia_aluno = []
    blocos_embaralhados = []

    # Os 3 Níveis de Bricolagem Algorítmica
    # Os 5 Níveis de Bricolagem Algorítmica (Mais Conteúdo!)
    fases_algoritmo = [
        {
            "titulo": "Missão 1: O Ciclo de Compras",
            "tit_robo": "Inicializando Lógica Sequencial",
            "fala_robo": "Toda ação financeira possui uma ordem correta para não quebrar o sistema. Como um computador organizaria uma compra inteligente?",
            "blocos_corretos": [
                "1. Receber a mesada",
                "2. Guardar 20% do valor imediatamente",
                "3. Verificar os preços dos produtos desejados",
                "4. Comprar apenas se o saldo for suficiente"
            ],
            "msg_acerto": "Algoritmo Perfeito! Pagar a si mesmo primeiro (guardar os 20%) antes de gastar é a regra de ouro da matemática financeira.",
            "msg_erro": "Bug Detectado na Sequência. Lembre-se: em finanças saudáveis, a poupança deve ocorrer antes do consumo, e nunca com o que 'sobrar'."
        },
        {
            "titulo": "Missão 2: O Saque Bancário",
            "tit_robo": "Condicionais e Segurança",
            "fala_robo": "Quando você usa o caixa eletrônico, a máquina segue um fluxograma estrito para proteger seu dinheiro. Organize esse fluxo.",
            "blocos_corretos": [
                "1. Inserir o cartão no terminal",
                "2. Digitar a senha de autenticação",
                "3. Verificar se o saldo é maior que o valor solicitado",
                "4. Liberar as notas de dinheiro"
            ],
            "msg_acerto": "Fluxo Otimizado! Você compreendeu a estrutura condicional (IF/THEN). O dinheiro só é liberado após a validação do saldo.",
            "msg_erro": "Falha de Segurança! O sistema não pode liberar dinheiro antes de autenticar a senha ou de verificar o saldo em conta."
        },
        {
            "titulo": "Missão 3: Juros Compostos em Loop",
            "tit_robo": "Estruturas de Repetição (Loop)",
            "fala_robo": "A mágica dos Juros Compostos ocorre através da repetição. Organize como a máquina calcula os rendimentos de um investimento mês a mês.",
            "blocos_corretos": [
                "1. Definir o Capital Inicial investido",
                "2. Iniciar o laço de repetição de meses",
                "3. Multiplicar o saldo atual pela taxa de juros",
                "4. Somar o lucro ao montante para o próximo mês"
            ],
            "msg_acerto": "Laço Executado com Sucesso! Você modelou perfeitamente o comportamento dos juros sobre juros (Loops), a força mais poderosa dos investimentos.",
            "msg_erro": "Erro de Iteração. Para gerar Juros Compostos, você precisa iniciar o laço e garantir que os lucros se somem ao montante a cada novo ciclo."
        },
        {
            "titulo": "Missão 4: O Algoritmo da Pechincha",
            "tit_robo": "Comparação de Variáveis",
            "fala_robo": "Antes de comprar algo caro, um consumidor inteligente faz uma pesquisa e compara dados. Monte o fluxo da pechincha perfeita.",
            "blocos_corretos": [
                "1. Identificar a necessidade real do produto",
                "2. Pesquisar o preço em pelo menos 3 lojas diferentes",
                "3. Calcular o valor do frete ou custos extras",
                "4. Escolher a opção com o menor custo total"
            ],
            "msg_acerto": "Excelente! Você criou um algoritmo de otimização de custos. O frete e os custos ocultos sempre devem entrar na conta antes da decisão.",
            "msg_erro": "Cuidado! Comparar preços e incluir custos ocultos (como frete) deve sempre vir antes da decisão de compra."
        },
        {
            "titulo": "Missão 5: Triagem de Dívidas",
            "tit_robo": "Priorização de Dados",
            "fala_robo": "Se você tem várias contas a pagar e pouco dinheiro, qual é a ordem matemática correta? Organize a prioridade.",
            "blocos_corretos": [
                "1. Listar todas as dívidas pendentes",
                "2. Identificar a dívida com a maior taxa de juros",
                "3. Destinar o dinheiro primeiro para a dívida mais cara",
                "4. Renegociar ou parcelar o restante"
            ],
            "msg_acerto": "Lógica impecável! Matematicamente, a dívida com os juros mais altos é a que mais cresce, logo, deve ser eliminada primeiro.",
            "msg_erro": "Erro de Prioridade. Se você não atacar a dívida com a maior taxa de juros primeiro, ela crescerá como uma bola de neve incontrolável."
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()
        
        # ANIMAÇÃO: O Balão flutua suavemente e o Robô "respira"
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.5)
        
        # Animação de flutuação (Aumenta e diminui a sombra do cartão simulando altura)
        anim_flutuar = Animation(elevation=4, duration=1.2, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.2, transition='in_out_sine')
        anim_flutuar.repeat = True
        
        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_fase(self):
        fase = self.fases_algoritmo[self.nivel_desafio]
        
        self.titulo_fase = fase["titulo"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        self.sequencia_correta = fase["blocos_corretos"]
        self.sequencia_aluno = []
        
        # Clona a lista e embaralha a ordem para o aluno organizar
        self.blocos_embaralhados = list(self.sequencia_correta)
        random.shuffle(self.blocos_embaralhados)
        
        self.renderizar_blocos_disponiveis()
        self.renderizar_sequencia()

    def renderizar_blocos_disponiveis(self):
        self.ids.container_blocos.clear_widgets()
        
        for texto_bloco in self.blocos_embaralhados:
            
            # TRUQUE AQUI: Remove o número original (ex: "1. ") para não dar a resposta!
            texto_exibicao = texto_bloco.split('. ', 1)[1] if '. ' in texto_bloco else texto_bloco
            
            # Criação do Bloco Interativo via Python
            card = MDCard(
                size_hint_y=None, 
                height=dp(60), 
                padding="12dp", 
                radius=[8], 
                md_bg_color=[1, 1, 1, 1],
                elevation=1,
                ripple_behavior=True
            )
            # Ao clicar, o bloco dispara a função de adicionar com uma animação (passando o texto original)
            card.bind(on_release=lambda instance, t=texto_bloco: self.adicionar_a_sequencia(t, instance))
            
            label = MDLabel(
                text=texto_exibicao,  # <-- Injeta o texto limpo, sem o número!
                font_style="Caption", 
                bold=True, 
                halign="center",
                theme_text_color="Primary"
            )
            card.add_widget(label)
            self.ids.container_blocos.add_widget(card)

    def renderizar_sequencia(self):
        self.ids.container_sequencia.clear_widgets()
        
        for index, texto_bloco in enumerate(self.sequencia_aluno):
            card = MDCard(
                size_hint_y=None, 
                height=dp(40), 
                padding="12dp", 
                radius=[4], 
                md_bg_color=[0.8, 0.9, 0.8, 1], # Cor verde clara para itens organizados
                elevation=0
            )
            label = MDLabel(
                text=f"{index + 1}º -> {texto_bloco.split('. ', 1)[1]}", # Tira o número original para mostrar a ordem do aluno
                font_style="Caption", 
                halign="center",
                theme_text_color="Primary"
            )
            card.add_widget(label)
            self.ids.container_sequencia.add_widget(card)

    def adicionar_a_sequencia(self, texto_bloco, widget_card):
        # Animação 2: O bloco dá um 'pulo' visual ao ser tocado
        anim_pulo = Animation(elevation=3, duration=0.1) + Animation(elevation=1, duration=0.1)
        anim_pulo.start(widget_card)
        
        if texto_bloco not in self.sequencia_aluno:
            self.sequencia_aluno.append(texto_bloco)
            # Remove o bloco da lista de embaralhados e re-renderiza a tela
            self.blocos_embaralhados.remove(texto_bloco)
            self.renderizar_blocos_disponiveis()
            self.renderizar_sequencia()

    def limpar_sequencia(self):
        # Devolve todos os blocos do aluno para a área de embaralhados
        self.blocos_embaralhados.extend(self.sequencia_aluno)
        random.shuffle(self.blocos_embaralhados)
        self.sequencia_aluno = []
        self.renderizar_blocos_disponiveis()
        self.renderizar_sequencia()

    def validar_algoritmo(self):
        fase = self.fases_algoritmo[self.nivel_desafio]
        
        if len(self.sequencia_aluno) < len(self.sequencia_correta):
            self.mostrar_popup("Algoritmo Incompleto", "Você precisa organizar todos os blocos disponíveis antes de compilar o código.")
            return

        if self.sequencia_aluno == self.sequencia_correta:
            titulo = "Compilação Bem Sucedida!"
            texto = fase["msg_acerto"]
            
            if self.nivel_desafio < len(self.fases_algoritmo) - 1:
                acao = self.avancar_fase
            else:
                texto += "\n\nVocê dominou a arte de organizar variáveis financeiras em fluxos lógicos! \n\n✨ FASE 6 DESBLOQUEADA ✨"
                
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 6:
                    app.nivel_modulo1 = 6
                    app.save_data()
                acao = self.concluir_laboratorio
        else:
            titulo = "Erro de Lógica!"
            texto = fase["msg_erro"] + "\n\nRevise as etapas e tente compilar novamente."
            self.limpar_sequencia()
            acao = lambda x: self.dialog.dismiss()

        self.mostrar_popup(titulo, texto, acao)

    def mostrar_popup(self, titulo, texto, acao=None):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        if acao is None:
            acao = lambda x: self.dialog.dismiss()
            
        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="OK", on_release=acao)]
        )
        self.dialog.open()

    def avancar_fase(self, *args):
        self.dialog.dismiss()
        self.nivel_desafio += 1
        self.carregar_fase()

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'