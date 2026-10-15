import json
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

class DesafiosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questoes = []
        self.indice_atual = 0
        self.premiadas = set()   # questões que já deram moedas nesta sessão

    def on_enter(self):
        self.carregar_dados()

    def carregar_dados(self):
        diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_json = os.path.join(diretorio_base, "data", "desafios_olimpicos.json")
        
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.questoes = dados.get("questoes", [])
            
            if self.questoes:
                self.carregar_questao()
        except FileNotFoundError:
            self.ids.lbl_pergunta.text = f"Erro: Arquivo JSON não encontrado em:\n{caminho_json}"

    def carregar_questao(self):
        self.ids.lbl_feedback.text = ""
        
        if not self.questoes:
            return

        questao = self.questoes[self.indice_atual]
        
        self.ids.lbl_origem.text = questao["origem"]
        self.ids.lbl_tema.text = questao["tema"]
        self.ids.lbl_pergunta.text = questao["pergunta"]
        
        self.ids.box_opcoes.clear_widgets()
        
        for opcao in questao["opcoes"]:
            card_opcao = MDCard(
                orientation="vertical",
                padding="15dp",
                size_hint_x=1,
                size_hint_y=None,
                radius=[8],
                elevation=1,
                line_color=(0.2, 0.5, 0.8, 1),
                md_bg_color=(0.95, 0.95, 0.97, 1)
            )
            # A mágica no Python: Força o Card a acompanhar a altura do que tem dentro
            card_opcao.bind(minimum_height=card_opcao.setter('height'))
            
            lbl_texto = MDLabel(
                text=opcao,
                theme_text_color="Primary",
                size_hint_y=None
            )
            # A mágica no Python: Força o Texto a calcular a quebra de linha corretamente
            lbl_texto.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
            
            card_opcao.add_widget(lbl_texto)
            card_opcao.bind(on_release=lambda x, opt=opcao: self.verificar_resposta(opt))
            self.ids.box_opcoes.add_widget(card_opcao)

    def verificar_resposta(self, opcao_escolhida):
        questao = self.questoes[self.indice_atual]
        self.ids.lbl_feedback.markup = True
        if opcao_escolhida == questao["correta"]:
            # Retorno que explica a decisão, e não só o veredito
            retorno = questao.get("retorno", "")
            if self.indice_atual not in self.premiadas:
                self.premiadas.add(self.indice_atual)
                # SALVANDO O PROGRESSO E AS MOEDAS!
                app = MDApp.get_running_app()
                app.moedas += 10
                app.save_data()
                premio = " +10 moedas"
            else:
                premio = ""
            self.ids.lbl_feedback.text = (
                f"[color=#2E7D32][b]Resposta correta!{premio}[/b]\n{retorno}[/color]")
        else:
            self.ids.lbl_feedback.text = ("[color=#C62828]Ainda não. Releia o enunciado ou "
                                          "toque em DICA DA TEORIA e tente de novo.[/color]")

    def mostrar_dica(self):
        questao = self.questoes[self.indice_atual]
        self.ids.lbl_feedback.text = f"[color=#E65100][b]Conceito Teórico:[/b] {questao['dica_ia']}[/color]"
        self.ids.lbl_feedback.markup = True

    def proxima_questao(self):
        if self.questoes:
            self.indice_atual += 1
            if self.indice_atual >= len(self.questoes):
                self.indice_atual = 0  # Reinicia o loop se acabar as questões
            self.carregar_questao()

    def voltar(self):
        self.manager.current = 'inicial'