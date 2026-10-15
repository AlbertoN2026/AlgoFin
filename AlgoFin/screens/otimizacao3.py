from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp

class Otimizacao3Screen(MDScreen):
    rv_perc = NumericProperty(0)
    rf_perc = NumericProperty(100)
    
    rv_val = NumericProperty(0)
    rf_val = NumericProperty(10000)
    
    retorno_calc = NumericProperty(1000)
    risco_texto = StringProperty("MUITO BAIXO")
    cor_risco = ListProperty([0.4, 0.8, 0.4, 1])
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: A Meta do Cliente",
            "texto": "Um cliente te entregou R$ 10.000. Ele exige que no final do ano a carteira renda EXATAMENTE R$ 1.600,00.\n\nDeslize o controle para achar a alocação matemática perfeita (ponto de otimização) que gera esse valor exato de retorno.",
            "validador": lambda rv: rv == 40,
            "msg_acerto": "Otimização Concluída! Para gerar R$ 1.600,00, a carteira precisava exatamente de 60% em Renda Fixa (gera R$ 600) e 40% em Renda Variável (gera R$ 1000). Risco mantido sob controle!"
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: O Limite da Ganância",
            "texto": "Um outro cliente quer o máximo de retorno possível. Deslize o controle para 100% em Renda Variável.\n\nO que acontece com o Risco Sistêmico e qual o retorno máximo alcançado?",
            "validador": lambda rv: rv == 100,
            "msg_acerto": "Alerta Vermelho! Você atingiu o retorno máximo de R$ 2.500, mas o Risco virou EXTREMO. Se a bolsa cair, o cliente perde quase todo o dinheiro. É por isso que otimizar é sobre DIVERSIFICAR (não colocar todos os ovos na mesma cesta)."
        },
        {
            "tipo": "questao",
            "titulo": "A QUESTÃO FINAL (OBMF)",
            "texto": "Matematicamente, o que significa diversificar uma carteira de investimentos?",
            "opcoes": [
                "Aumentar o Retorno para 100% anulando os juros compostos.",
                "Colocar todo o dinheiro no ativo de maior risco para recuperar as perdas mais rápido.",
                "Distribuir o capital entre diferentes ativos para diluir o Risco Sistêmico sem abrir mão de um bom retorno."
            ],
            "correta": 2,
            "msg_acerto": "Resposta de Mestre! Você dominou a base da engenharia financeira. Diversificação é o único 'almoço grátis' do mercado financeiro!\n\n🏆 PARABÉNS! VOCÊ ZEROU O MÓDULO III! 🏆"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.rv_perc = 0
        self.atualizar_alocacao(0)
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
                text="VERIFICAR OTIMIZAÇÃO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
            )
            self.ids.action_container.add_widget(btn)
        else:
            letras = ["A) ", "B) ", "C) "]
            for i, opt in enumerate(etapa["opcoes"]):
                card = MDCard(size_hint_y=None, height=dp(85), padding="12dp", radius=[8], md_bg_color=[1, 1, 1, 1], elevation=1, ripple_behavior=True)
                card.bind(on_release=lambda instance, idx=i: self.validar_questao(idx))
                label = MDLabel(text=f"[b]{letras[i]}[/b] {opt}", markup=True, font_style="Caption", theme_text_color="Primary")
                card.add_widget(label)
                self.ids.action_container.add_widget(card)

    def atualizar_alocacao(self, valor):
        self.rv_perc = valor
        self.rf_perc = 100 - valor
        
        self.rv_val = 10000 * (self.rv_perc / 100)
        self.rf_val = 10000 * (self.rf_perc / 100)
        
        # RF rende 10%, RV rende 25%
        retorno_rf = self.rf_val * 0.10
        retorno_rv = self.rv_val * 0.25
        self.retorno_calc = retorno_rf + retorno_rv
        
        # Medidor de Risco
        if self.rv_perc <= 20:
            self.risco_texto = "BAIXO"
            self.cor_risco = [0.4, 0.8, 0.4, 1] # Verde
        elif self.rv_perc <= 50:
            self.risco_texto = "MODERADO"
            self.cor_risco = [0.9, 0.7, 0.2, 1] # Amarelo
        elif self.rv_perc <= 80:
            self.risco_texto = "ALTO"
            self.cor_risco = [0.9, 0.5, 0.2, 1] # Laranja
        else:
            self.risco_texto = "EXTREMO (PERIGO)"
            self.cor_risco = [0.9, 0.1, 0.1, 1] # Vermelho

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.rv_perc):
            self.mostrar_popup("Missão Cumprida!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Fora da Meta", "A sua alocação não bate com a exigência do cliente. Deslize o medidor até atingir a meta.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Zerou o Jogo!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Quase lá...", "Lembre do termo: 'não colocar todos os ovos na mesma cesta'.", False)

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
            # MARCO HISTÓRICO: MÓDULO 3 CONCLUÍDO. ZEROU O APP!
            app = MDApp.get_running_app()
            # Se quiser, você pode criar uma variável 'jogo_zerado = True' no futuro.
            app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'