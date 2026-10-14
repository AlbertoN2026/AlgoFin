from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class ComparacaoCenScreen(MDScreen):
    capital_val = NumericProperty(1000)
    taxa_val = NumericProperty(5)
    tempo_val = NumericProperty(12)
    
    montante_simples = NumericProperty(0)
    montante_composto = NumericProperty(0)
    diferenca_cenarios = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Descolamento",
            "texto": "O Clube de Matemática de Codó quer investir [b]R$ 1.000,00[/b] a uma taxa de [b]5%[/b].\n\nAjuste o Capital para 1000 e a Taxa para 5. Agora, deslize o Tempo para [b]12 meses[/b]. Qual dos dois cenários gerou mais dinheiro no final de um ano?",
            "validador": lambda c, tx, t: c == 1000 and tx == 5 and t == 12,
            "msg_acerto": "Observação correta! Em 1 ano, os Juros Simples geraram R$ 1.600,00, enquanto os Compostos já decolaram para mais de R$ 1.795,00. A mágica da exponencial começou a agir!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Grande Descoberta",
            "texto": "Mantenha o Capital em [b]1000[/b] e a Taxa em [b]5[/b]. Agora, reduza o Tempo para exatamente [b]1 MÊS[/b] e olhe o placar comparativo dos dois cenários.\n\nO que acontece quando o tempo é igual a 1?",
            "validador": lambda c, tx, t: c == 1000 and tx == 5 and t == 1,
            "msg_acerto": "Você descobriu o segredo! No exato primeiro mês, os Juros Simples e os Juros Compostos dão o MESMO RESULTADO (R$ 1.050,00). O juro composto só ganha vantagem a partir do segundo mês!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OLITEF / OBMEP",
            "texto": "(Olimpíada) Ana tem R$ 500,00 e duas opções de investimento que rendem exatos 10% ao mês. A Opção A é em Juros Simples e a Opção B é em Juros Compostos. Se Ana investir o dinheiro por EXATAMENTE 1 MÊS e sacar tudo, qual opção lhe dará mais lucro?",
            "opcoes": [
                "A Opção A, porque juros simples são melhores a curto prazo.",
                "A Opção B, porque juros compostos são sempre maiores.",
                "Nenhuma. As duas opções darão exatamente o mesmo lucro de R$ 50,00."
            ],
            "correta": 2,
            "msg_acerto": "Resposta digna de Medalha de Ouro! Essa é uma pegadinha clássica em provas de Olimpíadas. No primeiro mês (t=1), a base de cálculo é apenas o capital inicial para AMBOS os sistemas, gerando rendimentos idênticos.\n\n✨ Progresso Salvo! Fase 7 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.capital_val = 1000
        self.taxa_val = 5
        self.tempo_val = 12
        self.calcular_resultados()
        self.carregar_etapa()
        
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + \
                       Animation(elevation=1, duration=1.5, transition='in_out_sine')
        anim_flutuar.repeat = True
        anim_entrada.start(self.ids.balao_robo)
        anim_flutuar.start(self.ids.card_fala)

    def carregar_etapa(self):
        etapa = self.etapas[self.etapa_atual]
        self.titulo_missao = etapa["titulo"]
        self.texto_missao = etapa["texto"]
        
        self.ids.action_container.clear_widgets()
        
        if etapa["tipo"] == "slider":
            btn = MDRaisedButton(
                text="VERIFICAR COMPARAÇÃO",
                size_hint_x=1,
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(
                    size_hint_y=None,
                    height=dp(70),
                    padding="12dp",
                    radius=[8],
                    md_bg_color=[1, 1, 1, 1],
                    elevation=1,
                    ripple_behavior=True
                )
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                
                label = MDLabel(
                    text=f"[b]{letras[i]}[/b] {opt}",
                    markup=True,
                    font_style="Caption",
                    theme_text_color="Primary"
                )
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_capital(self, valor):
        self.capital_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_tempo(self, valor):
        self.tempo_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        c = self.capital_val
        i = self.taxa_val / 100
        t = self.tempo_val
        
        # Juros Simples
        self.montante_simples = c + (c * i * t)
        
        # Juros Compostos
        self.montante_composto = c * ((1 + i) ** t)
        
        # Diferença a favor do composto
        self.diferenca_cenarios = self.montante_composto - self.montante_simples

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.capital_val, self.taxa_val, self.tempo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A simulação não bate com os valores da missão. Revise os parâmetros no texto e ajuste a máquina.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Medalha Garantida!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Faça o teste prático! Mova o Tempo para 1 MÊS no painel e olhe o resultado dos dois cenários antes de responder.", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.avancar_etapa if acertou else self.fechar_dialog

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
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
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 7:
                app.nivel_modulo2 = 7
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'