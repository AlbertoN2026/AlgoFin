from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class DecomposicaoScreen(MDScreen):
    nivel_desafio = NumericProperty(0)

    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    titulo_fase = StringProperty("")
    problema_macro = StringProperty("")

    dialog = None
    opcoes_atuais = []

    # Banco de Dados Analítico: Decomposição de Problemas
    fases_decomposicao = [
        {
            "titulo": "Etapa 1: A Aquisição de Longo Prazo",
            "tit_robo": "Módulo de Fragmentação Ativado",
            "fala_robo": "Um problema financeiro complexo pode paralisar o sistema. Aplique a decomposição para fatiá-lo em variáveis menores e computáveis.",
            "problema": "[b]Objetivo:[/b] Comprar um computador de R$ 2.400,00 à vista daqui a 6 meses para evitar juros.",
            "opcoes": [
                {"texto": "Dividir o valor total por 6 para encontrar a meta de poupança mensal (R$ 400,00).", "correta": True},
                {"texto": "Analisar o orçamento atual para cortar R$ 400,00 em despesas supérfluas.", "correta": True},
                {"texto": "Ignorar o planejamento e esperar sobrar R$ 2.400,00 de uma só vez no último mês.", "correta": False},
                {"texto": "Aplicar o dinheiro guardado mensalmente em um investimento seguro para render juros.", "correta": True}
            ],
            "msg_acerto": "Decomposição exata. Você fracionou o objetivo macro em metas mensais (R$ 400), ajustou o fluxo de caixa (cortes) e otimizou o capital (investimento).",
            "msg_erro": "Falha na fragmentação. Esperar o valor total sobrar magicamente não é um algoritmo seguro. Reveja quais passos realmente constroem o resultado."
        },
        {
            "titulo": "Etapa 2: Resgate do Endividamento",
            "tit_robo": "Algoritmo de Contingência",
            "fala_robo": "Quando as dívidas acumulam, o saldo devedor vira uma bola de neve. Fatie o problema de um endividamento múltiplo em etapas executáveis.",
            "problema": "[b]Problema:[/b] Você possui uma dívida no cartão de crédito (juros altos) e uma dívida com um amigo (sem juros). O dinheiro atual não paga ambas.",
            "opcoes": [
                {"texto": "Mapear o valor exato e a taxa de juros de cada dívida.", "correta": True},
                {"texto": "Pagar o amigo primeiro por questões emocionais, deixando o cartão rodar juros compostos.", "correta": False},
                {"texto": "Direcionar todo o capital disponível para amortizar o cartão de crédito (maior taxa).", "correta": True},
                {"texto": "Renegociar o prazo de pagamento com o amigo, explicando a prioridade matemática do cartão.", "correta": True}
            ],
            "msg_acerto": "Otimização validada. Na matemática financeira, a prioridade absoluta deve ser o estancamento da dívida com maior taxa de crescimento (o cartão).",
            "msg_erro": "Erro de priorização. Decisões financeiras devem ser baseadas em dados, não em emoções. A dívida que multiplica mais rápido precisa ser eliminada primeiro."
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()

        # Animações do Robô
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True

        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_fase(self):
        fase = self.fases_decomposicao[self.nivel_desafio]
        self.titulo_fase = fase["titulo"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        self.problema_macro = fase["problema"]
        
        # Resetar as opções e renderizar
        self.opcoes_atuais = []
        for op in fase["opcoes"]:
            self.opcoes_atuais.append({
                "texto": op["texto"],
                "correta": op["correta"],
                "selecionada": False
            })
            
        self.renderizar_opcoes()

    def renderizar_opcoes(self):
        self.ids.container_opcoes.clear_widgets()
        
        for index, op in enumerate(self.opcoes_atuais):
            # Cor muda dependendo se está selecionado
            bg_color = [0.8, 0.9, 0.8, 1] if op["selecionada"] else [1, 1, 1, 1]
            
            card = MDCard(
                size_hint_y=None,
                height=dp(70),
                padding="12dp",
                radius=[8],
                md_bg_color=bg_color,
                elevation=1,
                ripple_behavior=True
            )
            # Ao clicar, altera o status de "selecionada" e re-renderiza
            card.bind(on_release=lambda instance, idx=index: self.alternar_selecao(idx))
            
            label = MDLabel(
                text=op["texto"],
                font_style="Caption",
                theme_text_color="Primary",
                valign="center",
                halign="left"
            )
            card.add_widget(label)
            self.ids.container_opcoes.add_widget(card)

    def alternar_selecao(self, index):
        self.opcoes_atuais[index]["selecionada"] = not self.opcoes_atuais[index]["selecionada"]
        self.renderizar_opcoes()

    def validar_decomposicao(self):
        fase = self.fases_decomposicao[self.nivel_desafio]
        
        # Verifica se todas as corretas foram selecionadas E nenhuma incorreta foi selecionada
        acertou_tudo = True
        for op in self.opcoes_atuais:
            if op["correta"] and not op["selecionada"]:
                acertou_tudo = False # Faltou marcar uma certa
            if not op["correta"] and op["selecionada"]:
                acertou_tudo = False # Marcou uma armadilha
                
        if acertou_tudo:
            titulo = "Decomposição Validada"
            texto = fase["msg_acerto"]

            if self.nivel_desafio < len(self.fases_decomposicao) - 1:
                botao_acao = self.avancar_fase
            else:
                texto += "\n\nProcessamento finalizado. A decomposição de problemas é a chave para transformar impossibilidades matemáticas em planos de ação.\n\n✨ FASE 8 DESBLOQUEADA ✨"
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 8:
                    app.nivel_modulo1 = 8
                    app.save_data()
                botao_acao = self.concluir_laboratorio
        else:
            titulo = "Erro de Fatiamento"
            texto = fase["msg_erro"] + "\n\nO sistema desmarcará suas opções. Tente separar novamente os passos úteis das falhas lógicas."
            botao_acao = self.game_over

        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="ENTENDIDO", on_release=botao_acao)]
        )
        self.dialog.open()

    def avancar_fase(self, *args):
        self.dialog.dismiss()
        self.nivel_desafio += 1
        self.carregar_fase()

    def game_over(self, *args):
        self.dialog.dismiss()
        # Reseta as seleções para o aluno tentar de novo
        for op in self.opcoes_atuais:
            op["selecionada"] = False
        self.renderizar_opcoes()

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'