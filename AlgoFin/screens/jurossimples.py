from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class JurosSimplesScreen(MDScreen):
    capital_val = NumericProperty(100)
    taxa_val = NumericProperty(1)
    tempo_val = NumericProperty(1)
    
    juros_calc = NumericProperty(0)
    montante_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    
    dialog = None

    # Banco de Missões e Questões Progressivas
    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: A Viagem do Clube",
            "texto": "O Clube de Matemática tem um capital de [b]R$ 500,00[/b] aplicado a uma taxa de [b]2%[/b] ao mês.\n\nAjuste a máquina acima para descobrir: Em [b]quantos meses (n)[/b] o rendimento atingirá exatamente [b]R$ 60,00[/b] de Juros para pagar as passagens?",
            "validador": lambda p, i, n: p == 500 and i == 2 and n == 6,
            "msg_acerto": "Excelente modelagem! A equação J = P x i x n operou perfeitamente: 500 x 0,02 x 6 resultou nos 60 reais de Juros."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: O Computador Parcelado",
            "texto": "Uma loja vende um notebook por [b]R$ 1.000,00[/b]. A loja cobra um absurdo de [b]5%[/b] de juros simples ao mês. Se parcelarmos em [b]10 meses[/b], ajuste a máquina para descobrir qual será o valor dos [b]JUROS (J)[/b] no final do período.",
            "validador": lambda p, i, n: p == 1000 and i == 5 and n == 10,
            "msg_acerto": "Análise crítica validada! A conta J = 1000 x 0,05 x 10 resulta em R$ 500,00 SÓ DE JUROS. Isso é metade do valor do notebook original!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 3: A Taxa Misteriosa",
            "texto": "A Aline pegou [b]R$ 400,00[/b] emprestados para vender doces. Após [b]5 meses[/b], ela pagou exatos [b]R$ 100,00 de Juros[/b].\n\nAjuste o Capital (P) e o Tempo (n). Agora, brinque com o slider da [b]Taxa (i)[/b] até o painel marcar R$ 100 de Juros e descubra qual foi a taxa cobrada.",
            "validador": lambda p, i, n: p == 400 and n == 5 and i == 5,
            "msg_acerto": "Lógica investigativa concluída! Para o juro resultar em R$ 100, mantendo o capital de 400 em 5 meses, a taxa obrigatoriamente teve de ser de 5%."
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO FINAL: A Reta dos Juros",
            "texto": "Você pode usar a máquina acima para testar antes de responder!\n\nMatematicamente, se você [b]dobrar o TEMPO (n)[/b] de um investimento em Juros Simples, mantendo o mesmo Capital e a mesma Taxa, o que acontece com os Juros gerados?",
            "opcoes": [
                "Eles também dobram (Crescimento Linear)",
                "Eles quadruplicam (Crescimento Exponencial)",
                "Eles ficam do mesmo tamanho"
            ],
            "correta": 0,
            "msg_acerto": "Lógica estrutural compreendida! Nos Juros Simples, as variáveis são lineares e proporcionais. Se o tempo dobra, o juro dobra.\n\n✨ Fase 2 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.capital_val = 100
        self.taxa_val = 1
        self.tempo_val = 1
        self.calcular_resultados()
        self.carregar_etapa()
        
        # Animação flutuante do Robô
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
                text="CONFIRMAR MODELAGEM",
                size_hint_x=1,
                md_bg_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            # Para a questão final, gera as 3 alternativas
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(
                    size_hint_y=None,
                    height=dp(50),
                    padding="12dp",
                    radius=[8],
                    md_bg_color=[1, 1, 1, 1],
                    elevation=1,
                    ripple_behavior=True
                )
                # Passa o índice atual para a validação
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
        self.juros_calc = self.capital_val * (self.taxa_val / 100) * self.tempo_val
        self.montante_calc = self.capital_val + self.juros_calc

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        # Valida chamando a função lambda do dicionário
        if etapa["validador"](self.capital_val, self.taxa_val, self.tempo_val):
            self.mostrar_popup("Modelagem Correta!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Os parâmetros não resolvem o problema atual. Leia o enunciado e ajuste os 3 controles deslizantes corretamente.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Resposta Exata!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Utilize a máquina acima! Coloque o Tempo em 2 meses e olhe o Juro. Depois coloque o Tempo em 4 meses e veja o que acontece. Tente novamente!", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        # Se acertou, a ação do botão avança de etapa. Se errou, apenas fecha o popup.
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
            # Se for a última etapa (a questão final), desbloqueia o Módulo 2, Fase 2
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo2') and app.nivel_modulo2 < 2:
                app.nivel_modulo2 = 2
                app.save_data()
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo2'