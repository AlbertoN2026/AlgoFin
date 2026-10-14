from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation

class PadroesScreen(MDScreen):
    nivel_desafio = NumericProperty(0)

    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    titulo_fase = StringProperty("")
    icone_fase = StringProperty("")

    sequencia_texto = StringProperty("")
    opcao_a = StringProperty("")
    opcao_b = StringProperty("")
    opcao_c = StringProperty("")

    dialog = None

    # Banco de Dados Analítico: Reconhecimento de Padrões
    fases_padroes = [
        {
            "titulo": "Etapa 1: Frequência de Gastos",
            "icone": "coffee-outline",
            "tit_robo": "Padrões de Consumo Invisível",
            "fala_robo": "Pequenos gastos diários formam uma sequência estrita. Analise o padrão de um lanche diário de R$ 10,00 e determine o impacto projetado ao final de 30 dias.",
            "sequencia": "[b]Dia 1:[/b] R$ 10,00\n[b]Dia 2:[/b] R$ 20,00\n[b]Dia 3:[/b] R$ 30,00\n...\n[b]Dia 30:[/b] [color=#D32F2F]???[/color]",
            "opcao_a": "R$ 100,00",
            "opcao_b": "R$ 300,00",
            "opcao_c": "R$ 50,00",
            "resposta_correta": "B",
            "msg_acerto": "Padrão identificado com precisão. A progressão aritmética de razão 10 resulta em R$ 300,00 ao fim do ciclo. O reconhecimento deste padrão demonstra como despesas microscópicas comprometem o orçamento mensal.",
            "msg_erro": "Inconsistência lógica. Se o acúmulo financeiro cresce linearmente em R$ 10,00 por dia, a projeção exige multiplicar esta constante pelo número total de iterações (30 dias)."
        },
        {
            "titulo": "Etapa 2: A Curva do Investimento",
            "icone": "chart-timeline-variant-shimmer",
            "tit_robo": "Análise de Progressão",
            "fala_robo": "A Sequência 1 simula dinheiro guardado sem rendimento. A Sequência 2 ilustra Juros Compostos. Identifique o próximo valor da Sequência 2.",
            "sequencia": "[b]Seq 1 (Linear):[/b] 100 -> 200 -> 300 -> 400\n\n[b]Seq 2 (Composto):[/b] 100 -> 210 -> 331 -> [color=#D32F2F]???[/color]",
            "opcao_a": "464",
            "opcao_b": "400",
            "opcao_c": "431",
            "resposta_correta": "A",
            "msg_acerto": "Cálculo exato. O padrão da Sequência 2 demonstra um crescimento exponencial. Esta curva acelerada é o princípio fundamental da rentabilidade dos investimentos a longo prazo.",
            "msg_erro": "Erro na identificação do padrão. O crescimento composto não é estático. Cada termo é gerado aplicando-se uma taxa multiplicativa ao montante anterior, somada a um novo aporte."
        },
        {
            "titulo": "Etapa 3: Sistema SAC",
            "icone": "bank-outline",
            "tit_robo": "O Padrão da Amortização",
            "fala_robo": "No Sistema de Amortização Constante (SAC), os juros recaem sobre um saldo devedor decrescente, gerando um padrão. Calcule o próximo termo.",
            "sequencia": "[b]Mês 1:[/b] R$ 500,00\n[b]Mês 2:[/b] R$ 480,00\n[b]Mês 3:[/b] R$ 460,00\n[b]Mês 4:[/b] [color=#D32F2F]???[/color]",
            "opcao_a": "R$ 450,00",
            "opcao_b": "R$ 460,00",
            "opcao_c": "R$ 440,00",
            "resposta_correta": "C",
            "msg_acerto": "Lógica impecável. A análise revela uma constante de decaimento exata de R$ 20,00. No algoritmo SAC, as parcelas formam rigorosamente uma progressão aritmética decrescente.",
            "msg_erro": "Desvio no reconhecimento da constante. Observe a variação entre os primeiros meses (-20). A progressão exige que a próxima dedução obedeça estritamente à mesma razão."
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()

        # Ativação das Animações
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True

        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_fase(self):
        fase = self.fases_padroes[self.nivel_desafio]
        self.titulo_fase = fase["titulo"]
        self.icone_fase = fase["icone"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        self.sequencia_texto = fase["sequencia"]
        self.opcao_a = fase["opcao_a"]
        self.opcao_b = fase["opcao_b"]
        self.opcao_c = fase["opcao_c"]

    def processar_escolha(self, escolha):
        fase = self.fases_padroes[self.nivel_desafio]

        if escolha == fase["resposta_correta"]:
            titulo = "Padrão Validado"
            texto = fase["msg_acerto"]

            if self.nivel_desafio < len(self.fases_padroes) - 1:
                botao_acao = self.avancar_fase
            else:
                texto += "\n\nAnálise concluída. O reconhecimento de padrões estruturais é uma competência essencial para interpretar cenários econômicos e antecipar tomadas de decisão.\n\n✨ FASE 7 DESBLOQUEADA ✨"
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 7:
                    app.nivel_modulo1 = 7
                    app.save_data()
                botao_acao = self.concluir_laboratorio
        else:
            titulo = "Inconsistência Lógica"
            texto = fase["msg_erro"] + "\n\nOs dados serão reprocessados para uma nova avaliação analítica."
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
        self.carregar_fase()

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'