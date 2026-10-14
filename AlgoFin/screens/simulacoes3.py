from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp

class Simulacoes3Screen(MDScreen):
    patrimonio_val = NumericProperty(1000000)
    gasto_val = NumericProperty(5000)
    rendimento_val = NumericProperty(4.0)
    
    status_texto = StringProperty("AGUARDANDO SIMULAÇÃO")
    detalhe_texto = StringProperty("")
    cor_status = ListProperty([1, 1, 1, 1])
    idade_ruina = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: Testando a Regra dos 4%",
            "texto": "O Clube de Matemática de Codó decidiu simular um cenário: Um professor se aposenta aos 60 anos com R$ 1.200.000,00 de patrimônio. Ele deseja gastar R$ 4.000,00 por mês (o que dá R$ 48.000 no ano, exatamente 4% do total). O rendimento real é de 4.0%.\n\nRode a simulação e descubra: O dinheiro acaba ou ele atinge a Independência?",
            "validador": lambda p, g, r: p == 1200000 and g == 4000 and 3.9 < r < 4.1,
            "msg_acerto": "Simulação perfeita! O painel mostra 'INDEPENDÊNCIA GARANTIDA'. Como ele saca exatamente o que a carteira rende (4%), o dinheiro nunca acaba, sobrevivendo até depois dos 100 anos."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Ilusão do Novo Rico",
            "texto": "Alguém ganha na loteria R$ 1.500.000,00 aos 60 anos. Ele acha que está milionário e decide gastar R$ 15.000,00 por mês! O rendimento real é de 5.0% ao ano.\n\nAjuste a máquina e execute a simulação. Em qual idade o dinheiro dele vai zerar?",
            "validador": lambda p, g, r: p == 1500000 and g == 15000 and 4.9 < r < 5.1,
            "msg_acerto": "Lógica implacável! Apesar de ter um milhão e meio, o gasto de 15 mil reais (12% do patrimônio ao ano) destruiu a carteira. O dinheiro acabou completamente aos 70 anos. Ele voltou à estaca zero!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO OBMF",
            "texto": "Com base no motor de simulação, o que determina matematicamente se uma pessoa vai 'quebrar' financeiramente na aposentadoria?",
            "opcoes": [
                "Ter menos de 2 milhões de reais guardados no banco.",
                "A Taxa de Retirada (o percentual gasto no ano) ser maior que o Rendimento Real da carteira.",
                "Não investir na caderneta de poupança."
            ],
            "correta": 1,
            "msg_acerto": "Resposta exata! Não importa se você tem 100 mil ou 10 milhões. Se o seu percentual de gasto anual for maior que o percentual de rendimento líquido, o seu saldo vai começar a encolher até a ruína matemática.\n\n✨ Fase 9 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.patrimonio_val = 1000000
        self.gasto_val = 5000
        self.rendimento_val = 4.0
        self.calcular_simulacao()
        self.carregar_etapa()
        
        self.ids.balao_robo.opacity = 0
        anim_entrada = Animation(opacity=1, duration=0.6)
        anim_flutuar = Animation(elevation=4, duration=1.5, transition='in_out_sine') + Animation(elevation=1, duration=1.5, transition='in_out_sine')
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
                text="EXECUTAR SIMULAÇÃO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(80), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_patrimonio(self, valor):
        self.patrimonio_val = valor
        self.calcular_simulacao()

    def atualizar_gasto(self, valor):
        self.gasto_val = valor
        self.calcular_simulacao()

    def atualizar_rendimento(self, valor):
        self.rendimento_val = valor
        self.calcular_simulacao()

    def calcular_simulacao(self):
        saldo = self.patrimonio_val
        gasto_anual = self.gasto_val * 12
        taxa = self.rendimento_val / 100
        idade = 60
        quebrou = False
        
        # Loop de simulação dos 60 aos 100 anos
        while idade < 100:
            # Rendimento do ano
            rendimento_gerado = saldo * taxa
            # Saldo após rendimento e gasto
            saldo = saldo + rendimento_gerado - gasto_anual
            
            if saldo <= 0:
                quebrou = True
                self.idade_ruina = idade
                break
                
            idade += 1

        if quebrou:
            self.status_texto = "FALÊNCIA!"
            self.cor_status = [0.9, 0.3, 0.3, 1] # Vermelho
            self.detalhe_texto = f"O dinheiro acabou completamente aos {self.idade_ruina} anos."
        else:
            self.status_texto = "INDEPENDÊNCIA GARANTIDA!"
            self.cor_status = [0.4, 0.8, 0.4, 1] # Verde
            saldo_formatado = f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.detalhe_texto = f"Aos 100 anos, você ainda terá {saldo_formatado}."

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.patrimonio_val, self.gasto_val, self.rendimento_val):
            self.mostrar_popup("Simulação Concluída!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Divergência", "Os parâmetros não conferem. Revise o Patrimônio, o Gasto Mensal e o Rendimento exigidos na missão.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Lógica Impecável!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro Conceitual", "Lembre-se da relação direta entre a 'Taxa de Retirada' (o que você gasta do bolo total) e a Taxa de Rendimento.", False)

    def mostrar_popup(self, titulo, texto, acertou):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        acao = self.avancar_etapa if acertou else self.fechar_dialog
        self.dialog = MDDialog(title=titulo, text=texto, buttons=[MDFlatButton(text="OK", on_release=acao)])
        self.dialog.open()

    def fechar_dialog(self, *args):
        self.dialog.dismiss()

    def avancar_etapa(self, *args):
        self.dialog.dismiss()
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.carregar_etapa()
        else:
            # Salvando o progresso para a Fase 9!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 9:
                app.nivel_modulo3 = 9
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'