import webbrowser
from kivymd.uix.screen import MDScreen

class MateriasScreen(MDScreen):
    def abrir_pdf_drive(self):
        # O link do seu drive fica agora encapsulado e organizado aqui
        link_fixo = "https://drive.google.com/file/d/1TtcZ4y3RR_UvM6nsp9U4rrlWUhwoLl0i/view?usp=sharing"
        webbrowser.open(link_fixo)