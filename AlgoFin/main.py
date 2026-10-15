import os
import json
import tempfile
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

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

# Este é o único design que fica aqui: a base do aplicativo (menu lateral e gerenciador de telas)
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

# Perfil e progresso: valores padrão (Código 2 da dissertação)
PADRAO = {"nome": "Estudante", "escola": "", "turma": "",
          "moedas": 0, "nivel_modulo1": 1, "nivel_modulo2": 1,
          "nivel_modulo3": 1}
CAMPOS = ("escola", "turma", "moedas",
          "nivel_modulo1", "nivel_modulo2", "nivel_modulo3")


class AlgoFinApp(MDApp):

    user_name = StringProperty(PADRAO["nome"])
    escola = StringProperty(PADRAO["escola"])
    turma = StringProperty(PADRAO["turma"])
    nivel_modulo1 = NumericProperty(1)
    nivel_modulo2 = NumericProperty(1)
    nivel_modulo3 = NumericProperty(1)
    moedas = NumericProperty(0)
    aviso_dados = StringProperty("")

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.load_data()
        
        # Proteção de leitura da pasta KV
        if os.path.exists('kv'):
            for kv_file in os.listdir('kv'):
                if kv_file.endswith('.kv'):
                    Builder.load_file(os.path.join('kv', kv_file))
        
        return Builder.load_string(ROOT_KV)

    def on_start(self):
        # Aviso de leitura (arquivo corrompido) só depois que a tela existe
        if self.aviso_dados:
            Clock.schedule_once(lambda dt: self.avisar(self.aviso_dados), 1)

    def pegar_caminho_json(self):
        # Diretório de dados do app: gravável no Android e no Windows
        return os.path.join(self.user_data_dir, "user_data.json")

    def load_data(self):
        dados = dict(PADRAO)              # valores padrão sempre definidos
        self.aviso_dados = ""
        caminho = self.pegar_caminho_json()
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    lidos = json.load(f)
                if not isinstance(lidos, dict):
                    raise ValueError("formato inválido")
                for chave, padrao in PADRAO.items():
                    valor = lidos.get(chave, padrao)
                    # aceita só o tipo esperado (texto ou número inteiro)
                    if isinstance(padrao, str) and isinstance(valor, str):
                        dados[chave] = valor
                    elif (isinstance(padrao, int) and isinstance(valor, (int, float))
                          and not isinstance(valor, bool)):
                        dados[chave] = int(valor)
            except (OSError, ValueError):   # inclui JSON inválido
                self.aviso_dados = ("Não foi possível ler seu progresso; "
                                    "começamos de novo.")
        self.user_name = dados["nome"]
        for chave in CAMPOS:
            setattr(self, chave, dados[chave])

    def save_data(self):
        dados = {"nome": self.user_name}
        dados.update({chave: getattr(self, chave) for chave in CAMPOS})
        caminho = self.pegar_caminho_json()
        temporario = None
        try:
            pasta = os.path.dirname(caminho)
            os.makedirs(pasta, exist_ok=True)
            fd, temporario = tempfile.mkstemp(dir=pasta, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            os.replace(temporario, caminho)   # gravação atômica
            return True
        except OSError:
            if temporario and os.path.exists(temporario):
                try:
                    os.remove(temporario)
                except OSError:
                    pass
            self.aviso_dados = ("Seu progresso não pôde ser salvo "
                                "neste aparelho.")
            self.avisar(self.aviso_dados)
            return False

    def avisar(self, texto):
        """Mensagem curta na parte de baixo da tela."""
        try:
            Snackbar(text=texto).open()
        except Exception:
            print(texto)

    def confirmar_recomecar(self, modulo):
        """Pede confirmação antes de apagar o progresso de um módulo."""
        def recomecar(*_):
            dialogo.dismiss()
            setattr(self, f"nivel_modulo{modulo}", 1)
            self.save_data()

        dialogo = MDDialog(
            title=f"Recomeçar o Módulo {'I' * modulo if modulo < 4 else modulo}?",
            text="As fases deste módulo voltarão a ficar bloqueadas. "
                 "As moedas e os outros módulos não mudam.",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda *_: dialogo.dismiss()),
                MDFlatButton(text="RECOMEÇAR", on_release=recomecar),
            ],
        )
        dialogo.open()

if __name__ == '__main__':
    AlgoFinApp().run()