from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp

class JurosCompostos3Screen(MDScreen):
    aporte_val = NumericProperty(500)
    taxa_val = NumericProperty(1.0)
    anos_val = NumericProperty(10)
    
    total_investido = NumericProperty(0)
    montante_final = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Primeiro Milhão",
            "texto": "Use o simulador! Se você guardar R$ 500 por mês, a uma taxa realista de 1.0% ao mês, quantos ANOS vai demorar para você se tornar milionário? (Ajuste o Prazo até o Montante Final ultrapassar R$ 1.000.000,00).",
            # Validador ajustado para aceitar 26 anos e ser flexível com a casa decimal da taxa
            "validador": lambda a, t, anos: a == 500 and 0.9 < t < 1.1 and anos == 26,
            "msg_acerto": "Incrível! Foram precisos 26 anos. Mas repare: você tirou do seu bolso apenas R$ 156.000. Os outros oitocentos e poucos mil reais foram gerados pura e simplesmente pela força do Expoente (Tempo)!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: O Custo do Atraso",
            "texto": "Um jovem começa a investir aos 20 anos e para aos 40 (Prazo: 20 anos). Mantenha a taxa em 1.0% e ajuste o Aporte para R$ 1000. Veja quanto ele acumulou no final.\n\nAgora, digamos que você demorou 10 anos a mais (Prazo: 30 anos). Para quanto o valor salta?",
            "validador": lambda a, t, anos: a == 1000 and 0.9 < t < 1.1 and anos == 30,
            "msg_acerto": "Matemática assustadora! Em 20 anos, o valor era perto de R$ 989 mil. Mas com apenas 10 anos a mais (30 anos), o valor EXPLODE para quase R$ 3,5 milhões! Isso é a curva exponencial agindo."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO DE MODELAGEM",
            "texto": "Analisando a fórmula M = C * (1+i)^n, por que esperar para começar a investir 'quando estiver ganhando mais' é um erro matemático gravíssimo?",
            "opcoes": [
                "Porque os bancos não aceitam clientes mais velhos.",
                "Porque o Tempo (n) é a única variável no EXPOENTE. Começar cedo compensa aportes menores.",
                "Porque a taxa de juros cai conforme você envelhece."
            ],
            "correta": 1,
            "msg_acerto": "Gênio Algorítmico! O tempo multiplica o seu dinheiro sobre ele mesmo. Não importa se você ganha pouco hoje: colocar o expoente para trabalhar o mais cedo possível é o grande segredo das finanças!\n\n✨ Fase 2 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.aporte_val = 500
        self.taxa_val = 1.0
        self.anos_val = 10
        self.calcular_resultados()
        self.carregar_etapa()

    def carregar_etapa(self):
        etapa = self.etapas[self.etapa_atual]
        self.titulo_missao = etapa["titulo"]
        self.texto_missao = etapa["texto"]
        self.ids.action_container.clear_widgets()
        
        if etapa["tipo"] == "slider":
            btn = MDRaisedButton(
                text="VERIFICAR MODELAGEM",
                size_hint_x=1,
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(
                    size_hint_y=None, height=dp(70), padding="12dp", radius=[8],
                    md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True
                )
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_aporte(self, valor):
        self.aporte_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_anos(self, valor):
        self.anos_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        meses = self.anos_val * 12
        i = self.taxa_val / 100
        
        self.total_investido = self.aporte_val * meses
        
        # Fórmula do Valor Futuro (Série de Pagamentos Uniformes)
        if i > 0:
            self.montante_final = self.aporte_val * (((1 + i)**meses - 1) / i)
        else:
            self.montante_final = self.total_investido

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.aporte_val, self.taxa_val, self.anos_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A matemática não bateu. Continue ajustando o simulador de acordo com o texto da missão.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Lógica Impecável!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Lembre-se da matemática: o 'n' na fórmula M = C(1+i)^n atua de forma exponencial.", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.avancar_etapa if acertou else self.fechar_dialog

        self.dialog = MDDialog(
            title=titulo, text=texto,
            buttons=[MDFlatButton(text="OK", on_release=acao)]
        )
        self.dialog.open()

    def fechar_dialog(self, *args):
        self.dialog.dismiss()

    def avancar_etapa(self, *args):
        self.dialog.dismiss()
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.carregar_etapa()
        else:
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 2:
                app.nivel_modulo3 = 2
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'