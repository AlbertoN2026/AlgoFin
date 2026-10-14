import webbrowser
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class Modulo1Screen(MDScreen):
    
    def forcar_atualizacao(self):
        # Força o Kivy a reavaliar os cadeados sempre que a tela abrir
        app = MDApp.get_running_app()
        temp = app.nivel_modulo1
        app.nivel_modulo1 = 0
        app.nivel_modulo1 = temp

    def abrir_pdf(self, tema):
        links_pdfs = {
            "consumo": "https://seu-link-aqui.com",
            "porcentagem": "https://seu-link-aqui.com",
            "algoritmos": "https://seu-link-aqui.com",
            "padroes": "https://seu-link-aqui.com",
            "decomposicao": "https://seu-link-aqui.com",
            "logica": "https://seu-link-aqui.com",
            "bebras": "https://seu-link-aqui.com"
        }
        
        link = links_pdfs.get(tema)
        if link:
            webbrowser.open(link)
        else:
            print(f"Link para {tema} não encontrado.")

    def abrir_planejamento(self):
        self.manager.current = 'planejamento'

    def abrir_orcamento(self):
        self.manager.current = 'orcamento'

    def abrir_consumo(self):
        self.manager.current = 'consumo'
    def abrir_porcentagem(self):
        self.manager.current = 'porcentagem'
    def abrir_algoritmos(self):
        self.manager.current = 'algoritmos'
    def abrir_padroes(self):
        self.manager.current = 'padroes'
    def abrir_decomposicao(self):
        self.manager.current = 'decomposicao'
    def abrir_abstracao(self):
        self.manager.current = 'abstracao'
    def abrir_bebras(self):
        self.manager.current = 'bebras'