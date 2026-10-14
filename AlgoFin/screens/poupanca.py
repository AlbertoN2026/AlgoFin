import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp

class PoupancaScreen(MDScreen):
    blocos_selecionados = ListProperty([])
    moedas = NumericProperty(0)
    missao_texto = StringProperty("")
    gabarito_atual = ListProperty([])
    dialog = None

    def on_enter(self):
        if not self.missao_texto:
            self.gerar_novo_desafio()

    def gerar_novo_desafio(self):
        self.limpar_blocos()
        
        mesada = random.choice([50, 80, 100, 120, 150, 200])
        gasto = random.choice([20, 30, 40, 50, 70])
        
        if gasto >= mesada:
            gasto = mesada - 20
            
        sobra = mesada - gasto
        objetivo = sobra * random.choice([3, 4, 5, 6]) 
        
        self.missao_texto = f"Mesada: R$ {mesada}. Gasto: R$ {gasto}. Objetivo: Comprar item de R$ {objetivo}. Monte a logica:"
        
        texto_btn_mesada = f"Var: Mesada = {mesada}"
        texto_btn_gasto = f"Var: Gasto = {gasto}"
        texto_btn_operacao = "Op: Poupanca = Mesada - Gasto"
        texto_btn_loop = f"Loop: Juntar R$ {objetivo}"
        
        # O Gabarito sempre será nesta ordem lógica
        self.gabarito_atual = [
            texto_btn_mesada,
            texto_btn_gasto,
            texto_btn_operacao,
            texto_btn_loop
        ]
        
        # Criamos os "dados" dos blocos com suas respectivas cores
        blocos_disponiveis = [
            {"text": texto_btn_mesada, "color": [0.2, 0.6, 0.2, 1]},
            {"text": texto_btn_gasto, "color": [0.8, 0.2, 0.2, 1]},
            {"text": texto_btn_operacao, "color": [0.2, 0.4, 0.8, 1]},
            {"text": texto_btn_loop, "color": [0.8, 0.6, 0.1, 1]}
        ]
        
        # A MÁGICA ACONTECE AQUI: Embaralha a ordem dos blocos!
        random.shuffle(blocos_disponiveis)
        
        self.desenhar_paleta(blocos_disponiveis)

    def desenhar_paleta(self, blocos):
        paleta = self.ids.paleta_blocos
        paleta.clear_widgets()
        
        # Cria os botões na tela baseados na lista embaralhada
        for bloco in blocos:
            btn = MDRaisedButton(
                text=bloco["text"],
                size_hint_x=1,
                size_hint_y=None,
                height=dp(48),
                font_size="14sp",
                md_bg_color=bloco["color"],
                # Usamos lambda para passar o texto correto para o evento de clique
                on_release=lambda x, t=bloco["text"]: self.adicionar_bloco(t)
            )
            paleta.add_widget(btn)

    def adicionar_bloco(self, tipo_bloco):
        self.blocos_selecionados.append(tipo_bloco)
        self.atualizar_area_trabalho()

    def limpar_blocos(self):
        self.blocos_selecionados.clear()
        self.atualizar_area_trabalho()

    def atualizar_area_trabalho(self):
        app = MDApp.get_running_app()
        area = self.ids.area_trabalho
        area.clear_widgets()
        
        for bloco in self.blocos_selecionados:
            bloco_card = MDCard(
                size_hint_y=None,
                height=dp(40),
                md_bg_color=app.theme_cls.primary_color,
                radius=[dp(8)],
                elevation=1
            )
            lbl = MDLabel(
                text=bloco,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Subtitle2",
                bold=True
            )
            bloco_card.add_widget(lbl)
            area.add_widget(bloco_card)

    def executar_algoritmo(self):
        if self.blocos_selecionados == self.gabarito_atual:
            self.moedas += 10
            titulo = "Algoritmo Correto!"
            texto = f"Excelente! Voce estruturou a logica perfeita.\n\nRecompensa: +10 Moedas\nTotal: {self.moedas} Moedas"
            btn = MDFlatButton(text="PROXIMO DESAFIO", on_release=self.proximo_desafio)
            
        else:
            titulo = "Ops! Encontramos um erro."
            texto = "A sequencia nao esta certa. Lembre-se: defina as Variaveis, depois a Operacao e por fim o Loop."
            btn = MDFlatButton(text="TENTAR DE NOVO", on_release=self.fechar_dialog)

        self.dialog = MDDialog(title=titulo, text=texto, buttons=[btn])
        self.dialog.open()
        

    def fechar_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def proximo_desafio(self, *args):
        self.fechar_dialog()
        self.gerar_novo_desafio()
        app = MDApp.get_running_app()
        
        