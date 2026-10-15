from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import NumericProperty, StringProperty

class PorcentagemScreen(MDScreen):
    nivel_desafio = NumericProperty(0)
    
    titulo_fase = StringProperty("")
    icone_fase = StringProperty("")
    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    
    cenario_texto = StringProperty("")
    texto_opcao_a = StringProperty("")
    texto_opcao_b = StringProperty("")
    
    dialog = None

    # O Banco de Dados de Investigação Matemática
    fases_porcentagem = [
        {
            "titulo": "Nível 1: A Ilusão Matemática",
            "icone": "brightness-percent",
            "tit_robo": "Análise de Flutuação de Preço",
            "fala_robo": "Muitas lojas alteram os preços antes de aplicar descontos. A sua missão é analisar se a matemática apresentada no anúncio é simétrica.",
            "cenario": "Um smartphone custava R$ 1.000,00. Na véspera de uma promoção, a loja aumentou o preço em 20%. No dia seguinte, a loja anunciou um desconto de 20% sobre o novo preço.",
            "opcao_a": "O preço final voltou para R$ 1.000,00.",
            "opcao_b": "O preço final ficou em R$ 960,00.",
            "resposta_correta": "B",
            "msg_acerto": "Análise exata. A porcentagem não é simétrica porque a base de cálculo muda. O aumento de 20% sobre R$ 1.000 resulta em R$ 1.200. O desconto de 20% incide sobre R$ 1.200 (R$ 240), resultando em R$ 960.",
            "msg_erro": "Erro de cálculo. Lembre-se que a base de cálculo mudou. O desconto de 20% incide sobre o valor já com aumento (R$ 1.200), e não sobre os R$ 1.000 iniciais."
        },
        {
            "titulo": "Nível 2: Batalha de Ofertas",
            "icone": "storefront-outline",
            "tit_robo": "Percentual vs. Valor Absoluto",
            "fala_robo": "O cérebro humano costuma ser atraído por números percentuais grandes. Sua tarefa é calcular o custo efetivo para identificar a melhor decisão econômica.",
            "cenario": "Você deseja adquirir um fone de ouvido.\n\nLOJA A: O fone custa R$ 200,00 e possui um desconto de 25%.\n\nLOJA B: O fone custa R$ 180,00 e possui um desconto fixo de R$ 40,00.",
            "opcao_a": "Comprar na Loja A.",
            "opcao_b": "Comprar na Loja B.",
            "resposta_correta": "B",
            "msg_acerto": "Cálculo correto. Embora 25% pareça um desconto mais atrativo (reduzindo o preço para R$ 150), a dedução em valor absoluto da Loja B resulta no menor custo final (R$ 140).",
            "msg_erro": "Inconsistência identificada. Um percentual alto não garante o menor preço se o valor base for maior. A Loja A vende por R$ 150, enquanto a Loja B vende por R$ 140."
        },
        {
            "titulo": "Nível 3: O Custo Oculto",
            "icone": "credit-card-outline",
            "tit_robo": "Identificação de Juros Embutidos",
            "fala_robo": "O termo 'sem juros' é frequentemente utilizado como estratégia de marketing. É necessário aplicar a decomposição lógica para encontrar os custos ocultos de um financiamento.",
            "cenario": "Um computador é anunciado por R$ 2.000,00 para pagamento à vista. A loja oferece a opção de parcelamento 'sem juros' em 10 parcelas fixas de R$ 220,00.",
            "opcao_a": "O parcelamento possui juros embutidos, totalizando R$ 2.200,00.",
            "opcao_b": "O parcelamento não possui juros, pois a loja afirmou no anúncio.",
            "resposta_correta": "A",
            "msg_acerto": "Perfeito. Ao multiplicar 10 x R$ 220, obtemos o montante de R$ 2.200,00. A diferença de R$ 200,00 representa os juros embutidos na operação a prazo.",
            "msg_erro": "Atenção à operação de multiplicação. Ao somar as 10 parcelas de R$ 220,00, o valor final pago pelo consumidor será de R$ 2.200,00, o que comprova a existência de juros sobre o valor à vista."
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()

    def carregar_fase(self):
        fase = self.fases_porcentagem[self.nivel_desafio]
        
        self.titulo_fase = fase["titulo"]
        self.icone_fase = fase["icone"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        self.cenario_texto = fase["cenario"]
        self.texto_opcao_a = fase["opcao_a"]
        self.texto_opcao_b = fase["opcao_b"]

    def processar_escolha(self, escolha):
        fase = self.fases_porcentagem[self.nivel_desafio]
        
        if escolha == fase["resposta_correta"]:
            titulo = "Precisão Algorítmica!"
            texto = fase["msg_acerto"]
            
            if self.nivel_desafio < len(self.fases_porcentagem) - 1:
                botao_acao = self.avancar_fase
            else:
                # Venceu o Laboratório de Porcentagem
                texto += "\n\nVocê concluiu o módulo com excelência, demonstrando proficiência no cálculo e na interpretação de taxas. \n\n✨ FASE 5 DESBLOQUEADA ✨"
                
                # Salva o progresso rigorosamente
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 5:
                    app.nivel_modulo1 = 5
                    app.save_data()
                
                botao_acao = self.concluir_laboratorio
        else:
            titulo = "Divergência Lógica"
            texto = fase["msg_erro"] + "\n\nO sistema reiniciará este cenário para uma nova análise."
            botao_acao = self.game_over

        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="CONTINUAR", on_release=botao_acao)]
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