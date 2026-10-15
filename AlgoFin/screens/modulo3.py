from kivymd.uix.screen import MDScreen

class Modulo3Screen(MDScreen):
    def abrir_fase(self, nome_tela):
        # O método abrir_fase leva o aluno para a tela interativa selecionada
        self.manager.current = nome_tela

    def voltar(self):
        self.manager.current = 'inicial'