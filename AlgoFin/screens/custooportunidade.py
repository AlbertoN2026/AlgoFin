from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.metrics import dp

class CustoOportunidadeScreen(MDScreen):
    opcao_selecionada = NumericProperty(0)
    nome_escolha = StringProperty("NENHUMA (Aguardando)")
    
    ganho_escolha = NumericProperty(0)
    custo_oportunidade = NumericProperty(0)
    lucro_economico = NumericProperty(0)
    cor_lucro = ListProperty([1, 1, 1, 1])
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    # Ganhos definidos na teoria para R$ 10.000 em 1 ano
    ganho_A = 0.0       # Conta Corrente
    ganho_B = 1050.0    # Tesouro Selic (10.5%)
    ganho_C = 5000.0    # Freelance

    etapas = [
        {
            "tipo": "selecao",
            "titulo": "MISSÃO 1: O Ilusionismo da Inércia",
            "texto": "Clique na 'Opção A: Conta Corrente'. Olhe para o painel de Lucro Econômico e clique em 'VERIFICAR DECISÃO'. O que o algoritmo matemático nos mostra sobre não fazer nada?",
            "validador": lambda opt: opt == 1,
            "msg_acerto": "Exatamente! Quem deixa dinheiro parado acha que não perdeu nada (Lucro Contábil = 0). Mas o Lucro Econômico revela que você teve um PREJUÍZO INVISÍVEL de R$ 5.000, pois abriu mão de empreender!"
        },
        {
            "tipo": "selecao",
            "titulo": "MISSÃO 2: O Investidor Passivo",
            "texto": "Agora, clique na 'Opção B: Tesouro Selic'. O seu Lucro Contábil será positivo (+ R$ 1.050). Mas clique em verificar e veja o que o Lucro Econômico revela.",
            "validador": lambda opt: opt == 2,
            "msg_acerto": "Visão Crítica ativada! O banco vai dizer que você lucrou mil reais. Mas, do ponto de vista do Custo de Oportunidade, você ainda teve um prejuízo econômico de quase 4 mil, pois o seu tempo renderia muito mais no freelance."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO TEÓRICA",
            "texto": "Selecione a 'Opção C: Freelance'. Você notará que o Custo de Oportunidade não foi zero, ele foi de R$ 1.050 (a Opção B). O que isso ensina sobre a teoria econômica?",
            "opcoes": [
                "Toda escolha tem um custo de oportunidade associado, não existe 'ganho sem renúncia'.",
                "O custo de oportunidade só existe quando perdemos dinheiro.",
                "O lucro econômico e o lucro contábil são sempre iguais se você trabalhar duro."
            ],
            "correta": 0,
            "msg_acerto": "Medalha de Ouro em Teoria Econômica! Você nunca ganha 'tudo'. Ao escolher o freelance, você abriu mão do sossego e do juro passivo de R$ 1.050. Mas como R$ 5.000 > R$ 1.050, o seu Lucro Econômico foi positivo!\n\n✨ Fase 5 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.opcao_selecionada = 0
        self.nome_escolha = "NENHUMA (Aguardando)"
        self.ganho_escolha = 0
        self.custo_oportunidade = 0
        self.lucro_economico = 0
        self.cor_lucro = [1, 1, 1, 1]
        self.carregar_etapa()

    def carregar_etapa(self):
        etapa = self.etapas[self.etapa_atual]
        self.titulo_missao = etapa["titulo"]
        self.texto_missao = etapa["texto"]
        self.ids.action_container.clear_widgets()
        
        if etapa["tipo"] == "selecao":
            btn = MDRaisedButton(
                text="VERIFICAR DECISÃO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(85), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def selecionar_opcao(self, opcao):
        self.opcao_selecionada = opcao
        
        # Algoritmo de Custo de Oportunidade
        # O Custo de Oportunidade é o valor da MELHOR alternativa não escolhida.
        
        if opcao == 1:
            self.nome_escolha = "CONTA CORRENTE"
            self.ganho_escolha = self.ganho_A
            # As opções rejeitadas são B e C. A melhor delas é C (5000)
            self.custo_oportunidade = max(self.ganho_B, self.ganho_C)
            
        elif opcao == 2:
            self.nome_escolha = "TESOURO SELIC"
            self.ganho_escolha = self.ganho_B
            # As opções rejeitadas são A e C. A melhor delas é C (5000)
            self.custo_oportunidade = max(self.ganho_A, self.ganho_C)
            
        elif opcao == 3:
            self.nome_escolha = "FREELANCE"
            self.ganho_escolha = self.ganho_C
            # As opções rejeitadas são A e B. A melhor delas é B (1050)
            self.custo_oportunidade = max(self.ganho_A, self.ganho_B)

        self.lucro_economico = self.ganho_escolha - self.custo_oportunidade
        
        # Formatação Visual
        if self.lucro_economico > 0:
            self.cor_lucro = [0.4, 0.8, 0.4, 1] # Verde
        elif self.lucro_economico < 0:
            self.cor_lucro = [0.9, 0.3, 0.3, 1] # Vermelho
        else:
            self.cor_lucro = [0.8, 0.8, 0.8, 1] # Cinza

    def validar_missao(self, *args):
        if self.opcao_selecionada == 0:
            self.mostrar_popup("Alerta", "Você precisa clicar em uma das opções A, B ou C antes de verificar.", False)
            return
            
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.opcao_selecionada):
            self.mostrar_popup("Decisão Modelada!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A sua escolha não atende ao pedido na missão. Tente escolher a opção correta.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Excelente!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Lembre-se: nenhum cenário escapa da teoria da escassez. Toda escolha é uma renúncia.", False)

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
            # Salvando o progresso para a Fase 5!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 5:
                app.nivel_modulo3 = 5
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'