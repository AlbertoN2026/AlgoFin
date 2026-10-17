import threading
import requests
import json
import re
from kivy.clock import Clock
from config_segura import (obter_chave_api, remover_chave_professor,
                           salvar_chave_professor)
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField

# URL da API do Gemini (sem chave: a chave é lida fora do código, por config_segura.py)
URL_IA = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

MSG_SEM_CHAVE = ("O tutor está desativado neste aparelho porque a chave de acesso "
                 "não foi configurada. Peça ajuda ao professor.")
# Emojis e símbolos que a fonte do aplicativo (Roboto) não tem apareceriam como
# quadrados; setas viram "->" e o restante é removido da resposta do tutor.
SEM_GLIFO = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]")

MSG_SEM_INTERNET = ("Não consegui falar com o tutor: o aparelho parece estar sem "
                    "internet. Os outros módulos do AlgoFin funcionam normalmente.")


class TutorScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.card_digitando = None
        self.historico = []
        self.ocupado = False
        self.dialogo_chave = None

        Clock.schedule_once(self.saudacao, 1)

    def saudacao(self, *args):
        texto = ("Olá! Sou o seu Tutor Cognitivo. Que desafio matemático ou "
                 "computacional vamos investigar hoje?")
        if not obter_chave_api():
            texto += ("\n\n[i]Para usar o tutor, o professor precisa configurar a "
                      "chave de acesso neste aparelho (ícone de chave, no alto da tela).[/i]")
        self.adicionar_balao("Tutor IA", texto, "left")

    def enviar(self):
        msg = self.ids.input_msg.text
        if not msg.strip():
            return
        if self.ocupado:
            Snackbar(text="Aguarde a resposta do tutor.").open()
            return

        self.ids.input_msg.text = ""
        self.adicionar_balao("Você", msg, "right")
        self.mostrar_digitando()
        self.ocupado = True

        # Inicia a thread para não travar a tela enquanto a IA pensa
        threading.Thread(target=self.chamar_api, args=(msg,), daemon=True).start()

    def mostrar_digitando(self):
        self.card_digitando = MDCard(
            size_hint=(0.4, None), height="50dp", padding="10dp",
            radius=[15, 15, 15, 0], md_bg_color=(0.9, 0.9, 0.9, 1)
        )
        self.card_digitando.add_widget(MDSpinner(size_hint=(None, None), size=("20dp", "20dp"), active=True))
        self.ids.chat_list.add_widget(self.card_digitando)
        Clock.schedule_once(lambda dt: setattr(self.ids.chat_scroll, 'scroll_y', 0))

    def chamar_api(self, msg):
        # ==========================================================
        # O CÉREBRO PEDAGÓGICO DO ALGOFIN (PROMPT DE SISTEMA)
        # ==========================================================
        contexto_pedagogico = (
            "Atue ESTRITAMENTE como um Tutor Cognitivo Socrático do aplicativo AlgoFin. "
            "Seu público são alunos do 9º ano. O seu objetivo é ensinar Matemática Financeira (Juros, Poupança, SAC) "
            "integrada ao Pensamento Computacional (Loops, Variáveis, Algoritmos). "
            "REGRAS ABSOLUTAS: "
            "1. NUNCA dê a resposta numérica final pronta. Seu papel é ser um 'andaime cognitivo'. "
            "2. MÉTODOS SOCRÁTICO: Sempre devolva uma pergunta reflexiva que faça o aluno pensar no próximo passo da resolução. "
            "3. DECOMPOSIÇÃO: Ajude o aluno a quebrar problemas grandes em partes menores. "
            "4. LINGUAGEM COMPUTACIONAL: Faça analogias entre o dinheiro e a programação. "
            "5. Responda de forma amigável, encorajadora e em no máximo 2 parágrafos curtos."
        )

        chave = obter_chave_api()
        if not chave:
            self.responder(MSG_SEM_CHAVE)
            return

        # Adiciona a pergunta atual na memória com o formato exigido pelo Gemini
        self.historico.append({"role": "user", "parts": [{"text": msg}]})

        # Estrutura completa da requisição (só o texto da conversa: o perfil
        # do estudante — nome, escola, turma — não é enviado)
        payload = {
            "system_instruction": {
                "parts": [{"text": contexto_pedagogico}]
            },
            "contents": self.historico
        }

        try:
            headers = {'Content-Type': 'application/json', 'x-goog-api-key': chave}
            r = requests.post(URL_IA, headers=headers, data=json.dumps(payload), timeout=20)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.historico.pop()
            self.responder(MSG_SEM_INTERNET)
            return
        except requests.exceptions.RequestException:
            self.historico.pop()
            self.responder("O tutor não conseguiu responder agora. Tente de novo em instantes.")
            return

        if r.status_code != 200:
            self.historico.pop()  # remove a pergunta para não quebrar o fluxo da conversa
            if r.status_code == 429:
                texto = "Muitos acessos ao mesmo tempo! Aguarde alguns segundos e tente de novo."
            elif r.status_code in (400, 401, 403):
                texto = ("A chave de acesso configurada neste aparelho não foi aceita "
                         "(pode ter sido revogada). Peça ajuda ao professor.")
            else:
                texto = (f"O tutor não conseguiu responder agora (erro {r.status_code}). "
                         "Tente de novo em instantes.")
            self.responder(texto)
            return

        try:
            txt = r.json()['candidates'][0]['content']['parts'][0]['text']
        except (ValueError, KeyError, IndexError, TypeError):
            self.historico.pop()
            self.responder("O tutor enviou uma resposta vazia. Tente perguntar de outro jeito.")
            return

        # Salva a resposta da IA na memória (o Gemini usa o role 'model')
        self.historico.append({"role": "model", "parts": [{"text": txt}]})

        # Limpeza e formatação de texto para o KivyMD (Negrito e Itálico)
        txt = txt.replace('\\n', '\n')
        txt = txt.replace('`', '').replace('\u2192', '->').replace('\u2190', '<-')
        txt = SEM_GLIFO.sub('', txt)
        txt = re.sub(r'\*\*(.*?)\*\*', r'[b]\1[/b]', txt)
        txt = re.sub(r'\*(.*?)\*', r'[i]\1[/i]', txt)

        self.responder(txt)

    def responder(self, texto):
        """Chamado na thread da rede: agenda a resposta na thread da interface.
        (O texto é passado como argumento padrão para que a função agendada
        não dependa de variáveis que deixam de existir ao fim do bloco except.)"""
        Clock.schedule_once(lambda dt, t=texto: self.finalizar(t))

    def finalizar(self, texto):
        self.ocupado = False
        if self.card_digitando:
            self.ids.chat_list.remove_widget(self.card_digitando)
            self.card_digitando = None

        self.adicionar_balao("Tutor IA", texto, "left")

    def adicionar_balao(self, autor, texto, lado):
        cor = (0.9, 0.9, 1, 1) if lado == "right" else (1, 1, 1, 1)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.85, None),
            padding="12dp",
            radius=[15],
            md_bg_color=cor,
            pos_hint={lado: 1},
            elevation=1
        )

        lbl = MDLabel(
            text=f"[b]{autor}[/b]\n{texto}",
            markup=True,
            adaptive_height=True
        )

        card.add_widget(lbl)

        # Regra de ouro para o card esticar junto com o tamanho do texto
        lbl.bind(texture_size=lambda instance, size: setattr(card, 'height', size[1] + 24))

        self.ids.chat_list.add_widget(card)
        Clock.schedule_once(lambda dt: setattr(self.ids.chat_scroll, 'scroll_y', 0), 0.1)

    # ==========================================================
    # Configuração da chave pelo professor (fica só neste aparelho)
    # ==========================================================
    def abrir_config_chave(self):
        campo = MDTextField(hint_text="Chave de acesso",
                            password=True)
        conteudo = MDBoxLayout(orientation="vertical", spacing="12dp",
                               size_hint_y=None, height="120dp")
        conteudo.add_widget(MDLabel(
            text="Somente para o professor. A chave fica gravada só neste aparelho e não aparece na tela.",
            font_style="Caption", theme_text_color="Secondary"))
        conteudo.add_widget(campo)

        def salvar(*_):
            ok = salvar_chave_professor(campo.text)
            self.dialogo_chave.dismiss()
            Snackbar(text="Chave salva neste aparelho." if ok
                     else "Não foi possível salvar a chave.").open()
            if ok:
                self.adicionar_balao("Tutor IA", "Chave configurada. Pode mandar sua dúvida!", "left")

        def remover(*_):
            ok = remover_chave_professor()
            self.dialogo_chave.dismiss()
            Snackbar(text="Chave removida deste aparelho." if ok
                     else "Não havia chave salva neste aparelho.").open()

        self.dialogo_chave = MDDialog(
            title="Tutor IA: chave de acesso",
            type="custom",
            content_cls=conteudo,
            buttons=[
                MDFlatButton(text="REMOVER", on_release=remover),
                MDFlatButton(text="CANCELAR", on_release=lambda *_: self.dialogo_chave.dismiss()),
                MDFlatButton(text="SALVAR", on_release=salvar),
            ],
        )
        self.dialogo_chave.open()
