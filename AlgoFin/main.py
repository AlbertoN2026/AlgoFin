import os
import json
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp

# Importamos as lógicas das nossas pastas (screens)
from screens.inicial import InicialScreen
from screens.perfil import PerfilScreen
from screens.tutor_ia import TutorScreen
from screens.materias import MateriasScreen
from screens.desafios import DesafiosScreen
from screens.poupanca import PoupancaScreen
from screens.juros import JurosScreen
from screens.sobre import SobreScreen
from screens.modulo1 import Modulo1Screen
from screens.modulo2 import Modulo2Screen  
from screens.modulo3 import Modulo3Screen
from screens.planejamento import PlanejamentoScreen
from screens.orcamento import OrcamentoScreen
from screens.consumo import ConsumoScreen
from screens.porcentagem import PorcentagemScreen
from screens.algoritmos import AlgoritmosScreen
from screens.padroes import PadroesScreen
from screens.decomposicao import DecomposicaoScreen
from screens.abstracao import AbstracaoScreen
from screens.bebras import BebrasScreen
from screens.jurossimples import JurosSimplesScreen
from screens.descontos import DescontosScreen
from screens.inflacao import InflacaoScreen
from screens.planejamentofin import PlanejamentoFinScreen
from screens.simulacaoinv import SimulacaoInvScreen
from screens.comparacaocen import ComparacaoCenScreen
from screens.algoritmosmod2 import AlgoritmosMod2Screen
from screens.modelagemcomp import ModelagemCompScreen
from screens.problemasolief import ProblemasOlitefScreen
from screens.juroscompostos3 import JurosCompostos3Screen
from screens.amortizacao import AmortizacaoScreen
from screens.equivalencia import EquivalenciaScreen
from screens.custooportunidade import CustoOportunidadeScreen
from screens.analiseinvest import AnaliseInvestScreen
from screens.algoritmosinterativos import AlgoritmosIterativosScreen
from screens.condicionais3 import Condicionais3Screen
from screens.simulacoes3 import Simulacoes3Screen
from screens.problemas3 import Problemas3Screen
from screens.otimizacao3 import Otimizacao3Screen


# Configuração de Janela para Computador
if platform != 'android':
    Window.size = (360, 640)

# Este é o único design que fica aqui: a base da aplicação (Menu Lateral e Gestor de Ecrãs)
ROOT_KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        InicialScreen:
            name: 'inicial'
        PlanejamentoScreen:          
            name: 'planejamento'
        Otimizacao3Screen:                         # <-- Registro
            name: 'otimizacao3'
        OrcamentoScreen:        
            name: 'orcamento'
        Condicionais3Screen:                                 # <-- Registro
            name: 'condicionais3'
        AbstracaoScreen:
            name: 'abstracao'
        Problemas3Screen:                        # <-- Registro
            name: 'problemas3'
        JurosSimplesScreen:
            name: 'jurossimples'
        Simulacoes3Screen:                             # <-- Registro
            name: 'simulacoes3'
        AlgoritmosIterativosScreen:                                  # <-- Registro
            name: 'algoritmositerativos'
        CustoOportunidadeScreen:                               # <-- Registro
            name: 'custooportunidade'
        AnaliseInvestScreen:                           # <-- Registro
            name: 'analiseinvest'
        PlanejamentoFinScreen:                             # <-- Registro
            name: 'planejamentofin'
        ProblemasOlitefScreen:                             # <-- Registro
            name: 'problemasolitef'
        JurosCompostos3Screen:                             # <-- Registro
            name: 'juroscompostos3'
        AlgoritmosMod2Screen:                          # <-- Registro
            name: 'algoritmosmod2'
        ComparacaoCenScreen:                           # <-- Registro
            name: 'comparacaocen'
        ModelagemCompScreen:                           # <-- Registro
            name: 'modelagemcomp'
        SimulacaoInvScreen:                          # <-- Registro
            name: 'simulacaoinv'
        EquivalenciaScreen:                          # <-- Registro
            name: 'equivalencia'
        AmortizacaoScreen:                         # <-- Registro
            name: 'amortizacao'
        InflacaoScreen:                      # <-- Registro da Tela
            name: 'inflacao'
        DescontosScreen:                       # <-- Registro da Tela
            name: 'descontos'
        BebrasScreen:                    # <-- Nova tela registrada
            name: 'bebras'
        DecomposicaoScreen:
            name: 'decomposicao'
        PadroesScreen:
            name: 'padroes'
        AlgoritmosScreen:             # <-- ADICIONE AQUI
            name: 'algoritmos'
        ConsumoScreen:             
            name: 'consumo'
        PorcentagemScreen:             
            name: 'porcentagem'      
        PoupancaScreen:
            name: 'poupanca'
        JurosScreen:
            name: 'juros'
        Modulo1Screen:
            name: 'modulo1'
        Modulo2Screen:
            name: 'modulo2'
        Modulo3Screen:
            name: 'modulo3'
        TutorScreen:
            name: 'tutor_ia'
        PerfilScreen:
            name: 'perfil'
        DesafiosScreen:
            name: 'desafios'
        MateriasScreen:
            name: 'materias'
        SobreScreen:
            name: 'sobre'

    MDNavigationDrawer:
        id: nav_drawer
        MDNavigationDrawerMenu:
            MDNavigationDrawerHeader:
                title: "AlgoFin"
                title_color: app.theme_cls.primary_color
                text: "Educação Financeira e Computação" # Reflete a integração exigida
                source: "logo.png" # Aqui o Kivy puxa a sua imagem!
                spacing: "8dp"
                padding: "12dp", 0, 0, "36dp"
            MDNavigationDrawerItem:
                icon: "home"
                text: "Início"
                on_release: screen_manager.current = 'inicial'; nav_drawer.set_state("close")
            MDNavigationDrawerItem:
                icon: "account-circle"
                text: "Perfil"
                on_release: screen_manager.current = 'perfil'; nav_drawer.set_state("close")
            
            MDNavigationDrawerItem:
                icon: "information"
                text: "Sobre"
                on_release: screen_manager.current = 'sobre'; nav_drawer.set_state("close")
'''


from kivy.core.window import Window
if platform == 'android':
    Window.create_window()

class AlgoFinApp(MDApp):

    user_name = StringProperty("Utilizador")
    escola = StringProperty("Escola")
    turma = StringProperty("Turma")
    nivel_modulo1 = NumericProperty(1)
    nivel_modulo2 = NumericProperty(1)
    nivel_modulo3 = NumericProperty(1)
    moedas = NumericProperty(0)

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.load_data()
        
        # Proteção de leitura da pasta KV
        if os.path.exists('kv'):
            for kv_file in os.listdir('kv'):
                if kv_file.endswith('.kv'):
                    Builder.load_file(os.path.join('kv', kv_file))
        
        return Builder.load_string(ROOT_KV)

    def pegar_caminho_json(self):
        return os.path.join(self.user_data_dir, "user_data.json")

    def load_data(self):
        caminho = self.pegar_caminho_json()
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding='utf-8') as f:
                    dados = json.load(f)
                    self.user_name = dados.get("nome", "Utilizador")
                    self.moedas = dados.get("moedas", 0) 
                    self.escola = dados.get("escola", "Escola")
                    self.turma = dados.get("turma", "Turma")
                    self.nivel_modulo1 = dados.get("nivel_modulo1", 1) 
                    self.nivel_modulo2 = dados.get("nivel_modulo2", 1)
                    self.nivel_modulo3 = dados.get("nivel_modulo3", 1)
            except Exception:
                pass

    def save_data(self):
        dados = {
            "nome": self.user_name,
            "escola": self.escola,
            "moedas": self.moedas,
            "turma": self.turma,
            "nivel_modulo1": self.nivel_modulo1,
            "nivel_modulo2": self.nivel_modulo2,
            "nivel_modulo3": self.nivel_modulo3
        }
        caminho = self.pegar_caminho_json()
        try:
            with open(caminho, "w", encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

if __name__ == '__main__':
    AlgoFinApp().run()