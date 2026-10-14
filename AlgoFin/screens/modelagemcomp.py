from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class ModelagemCompScreen(MDScreen):
    preco_veiculo_val = NumericProperty(50000)
    perc_entrada_val = NumericProperty(0)
    taxa_val = NumericProperty(2)
    tempo_val = NumericProperty(48)
    
    valor_entrada_calc = NumericProperty(0)
    valor_financiado_calc = NumericProperty(0)
    total_juros_calc = NumericProperty(0)
    custo_final_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: A Ilusão do 'Sem Entrada'",
            "texto": "Um dos professores do Clube de Matemática de Codó quer comprar um carro de [b]R$ 50.000,00[/b]. O banco ofereceu financiar 100% do carro ([b]0% de entrada[/b]) em [b]60 meses[/b] a uma taxa de [b]2% ao mês[/b].\n\nSimule esse cenário. Qual será o Custo Final deste carro?",
            "validador": lambda p, e, tx, t: p == 50000 and e == 0 and tx == 2 and t == 60,
            "msg_acerto": "Assustador, não é? O carro de 50 mil custará mais de 86 mil reais no final das contas. Você pagou um carro e quase outro só de juros para o banco!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: O Poder de Poupar Antes",
            "texto": "Agora, simule o cenário com Educação Financeira. Mantenha o preço em [b]R$ 50.000,00[/b], a taxa em [b]2%[/b] e o tempo em [b]60 meses[/b].\n\nMas desta vez, ajuste a [b]Entrada para 50%[/b]. Veja o que acontece com a linha vermelha dos Juros Cobrados no painel.",
            "validador": lambda p, e, tx, t: p == 50000 and e == 50 and tx == 2 and t == 60,
            "msg_acerto": "Análise perfeita! Ao dar 50% de entrada, os juros caíram pela metade (de R$ 36 mil para cerca de R$ 18 mil). Juros compostos só agem sobre o que você deve."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OLITEF / OBMF",
            "texto": "Com base nas simulações realizadas no laboratório, qual é a regra matemática fundamental para comprar bens de alto valor evitando o endividamento?",
            "opcoes": [
                "Alongar o prazo para o máximo de meses possível, pois a parcela fica menor.",
                "Juntar o máximo de dinheiro possível para dar uma Entrada maior, reduzindo o capital que sofrerá juros.",
                "Comprar carros mais caros, pois a taxa de juros do banco cai."
            ],
            "correta": 1,
            "msg_acerto": "Medalha garantida! Alongar prazo é uma armadilha matemática (a parcela diminui, mas o juro total explode). A única defesa contra os juros compostos é diminuir o Valor Financiado com uma entrada forte!\n\n✨ Fase 9 (A Batalha Final) Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.preco_veiculo_val = 50000
        self.perc_entrada_val = 0
        self.taxa_val = 2
        self.tempo_val = 60
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
                text="EXECUTAR MODELAGEM",
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
                    height=dp(85),
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

    def atualizar_preco(self, valor):
        self.preco_veiculo_val = valor
        self.calcular_resultados()

    def atualizar_entrada(self, valor):
        self.perc_entrada_val = valor
        self.calcular_resultados()

    def atualizar_taxa(self, valor):
        self.taxa_val = valor
        self.calcular_resultados()

    def atualizar_tempo(self, valor):
        self.tempo_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # 1. Valor da Entrada
        self.valor_entrada_calc = self.preco_veiculo_val * (self.perc_entrada_val / 100)
        
        # 2. Valor Financiado (O que o banco realmente emprestou)
        self.valor_financiado_calc = self.preco_veiculo_val - self.valor_entrada_calc
        
        # 3. Modelagem da Tabela Price (Cálculo da Prestação)
        i = self.taxa_val / 100
        n = self.tempo_val
        
        if self.valor_financiado_calc > 0:
            prestacao = self.valor_financiado_calc * (i * ((1 + i)**n)) / (((1 + i)**n) - 1)
        else:
            prestacao = 0
            
        # 4. Resultados Finais
        total_pago_banco = prestacao * n
        self.total_juros_calc = total_pago_banco - self.valor_financiado_calc
        self.custo_final_calc = self.valor_entrada_calc + total_pago_banco

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.preco_veiculo_val, self.perc_entrada_val, self.taxa_val, self.tempo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "A simulação não bate com os valores da missão. Revise os parâmetros no texto.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Medalha Garantida!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Lógico", "Pense como um investidor. Se você empresta menos dinheiro do banco, sobre qual valor os juros vão incidir?", False)

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
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 9:
                app.nivel_modulo2 = 9
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'