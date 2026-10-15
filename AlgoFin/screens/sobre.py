import webbrowser
from kivymd.uix.screen import MDScreen

class SobreScreen(MDScreen):
    def abrir_guia(self):
        # 1. Faça o upload do Guia_do_Estudante_AlgoFin.pdf para o seu Google Drive
        # 2. Clique com o botão direito, vá em "Compartilhar" e escolha "Qualquer pessoa com o link"
        # 3. Cole o link gerado aqui dentro das aspas:
        
        link_guia_drive = "https://drive.google.com/file/d/1pkXMs4Zajl4ipNrTSj_JmFH2VcwYxgqC/view?usp=sharing"
        
        # Abre o PDF diretamente do Google Drive no navegador do aluno
        webbrowser.open(link_guia_drive)