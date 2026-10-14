from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import NumericProperty, StringProperty

class ConsumoScreen(MDScreen):
    nivel_desafio = NumericProperty(0)
    orcamento_atual = NumericProperty(0)
    item_atual_index = NumericProperty(0)
    total_itens = NumericProperty(0)
    
    titulo_fase = StringProperty("")
    icone_fase = StringProperty("")
    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    
    nome_produto = StringProperty("")
    preco_produto = NumericProperty(0)
    icone_produto = StringProperty("")
    
    dialog = None

    # O "Tinder" Psicológico: 3 Fases com linguagem imparcial e educativa
    fases_consumo = [
        {
            "titulo": "Nível 1: Classificação Básica",
            "icone": "filter-outline",
            "tit_robo": "Módulo de Análise Ativado",
            "fala_robo": "Nesta etapa, você deve analisar e classificar cada item em duas categorias: o que é essencial para o cotidiano e o que é apenas um desejo secundário.",
            "orcamento": 200,
            "produtos": [
                {"nome": "Material Escolar Básico", "preco": 80, "icon": "pencil-ruler", "tipo": "necessidade", "msg_comprar": "Análise correta. O material escolar é um recurso necessário para o seu desenvolvimento.", "msg_descartar": "Decisão inadequada. Sem os materiais adequados, o rendimento escolar pode ser prejudicado."},
                {"nome": "Tênis de Marca Famosa", "preco": 450, "icon": "shoe-sneaker", "tipo": "desejo", "msg_comprar": "Atenção: O alto valor agregado por uma marca comprometeu seu saldo. Existem opções acessíveis com a mesma função.", "msg_descartar": "Boa escolha. Ao optar por não pagar a mais apenas por uma marca, você preserva o seu orçamento."},
                {"nome": "Lanche Escolar Diário", "preco": 50, "icon": "food-apple", "tipo": "necessidade", "msg_comprar": "Correto. A alimentação regular é uma necessidade básica e inegociável.", "msg_descartar": "Atenção: Privar-se da alimentação básica pode comprometer sua saúde e capacidade de concentração."}
            ]
        },
        {
            "titulo": "Nível 2: Comportamento de Consumo",
            "icone": "brain",
            "tit_robo": "Análise de Estímulos Externos",
            "fala_robo": "As propagandas e o grupo social costumam influenciar nossas decisões. Avalie com cuidado se a compra está sendo motivada por necessidade real ou por fatores externos.",
            "orcamento": 150,
            "produtos": [
                {"nome": "PROMOÇÃO: 3 Capinhas de Celular por R$ 60", "preco": 60, "icon": "cellphone-cog", "tipo": "desejo", "msg_comprar": "Atenção: Adquirir um item sem necessidade apenas porque está com desconto ainda representa uma saída de recursos.", "msg_descartar": "Decisão acertada. Um desconto só se torna vantajoso quando aplicado a algo que você realmente precisa."},
                {"nome": "Remédio para Febre", "preco": 30, "icon": "pill", "tipo": "necessidade", "msg_comprar": "Correto. Despesas ligadas ao cuidado com a saúde são prioritárias.", "msg_descartar": "Atenção: Os cuidados com a saúde são essenciais e não devem ser postergados em um planejamento financeiro."},
                {"nome": "Jaqueta igual à da 'Turma'", "preco": 100, "icon": "jacket", "tipo": "desejo", "msg_comprar": "Aviso: A compra foi motivada pela necessidade de pertencimento ao grupo, e não por utilidade, o que reduziu seu saldo desnecessariamente.", "msg_descartar": "Decisão consciente. Você priorizou o seu planejamento financeiro em vez de ceder à influência do grupo."}
            ]
        },
        {
            "titulo": "Nível 3: Gastos Recorrentes",
            "icone": "ghost-outline",
            "tit_robo": "Identificação de Custos Invisíveis",
            "fala_robo": "Pequenas despesas frequentes ou serviços contínuos esquecidos podem ter um grande impacto no orçamento ao longo do tempo. Avalie com atenção.",
            "orcamento": 120,
            "produtos": [
                {"nome": "Conta de Energia Elétrica", "preco": 90, "icon": "lightbulb-on", "tipo": "necessidade", "msg_comprar": "Correto. Manter as despesas de infraestrutura básica em dia é o alicerce de qualquer orçamento.", "msg_descartar": "Decisão inadequada. O não pagamento interrompe serviços fundamentais para a residência e para o estudo."},
                {"nome": "Item Aleatório em Jogo Online", "preco": 20, "icon": "treasure-chest", "tipo": "desejo", "msg_comprar": "Atenção: Gastos com elementos virtuais imprevisíveis não trazem retorno tangível e podem se tornar um hábito oneroso.", "msg_descartar": "Boa escolha. Você evitou comprometer seus recursos com itens virtuais que não agregam valor real."},
                {"nome": "Assinatura de App sem uso", "preco": 35, "icon": "cellphone-arrow-down", "tipo": "desejo", "msg_comprar": "Aviso: Manter o pagamento de serviços ou assinaturas que não estão sendo utilizados gera desperdício financeiro.", "msg_descartar": "Decisão correta. Cancelar serviços inativos ajuda a otimizar a distribuição do seu saldo."}
            ]
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_fase()

    def carregar_fase(self):
        fase = self.fases_consumo[self.nivel_desafio]
        
        self.titulo_fase = fase["titulo"]
        self.icone_fase = fase["icone"]
        self.titulo_robo = fase["tit_robo"]
        self.fala_robo = fase["fala_robo"]
        
        self.orcamento_atual = fase["orcamento"]
        self.item_atual_index = 0
        self.total_itens = len(fase["produtos"])
        
        self.carregar_produto()

    def carregar_produto(self):
        fase = self.fases_consumo[self.nivel_desafio]
        p = fase["produtos"][self.item_atual_index]
        
        self.nome_produto = p["nome"]
        self.preco_produto = p["preco"]
        self.icone_produto = p["icon"]

    def processar_escolha(self, acao):
        fase = self.fases_consumo[self.nivel_desafio]
        p = fase["produtos"][self.item_atual_index]
        
        # Lógica de Feedback Imparcial
        if acao == "comprar":
            self.orcamento_atual -= p["preco"]
            if p["tipo"] == "necessidade":
                titulo = "Escolha Adequada"
                texto = p["msg_comprar"]
            else:
                titulo = "Atenção: Gasto Evitável"
                texto = p["msg_comprar"]
        else: # descartar
            if p["tipo"] == "desejo":
                titulo = "Orçamento Preservado"
                texto = p["msg_descartar"]
            else:
                titulo = "Atenção: Necessidade Ignorada"
                texto = p["msg_descartar"]

        # Se o dinheiro acabar, reinicia a fase
        if self.orcamento_atual < 0:
            titulo = "Orçamento Insuficiente"
            texto = "O seu saldo não foi suficiente para cobrir os gastos apresentados. Avalie melhor as prioridades para manter o equilíbrio matemático.\n\nA etapa será reiniciada."
            botao_acao = self.game_over
        else:
            if self.item_atual_index < self.total_itens - 1:
                # Vai para o próximo produto da mesma fase
                botao_acao = self.proximo_item
            else:
                # Concluiu a fase com saldo positivo
                if self.nivel_desafio < len(self.fases_consumo) - 1:
                    titulo = "Etapa Concluída"
                    texto = f"Muito bem. Você finalizou esta etapa mantendo um saldo positivo de R$ {self.orcamento_atual:.2f}. Vamos analisar o próximo cenário."
                    botao_acao = self.avancar_fase
                else:
                    # Zerou todas as fases
                    titulo = "Análise Concluída com Sucesso!"
                    texto = "Parabéns. Você demonstrou capacidade lógica para diferenciar necessidades de desejos, mantendo o controle estrutural do seu orçamento perante os estímulos de consumo.\n\n✨ FASE 4 DESBLOQUEADA ✨"
                    
                    app = MDApp.get_running_app()
                    if app.nivel_modulo1 < 4:
                        app.nivel_modulo1 = 4
                        app.save_data()
                        
                    botao_acao = self.concluir_laboratorio

        # Exibe o Pop-up de Feedback
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
            
        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="CONTINUAR", on_release=botao_acao)]
        )
        self.dialog.open()

    def proximo_item(self, *args):
        self.dialog.dismiss()
        self.item_atual_index += 1
        self.carregar_produto()

    def avancar_fase(self, *args):
        self.dialog.dismiss()
        self.nivel_desafio += 1
        self.carregar_fase()

    def game_over(self, *args):
        self.dialog.dismiss()
        # Reinicia a mesma fase para que o aluno reflita sobre a lógica de escolha
        self.carregar_fase() 

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'