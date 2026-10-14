import webbrowser
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation

class OrcamentoScreen(MDScreen):
    nivel_desafio = NumericProperty(0)
    
    # Variáveis Dinâmicas de UI
    titulo_robo = StringProperty("")
    fala_robo = StringProperty("")
    titulo_fase = StringProperty("")
    icone_fase = StringProperty("")
    
    # Variáveis Financeiras
    renda_atual = NumericProperty(0)
    min_moradia = NumericProperty(0)
    min_comida = NumericProperty(0)
    
    val_moradia = NumericProperty(1500)
    val_comida = NumericProperty(1000)
    val_lazer = NumericProperty(1000)
    saldo_atual = NumericProperty(0)
    
    dialog = None

    # O Novo Banco de Dados com 4 Cenários Únicos!
    cenarios = [
        {
            "titulo": "Mês 1: O Boot do Sistema",
            "icone": "power",
            "tit_robo": "Iniciando o Algoritmo Familiar...",
            "fala_robo": "Bem-vindo ao simulador! Uma família funciona como um software: se os gastos forem maiores que a renda, o sistema trava. Ajuste as barras para a conta fechar sem zerar o essencial!",
            "renda": 3000, "min_mor": 800, "min_com": 600
        },
        {
            "titulo": "Mês 2: O Bug da Inflação",
            "icone": "chart-line-variant",
            "tit_robo": "Ataque Hacker nos Preços!",
            "fala_robo": "Alerta! Os preços do supermercado dispararam (Inflação). O custo mínimo de sobrevivência da comida subiu drasticamente. Você terá que sacrificar o lazer se quiser comer!",
            "renda": 3000, "min_mor": 800, "min_com": 1200
        },
        {
            "titulo": "Mês 3: Vazamento de Memória",
            "icone": "alert-decagram",
            "tit_robo": "Alerta Crítico: Imprevisto!",
            "fala_robo": "A geladeira queimou! Consertar sugou grande parte do dinheiro. A renda despencou temporariamente. MODO DE SOBREVIVÊNCIA ATIVADO: Corte tudo o que puder!",
            "renda": 2200, "min_mor": 800, "min_com": 600
        },
        {
            "titulo": "Mês 4: O Grande Upgrade",
            "icone": "rocket-launch",
            "tit_robo": "Investimento a Longo Prazo",
            "fala_robo": "A família decidiu assinar uma internet rápida e pagar um curso de Robótica. A conta de Moradia/Fixos aumentou muito, mas é um sacrifício hoje para um futuro bilionário. Calcule bem!",
            "renda": 2600, "min_mor": 1300, "min_com": 700
        }
    ]

    def on_enter(self):
        self.nivel_desafio = 0
        self.carregar_cenario()
        
        self.ids.balao_robo.opacity = 0
        anim1 = Animation(opacity=1, duration=1)
        anim1.start(self.ids.balao_robo)

    def carregar_cenario(self):
        cenario = self.cenarios[self.nivel_desafio]
        self.titulo_fase = cenario["titulo"]
        self.icone_fase = cenario["icone"]
        self.titulo_robo = cenario["tit_robo"]
        self.fala_robo = cenario["fala_robo"]
        
        self.renda_atual = cenario["renda"]
        self.min_moradia = cenario["min_mor"]
        self.min_comida = cenario["min_com"]
        
        # Bagunça propositalmente as barras para forçar o aluno a consertar
        self.val_moradia = self.min_moradia + 200
        self.val_comida = self.min_comida + 300
        self.val_lazer = 1200
        self.calcular_saldo()

    def calcular_saldo(self):
        total_gastos = self.val_moradia + self.val_comida + self.val_lazer
        self.saldo_atual = self.renda_atual - total_gastos

    def verificar_orcamento(self):
        # Fecha qualquer diálogo antigo que tenha ficado "preso"
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        if self.saldo_atual < 0:
            titulo = "Déficit Detectado!"
            texto = "O orçamento ficou negativo (vermelho). O cartão de crédito vai cobrar juros altos! Reduza os gastos."
            botao_acao = lambda x: self.dialog.dismiss()
        
        elif self.val_moradia < self.min_moradia:
            titulo = "Erro Fatal: Moradia"
            texto = f"Você reduziu tanto os custos fixos que a luz foi cortada! O mínimo deste mês é R$ {self.min_moradia}."
            botao_acao = lambda x: self.dialog.dismiss()
            
        elif self.val_comida < self.min_comida:
            titulo = "Erro Fatal: Alimentação"
            texto = f"A comida acabou na terceira semana do mês! O mínimo exigido é R$ {self.min_comida}. Saúde não se negocia."
            botao_acao = lambda x: self.dialog.dismiss()
            
        else:
            if self.nivel_desafio < 3: # Como agora são 4 meses (0, 1, 2, 3), verificamos se é menor que 3
                titulo = "Cenário Estabilizado!"
                texto = "Brilhante! Você otimizou as equações e salvou a família neste mês.\n\nMas respire fundo... o próximo mês trará novos imprevistos!"
                botao_acao = self.avancar_cenario
            else:
                # VENCEU TODOS OS 4 DESAFIOS
                titulo = "🏆 ARQUITETO FINANCEIRO!"
                texto = "SENSACIONAL! Sobreviver à inflação, consertar imprevistos e investir no futuro... Você provou que a Lógica Computacional é a chave para a riqueza real!\n\n✨ FASE 3 DESBLOQUEADA ✨"
                
                app = MDApp.get_running_app()
                if app.nivel_modulo1 < 3:
                    app.nivel_modulo1 = 3
                    app.save_data()
                
                botao_acao = self.concluir_laboratorio

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="ENTENDIDO", on_release=botao_acao)]
        )
        self.dialog.open()

    def avancar_cenario(self, *args):
        self.dialog.dismiss()
        self.nivel_desafio += 1
        self.carregar_cenario()

    def concluir_laboratorio(self, *args):
        self.dialog.dismiss()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'