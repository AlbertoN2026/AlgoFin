from kivymd.uix.screen import MDScreen

class Modulo2Screen(MDScreen):
    
    def abrir_jurossimples(self):
        self.manager.current = 'jurossimples'

    def abrir_descontos(self):
        self.manager.current = 'descontos'

    def abrir_inflacao(self):
        self.manager.current = 'inflacao'

    def abrir_planejamento(self):
        self.manager.current = 'planejamentofin'

    def abrir_simulacao(self):
        self.manager.current = 'simulacaoinv'

    def abrir_comparacao(self):
        self.manager.current = 'comparacaocen'

    def abrir_algoritmos_mod2(self):
        self.manager.current = 'algoritmosmod2'

    def abrir_modelagem(self):
        self.manager.current = 'modelagemcomp'

    def abrir_olitef(self):
        self.manager.current = 'problemasolitef'

    def voltar(self):
        self.manager.current = 'inicial'