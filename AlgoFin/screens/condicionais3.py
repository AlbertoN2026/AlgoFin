from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.metrics import dp

class Condicionais3Screen(MDScreen):
    salario_val = NumericProperty(1000)
    
    condicao_texto = StringProperty("")
    aliquota_val = NumericProperty(0)
    imposto_calc = NumericProperty(0)
    
    etapa_atual = NumericProperty(0)
    titulo_missao = StringProperty("")
    texto_missao = StringProperty("")
    dialog = None

    etapas = [
        {
            "tipo": "slider",
            "titulo": "MISSÃO 1: O Bloco de Isenção",
            "texto": "O algoritmo da Receita tem um 'IF' inicial que perdoa quem ganha pouco. Ajuste seu Salário Bruto para R$ 2.000,00 e veja o painel.\n\nQual bloco de código foi executado e qual foi o imposto gerado?",
            "validador": lambda s: s == 2000,
            "msg_acerto": "Isso! O computador executou o 'IF (Salario <= 2259)'. Você caiu na faixa de Isenção, a alíquota é 0% e o imposto é zero."
        },
        {
            "tipo": "slider",
            "titulo": "MISSÃO 2: A Armadilha do Else",
            "texto": "Agora, vamos simular alguém que ganha bem. Ajuste o seu Salário Bruto para o máximo (R$ 10.000,00).\n\nObserve o painel. Como nenhuma das condições anteriores (IF e ELIFs) era verdadeira, em qual bloco o código caiu?",
            "validador": lambda s: s == 10000,
            "msg_acerto": "Algoritmo compreendido! Como seu salário não era menor que nenhum dos limites testados, o computador pulou todos os ELIFs e caiu no 'ELSE' (Senão), que é a última condição (27,5% de imposto)!"
        },
        {
            "tipo": "questao",
            "titulo": "QUESTÃO DE COMPUTAÇÃO",
            "texto": "Por que a estrutura ELSE (Senão) não precisa de uma verificação matemática (ex: ELSE Salario > 4664)?",
            "opcoes": [
                "Porque o computador não sabe fazer contas maiores que 4664.",
                "Porque o ELSE é uma condição de descarte. Ele captura automaticamente tudo o que foi falso nos IFs e ELIFs anteriores.",
                "Porque o imposto de renda não cobra de quem ganha mais que o limite."
            ],
            "correta": 1,
            "msg_acerto": "Medalha de Programador! O ELSE é o famoso 'caso contrário'. Se nenhuma das regras de cima funcionou, o código executa o bloco ELSE por eliminação. É assim que os maiores salários são taxados.\n\n✨ Fase 8 Desbloqueada ✨"
        }
    ]

    def on_enter(self):
        self.etapa_atual = 0
        self.salario_val = 1000
        self.calcular_resultados()
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
                text="COMPILAR CÓDIGO", size_hint_x=1, md_bg_color=MDApp.get_running_app().theme_cls.primary_color, on_release=self.validar_missao
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

    def atualizar_salario(self, valor):
        self.salario_val = valor
        self.calcular_resultados()

    def calcular_resultados(self):
        # Transcrição da Tabela do IRPF (Base aproximada 2024 para ensino)
        salario = self.salario_val
        deducao = 0
        
        # A MÁQUINA DE ESTADOS (Condicionais)
        if salario <= 2259.20:
            self.condicao_texto = "IF (Salario <= 2259.20)"
            self.aliquota_val = 0.0
            deducao = 0.0
            
        elif salario <= 2826.65:
            self.condicao_texto = "ELIF (Salario <= 2826.65)"
            self.aliquota_val = 7.5
            deducao = 169.44
            
        elif salario <= 3751.05:
            self.condicao_texto = "ELIF (Salario <= 3751.05)"
            self.aliquota_val = 15.0
            deducao = 381.44
            
        elif salario <= 4664.68:
            self.condicao_texto = "ELIF (Salario <= 4664.68)"
            self.aliquota_val = 22.5
            deducao = 662.77
            
        else:
            self.condicao_texto = "ELSE (Todas as acima foram falsas)"
            self.aliquota_val = 27.5
            deducao = 896.00

        # Cálculo final
        imposto_bruto = salario * (self.aliquota_val / 100)
        imposto_liquido = imposto_bruto - deducao
        
        # Impede imposto negativo por margem de erro da dedução
        if imposto_liquido < 0:
            imposto_liquido = 0
            
        self.imposto_calc = imposto_liquido

    def validar_missao(self, *args):
        etapa = self.etapas[self.etapa_atual]
        if etapa["validador"](self.salario_val):
            self.mostrar_popup("Código Compilado!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro no Input", "Seu salário bruto não corresponde ao que foi pedido na missão. Ajuste o slider e tente compilar novamente.", False)

    def validar_questao(self, index_escolhido):
        etapa = self.etapas[self.etapa_atual]
        if index_escolhido == etapa["correta"]:
            self.mostrar_popup("Lógica Impecável!", etapa["msg_acerto"], True)
        else:
            self.mostrar_popup("Erro de Sintaxe", "Lembre-se que o ELSE é acionado unicamente quando todas as opções anteriores são descartadas.", False)

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
            # Salvando o progresso para a Fase 8!
            app = MDApp.get_running_app()
            if hasattr(app, 'nivel_modulo3') and app.nivel_modulo3 < 8:
                app.nivel_modulo3 = 8
                app.save_data() 
            self.voltar()

    def voltar(self):
        self.manager.current = 'modulo3'