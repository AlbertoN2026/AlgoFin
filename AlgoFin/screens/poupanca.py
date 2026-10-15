import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.properties import ListProperty, StringProperty
from kivy.metrics import dp


class PoupancaScreen(MDScreen):
    blocos_selecionados = ListProperty([])
    missao_texto = StringProperty("")
    dialog = None

    def on_enter(self):
        if not self.missao_texto:
            self.gerar_novo_desafio()

    def gerar_novo_desafio(self):
        self.limpar_blocos()
        
        mesada = random.choice([50, 80, 100, 120, 150, 200])
        gasto = random.choice([20, 30, 40, 50, 70])
        
        # Caso de borda: com gasto >= mesada, o laço "juntar até a meta" não termina
        if gasto >= mesada:
            gasto = mesada - 20
            
        sobra = mesada - gasto
        # Meta múltipla da poupança mensal: o número de meses é exato
        objetivo = sobra * random.choice([3, 4, 5, 6]) 

        self.mesada, self.gasto, self.objetivo = mesada, gasto, objetivo
        self.missao_paga = False
        self.missao_texto = (f"Mesada: R$ {mesada}. Gasto: R$ {gasto}. "
                             f"Objetivo: comprar um item de R$ {objetivo}. "
                             f"Monte o algoritmo:")
        
        self.bloco_mesada = f"Var: Mesada = {mesada}"
        self.bloco_gasto = f"Var: Gasto = {gasto}"
        self.bloco_operacao = "Op: Poupanca = Mesada - Gasto"
        self.bloco_laco = f"Loop: Juntar R$ {objetivo}"
        
        # Criamos os "dados" dos blocos com suas respectivas cores
        blocos_disponiveis = [
            {"text": self.bloco_mesada, "color": [0.2, 0.6, 0.2, 1]},
            {"text": self.bloco_gasto, "color": [0.8, 0.2, 0.2, 1]},
            {"text": self.bloco_operacao, "color": [0.2, 0.4, 0.8, 1]},
            {"text": self.bloco_laco, "color": [0.8, 0.6, 0.1, 1]}
        ]
        
        # Embaralha a ordem dos blocos (evita a resolução mecânica)
        random.shuffle(blocos_disponiveis)
        
        self.desenhar_paleta(blocos_disponiveis)

    def desenhar_paleta(self, blocos):
        paleta = self.ids.paleta_blocos
        paleta.clear_widgets()
        
        # Cria os botões na tela baseados na lista embaralhada
        for bloco in blocos:
            btn = MDRaisedButton(
                text=bloco["text"],
                size_hint_x=1,
                size_hint_y=None,
                height=dp(48),
                font_size="14sp",
                md_bg_color=bloco["color"],
                # Usamos lambda para passar o texto correto para o evento de clique
                on_release=lambda x, t=bloco["text"]: self.adicionar_bloco(t)
            )
            paleta.add_widget(btn)

    def adicionar_bloco(self, tipo_bloco):
        self.blocos_selecionados.append(tipo_bloco)
        self.atualizar_area_trabalho()

    def desfazer_bloco(self):
        if self.blocos_selecionados:
            self.blocos_selecionados.pop()
            self.atualizar_area_trabalho()

    def limpar_blocos(self):
        self.blocos_selecionados.clear()
        self.atualizar_area_trabalho()

    def confirmar_limpar(self):
        if not self.blocos_selecionados:
            return
        self.fechar_dialog()
        self.dialog = MDDialog(
            title="Apagar o algoritmo?",
            text="Os blocos que você colocou no algoritmo serão retirados. "
                 "A missão continua a mesma.",
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.fechar_dialog),
                MDFlatButton(text="APAGAR", on_release=self._limpar_e_fechar),
            ],
        )
        self.dialog.open()

    def _limpar_e_fechar(self, *args):
        self.fechar_dialog()
        self.limpar_blocos()

    def atualizar_area_trabalho(self):
        app = MDApp.get_running_app()
        area = self.ids.area_trabalho
        area.clear_widgets()
        
        for bloco in self.blocos_selecionados:
            bloco_card = MDCard(
                size_hint_y=None,
                height=dp(40),
                md_bg_color=app.theme_cls.primary_color,
                radius=[dp(8)],
                elevation=1
            )
            lbl = MDLabel(
                text=bloco,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Subtitle2",
                bold=True
            )
            bloco_card.add_widget(lbl)
            area.add_widget(bloco_card)

    def diagnosticar(self):
        """Devolve None se a ordem respeita as dependências entre os dados
        (as duas variáveis antes da operação, e a operação antes do laço);
        caso contrário, devolve uma mensagem que indica o problema."""
        blocos = list(self.blocos_selecionados)
        necessarios = [self.bloco_mesada, self.bloco_gasto,
                       self.bloco_operacao, self.bloco_laco]
        if len(blocos) != len(set(blocos)):
            return ("Há blocos repetidos no algoritmo. Use o botão de desfazer "
                    "ou a lixeira e monte de novo, usando cada bloco uma vez.")
        if len(blocos) < len(necessarios):
            return ("Faltam blocos: o algoritmo precisa das duas variáveis, "
                    "da operação e do laço.")
        pos = {b: blocos.index(b) for b in necessarios}
        if pos[self.bloco_laco] < pos[self.bloco_operacao]:
            return ("O laço \"Juntar\" usa a Poupança, mas ela ainda não foi "
                    "calculada nesse ponto. A operação precisa vir antes do laço.")
        if pos[self.bloco_operacao] < max(pos[self.bloco_mesada], pos[self.bloco_gasto]):
            return ("A operação Poupanca = Mesada - Gasto usa a Mesada e o Gasto, "
                    "mas uma dessas variáveis ainda não existe nesse ponto. "
                    "Defina as duas variáveis antes da operação.")
        return None

    def executar_algoritmo(self):
        problema = self.diagnosticar()
        if problema is None:
            sobra = self.mesada - self.gasto
            meses = self.objetivo // sobra
            passos = "\n".join(f"Mês {m}: R$ {m * sobra}" for m in range(1, meses + 1))
            app = MDApp.get_running_app()
            if not self.missao_paga:
                self.missao_paga = True
                app.moedas += 10
                app.save_data()
                recompensa = f"Recompensa: +10 moedas (total: {app.moedas})."
            else:
                recompensa = "A recompensa desta missão já foi recebida."
            titulo = "Algoritmo correto!"
            texto = (f"Execução (Poupança = R$ {sobra} por mês):\n{passos}\n\n"
                     f"Em {meses} meses você junta R$ {self.objetivo} e compra o item.\n\n"
                     f"{recompensa}")
            btn = MDFlatButton(text="PRÓXIMO DESAFIO", on_release=self.proximo_desafio)
        else:
            titulo = "Ainda não está certo"
            texto = problema
            btn = MDFlatButton(text="TENTAR DE NOVO", on_release=self.fechar_dialog)

        self.fechar_dialog()
        self.dialog = MDDialog(title=titulo, text=texto, buttons=[btn])
        self.dialog.open()

    def fechar_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def proximo_desafio(self, *args):
        self.fechar_dialog()
        self.gerar_novo_desafio()
