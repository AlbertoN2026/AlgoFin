from kivymd.uix.screen import MDScreen
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivy.clock import Clock

class PerfilScreen(MDScreen):
    edit_mode = BooleanProperty(False)

    def campos(self):
        return (self.ids.field_nome, self.ids.field_escola, self.ids.field_turma)

    def focar_campo(self, dt):
        # Esta função é chamada 0.1s depois para o Android ter tempo de destravar o campo
        self.ids.field_nome.focus = True

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        app = MDApp.get_running_app()
        
        if not self.edit_mode:
            # Salvar dados ao fechar o modo de edição
            app.user_name = self.ids.field_nome.text
            app.escola = self.ids.field_escola.text
            app.turma = self.ids.field_turma.text
            app.save_data()
        else:
            # No Android, o Kivy deixa um campo "não focável" quando ele nasce
            # somente leitura e não desfaz isso ao liberar a edição; sem esta
            # linha, o teclado não aparece. Os campos voltam a ser editáveis aqui.
            for campo in self.campos():
                campo.readonly = False
                campo.is_focusable = True
            # Chama o teclado com um micro-atraso para não bugar no Android
            Clock.schedule_once(self.focar_campo, 0.1)
        
        self.ids.toolbar.right_action_items = [
            ["check" if self.edit_mode else "pencil", lambda x: self.toggle_edit()]
        ]

    def voltar(self):
        self.edit_mode = False
        self.manager.current = 'inicial'