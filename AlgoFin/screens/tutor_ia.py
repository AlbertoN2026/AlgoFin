import threading
import requests
import json
import re
from kivy.clock import Clock
from config_segura import obter_chave_api
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner

# URL da API do Gemini (sem chave: a chave é lida fora do código, por config_segura.py)
URL_IA = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

class TutorScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.card_digitando = None
        self.historico = [] 
        
        Clock.schedule_once(lambda dt: self.adicionar_balao(
            "Tutor IA", 
            "Olá! Sou o seu Tutor Cognitivo. Que desafio matemático ou computacional vamos investigar hoje?", 
            "left"
        ), 1)

    def enviar(self):
        msg = self.ids.input_msg.text
        if not msg.strip(): return
        
        self.ids.input_msg.text = ""
        self.adicionar_balao("Você", msg, "right")
        self.mostrar_digitando()
        
        # Inicia a thread para não travar a tela enquanto a IA pensa
        threading.Thread(target=self.chamar_api, args=(msg,)).start()

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
        
        # Adiciona a pergunta atual na memória com o formato exigido pelo Gemini
        nova_mensagem = {"role": "user", "parts": [{"text": msg}]}
        self.historico.append(nova_mensagem)
        
        # Estrutura completa da requisição
        payload = {
            "system_instruction": {
                "parts": [{"text": contexto_pedagogico}]
            },
            "contents": self.historico
        }
        
        chave = obter_chave_api()
        if not chave:
            self.historico.pop()
            Clock.schedule_once(lambda dt: self.finalizar(
                "O tutor está desativado neste aparelho porque a chave de acesso não foi configurada. "
                "Peça ajuda ao professor."))
            return

        try:
            headers = {'Content-Type': 'application/json', 'x-goog-api-key': chave}
            r = requests.post(URL_IA, headers=headers, data=json.dumps(payload), timeout=20)
            
            # RASTREADOR DE ERROS DO GOOGLE
            if r.status_code != 200:
                self.historico.pop() # Remove a pergunta da memória para não bugar o fluxo
                try:
                    erro_exato = r.json()['error']['message']
                except:
                    erro_exato = r.text
                
                erro_msg = f"Erro na API Google: {erro_exato}" if r.status_code != 429 else "Muitos acessos simultâneos! Aguarde alguns segundos."
                Clock.schedule_once(lambda dt: self.finalizar(erro_msg))
                return

            txt = r.json()['candidates'][0]['content']['parts'][0]['text']
            
            # Salva a resposta da IA na memória (o Gemini usa o role 'model')
            self.historico.append({"role": "model", "parts": [{"text": txt}]})
            
            # Limpeza e formatação de texto para o KivyMD (Negrito e Itálico)
            txt = txt.replace('\n', '\n').replace('\\n', '\n')
            txt = re.sub(r'\*\*(.*?)\*\*', r'[b]\1[/b]', txt) 
            txt = re.sub(r'\*(.*?)\*', r'[i]\1[/i]', txt)     
            
            Clock.schedule_once(lambda dt: self.finalizar(txt))
            
        except Exception as e:
            if self.historico:
                self.historico.pop()
            Clock.schedule_once(lambda dt: self.finalizar(f"Erro de conexão local. Verifique sua internet! ({str(e)})"))

    def finalizar(self, texto):
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