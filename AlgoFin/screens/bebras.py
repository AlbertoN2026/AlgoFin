import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp

class BebrasScreen(MDScreen):
    questao_atual_idx = NumericProperty(0)
    titulo_fase = StringProperty("")
    enunciado_texto = StringProperty("")
    
    dialog = None
    prova_sorteada = []

    # Banco de Dados de Desafios Integradores (Baseado na Lógica do Bebras 2023)
    banco_questoes = [
        {
            "titulo": "O Mistério dos Tubos de Moedas",
            "enunciado": "O banco guarda moedas raras em três tubos verticais. A máquina só consegue liberar a moeda que está [b]no topo de cada tubo[/b].\n\n• [b]Tubo A[/b] (de cima para baixo): R$ 4, R$ 8.\n• [b]Tubo B[/b]: R$ 3, R$ 9.\n• [b]Tubo C[/b]: R$ 2, R$ 6.\n\nPara liberar as moedas da [b]MENOR[/b] para a [b]MAIOR[/b], qual deve ser a ordem em que você vai acionar os tubos?",
            "opcoes": [
                {"texto": "C, B, A, C, A, B", "correta": True},
                {"texto": "C, B, A, C, B, A", "correta": False},
                {"texto": "C, A, B, C, B, A", "correta": False},
                {"texto": "B, C, A, A, B, C", "correta": False}
            ],
            "explicacao": "Lógica Perfeita! O topo inicial tem 4, 3 e 2. Você libera o C (R$ 2). O novo topo de C vira 6. Agora os topos são 4, 3 e 6. O menor é B (R$ 3), depois A (R$ 4). O novo topo tem A(8), B(9), C(6). Libera-se C(6), depois A(8) e por fim B(9)."
        },
        {
            "titulo": "A Fila do Servidor",
            "enunciado": "Para o aplicativo do banco não travar, o servidor precisa organizar a fila de pagamentos. A regra de ouro do algoritmo é: a transação [b]mais rápida de ser processada passa primeiro![/b]\n\nPagamentos na fila de espera:\n• Pix da Ana: 5 segundos\n• Boleto do Beto: 10 segundos\n• Transferência do Carlos: 7 segundos\n• Cheque do Daniel: 12 segundos\n• Depósito do Elias: 9 segundos\n\nQual será a ordem exata em que o servidor vai processar esses pagamentos?",
            "opcoes": [
                {"texto": "Ana, Beto, Carlos, Elias, Daniel.", "correta": False},
                {"texto": "Ana, Carlos, Elias, Beto, Daniel.", "correta": True},
                {"texto": "Daniel, Beto, Elias, Carlos, Ana.", "correta": False},
                {"texto": "Ana, Carlos, Beto, Elias, Daniel.", "correta": False}
            ],
            "explicacao": "Otimização perfeita! O algoritmo ordena os processos do menor tempo para o maior: 5s (Ana), 7s (Carlos), 9s (Elias), 10s (Beto) e 12s (Daniel)."
        },
        {
            "titulo": "A Rota do Dinheiro",
            "enunciado": "Um auditor precisa resolver as dívidas de três bancos fazendo uma [b]única viagem[/b] e carregando uma maleta. Ao visitar um banco, ele entrega o dinheiro que está na maleta e recolhe a dívida para o próximo.\n\nDívidas na mesa:\n• O Banco A deve ao Banco C.\n• O Banco B deve ao Banco A.\n• O Banco C deve ao Banco B.\n\nComeçando com a maleta vazia, qual é a ordem de visita para resolver tudo passando [b]apenas uma vez[/b] em cada banco?",
            "opcoes": [
                {"texto": "Visitar B, depois C, depois A.", "correta": False},
                {"texto": "Visitar A, depois C, depois B.", "correta": True},
                {"texto": "Visitar C, depois B, depois A.", "correta": False},
                {"texto": "A ordem não importa.", "correta": False}
            ],
            "explicacao": "Roteamento validado! Ao visitar A, a maleta pega o dinheiro para o Banco C. Ele visita C, entrega o dinheiro e pega o de B. Visita B, entrega o dinheiro e pega o de A, finalizando a cadeia com sucesso."
        },
        {
            "titulo": "Mapa de Fiadores",
            "enunciado": "O banco usa um mapa de setas para entender quem garante a dívida de quem. Se a pessoa X tem uma seta apontando para a pessoa Y, significa que [b]X é o 'fiador'[/b] (quem paga a dívida se Y não pagar).\n\nMapa atual:\n• Ana aponta para Carlos.\n• Bia aponta para Carlos.\n• Carlos aponta para Diego.\n\nAnalisando esse mapa, qual é a [b]única[/b] afirmação correta?",
            "opcoes": [
                {"texto": "Ana e Bia garantem a dívida uma da outra.", "correta": False},
                {"texto": "Se Carlos não conseguir pagar sua dívida, Ana e Bia terão que pagar por ele.", "correta": True},
                {"texto": "Diego é o fiador de Carlos.", "correta": False},
                {"texto": "Carlos não possui fiadores.", "correta": False}
            ],
            "explicacao": "Exato! A direção das setas no grafo demonstra quem assume o risco. Como Ana e Bia apontam para Carlos, ambas são fiadoras dele."
        },
        {
            "titulo": "O Caminho do Investimento",
            "enunciado": "Um robô investidor distribui o dinheiro seguindo comandos de direção ([b]E[/b] = Esquerda, [b]D[/b] = Direita). O dinheiro sai da Conta Principal.\n\n• Virar à 'E' leva para a Renda Fixa.\n• Virar à 'D' leva para a Renda Variável.\n• Estando na Renda Fixa, virar à 'D' leva para o Tesouro Direto.\n• Estando na Renda Variável, virar à 'E' leva para Ações.\n\nSe o robô receber o comando [b]'E, D'[/b], onde o seu dinheiro vai parar?",
            "opcoes": [
                {"texto": "Renda Variável.", "correta": False},
                {"texto": "Ações.", "correta": False},
                {"texto": "Tesouro Direto.", "correta": True},
                {"texto": "Conta Central.", "correta": False}
            ],
            "explicacao": "Trilha processada! O primeiro comando 'E' leva o capital para a Renda Fixa. O segundo comando 'D' roteia esse capital diretamente para o Tesouro Direto."
        },
        {
            "titulo": "A Máquina de Senhas",
            "enunciado": "O banco usa três máquinas de segurança que alteram a sua senha passo a passo para evitar invasões.\n\n• [b]Máquina 1:[/b] Adiciona o símbolo '#' no final da palavra.\n• [b]Máquina 2:[/b] Inverte a palavra de trás para frente.\n• [b]Máquina 3:[/b] Troca a primeira letra da palavra por 'X'.\n\nSe a senha original era [b]'BOLO'[/b] e passou pelas máquinas na ordem 1, depois 2, depois 3, como ficou a senha final?",
            "opcoes": [
                {"texto": "XOLOB#", "correta": False},
                {"texto": "XOLOB", "correta": True},
                {"texto": "#OLOX", "correta": False},
                {"texto": "X#OLO", "correta": False}
            ],
            "explicacao": "Criptografia concluída! A Máquina 1 gera 'BOLO#'. A Máquina 2 inverte tudo para '#OLOB'. A Máquina 3 substitui a primeira letra ('#') por 'X', resultando na senha 'XOLOB'."
        }
    ]

    def on_enter(self):
        # Sorteia 5 questões aleatórias do banco para criar uma prova única
        self.prova_sorteada = random.sample(self.banco_questoes, 5)
        self.questao_atual_idx = 0
        self.carregar_questao()

    def carregar_questao(self):
        questao = self.prova_sorteada[self.questao_atual_idx]
        self.titulo_fase = questao["titulo"]
        self.enunciado_texto = questao["enunciado"]
        
        # Embaralha as opções de A a D
        opcoes_embaralhadas = list(questao["opcoes"])
        random.shuffle(opcoes_embaralhadas)
        
        self.renderizar_opcoes(opcoes_embaralhadas)

    def renderizar_opcoes(self, opcoes):
        self.ids.container_opcoes.clear_widgets()
        letras = ["A", "B", "C", "D"]
        
        for index, op in enumerate(opcoes):
            card = MDCard(
                size_hint_y=None,
                height=dp(60),
                padding="16dp",
                radius=[10],
                md_bg_color=[0.85, 0.92, 0.98, 1],
                ripple_behavior=True
            )
            # Passa se a opção é a verdadeira ou falsa para a validação
            card.bind(on_release=lambda instance, is_correct=op["correta"]: self.processar_resposta(is_correct))
            
            label = MDLabel(
                text=f"[b]{letras[index]})[/b] {op['texto']}",
                markup=True,
                font_style="Body2",
                theme_text_color="Primary",
                valign="center"
            )
            card.add_widget(label)
            self.ids.container_opcoes.add_widget(card)

    def processar_resposta(self, is_correct):
        questao = self.prova_sorteada[self.questao_atual_idx]
        
        if is_correct:
            titulo = "Lógica Validada!"
            texto = questao["explicacao"]
            
            if self.questao_atual_idx < 4: # Se for menor que a 5ª questão (índice 4)
                botao_acao = self.proxima_questao
            else:
                texto += "\n\n🏆 PARABÉNS! Você superou o Módulo de Desafios Integradores. O seu domínio sobre abstração, algoritmos e matemática financeira está em nível de excelência!"
                botao_acao = self.concluir_modulo
        else:
            titulo = "Falha na Compilação"
            texto = "A sua lógica não fechou a equação. O sistema matemático não tolera falhas. Leia os dados novamente e repita a simulação."
            botao_acao = self.fechar_dialog

        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[MDFlatButton(text="ENTENDIDO", on_release=botao_acao)]
        )
        self.dialog.open()

    def proxima_questao(self, *args):
        self.dialog.dismiss()
        self.questao_atual_idx += 1
        self.carregar_questao()
        
    def fechar_dialog(self, *args):
        self.dialog.dismiss()

    def concluir_modulo(self, *args):
        self.dialog.dismiss()
        # Salva o progresso máximo no JSON
        app = MDApp.get_running_app()
        if app.nivel_modulo1 < 10:
            app.nivel_modulo1 = 10
            app.save_data()
        self.voltar()

    def voltar(self):
        self.manager.current = 'modulo1'