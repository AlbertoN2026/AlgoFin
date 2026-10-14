r"""
executar_trechos.py — Executa os trechos de código reproduzidos na dissertação
(versão anterior e versão corrigida) com entradas de teste e registra o que
cada um devolve.

Uso:   python3 executar_trechos.py
Saída: saida/execucao_trechos.md  e  saida/tabelas_latex/tab_execucao_trechos.tex

Não depende do Kivy: o objeto da tela é simulado com os mesmos nomes de
widgets usados no código (self.ids.input_capital etc.).
"""
import importlib.util
import os
import sys
import tempfile
import types

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
COD = os.path.join(RAIZ, "codigos")
SAIDA = os.path.join(AQUI, "saida")
TEX = os.path.join(SAIDA, "tabelas_latex")
os.makedirs(TEX, exist_ok=True)

# --- Kivy simulado: App.get_running_app().user_data_dir -----------------------
_pasta_app = {"dir": tempfile.mkdtemp()}
kivy = types.ModuleType("kivy")
kivy_app = types.ModuleType("kivy.app")


class _App:
    @staticmethod
    def get_running_app():
        return types.SimpleNamespace(user_data_dir=_pasta_app["dir"])


kivy_app.App = _App
sys.modules.setdefault("kivy", kivy)
sys.modules.setdefault("kivy.app", kivy_app)


def carrega(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ant_mvc = carrega(os.path.join(COD, "versao_anterior", "mvc_exemplo.py"), "ant_mvc")
nov_mvc = carrega(os.path.join(COD, "mvc_exemplo.py"), "nov_mvc")
ant_per = carrega(os.path.join(COD, "versao_anterior", "persistencia_exemplo.py"), "ant_per")
nov_per = carrega(os.path.join(COD, "persistencia_exemplo.py"), "nov_per")


class Campo:
    def __init__(self, t=""):
        self.text = t


def juros(mod, cap, tx, tp):
    tela = types.SimpleNamespace(ids=types.SimpleNamespace(
        input_capital=Campo(cap), input_taxa=Campo(tx), input_tempo=Campo(tp),
        lbl_resultado_juros=Campo()))
    try:
        mod.simular_juros(tela)
    except Exception as e:  # registra falhas não tratadas
        return f"exceção {type(e).__name__}"
    texto = tela.ids.lbl_resultado_juros.text.split("\n")[0]
    if texto.startswith("Use números não negativos"):
        return "Mensagem de orientação (números não negativos, meses inteiros, exemplos)"
    return texto


CASOS_JUROS = [
    ("1000", "1", "12", "Valores típicos"),
    ("1000", "1,5", "12", "Taxa com vírgula decimal"),
    ("1.000", "1", "12", "Capital com ponto de milhar"),
    ("-1000", "1", "12", "Capital negativo"),
    ("1000", "-5", "12", "Taxa negativa"),
    ("1000", "1", "0", "Tempo zero"),
    ("1000", "0", "12", "Taxa zero"),
    ("1000", "1", "12,5", "Tempo não inteiro"),
    ("", "1", "12", "Campo vazio"),
]

linhas_juros = []
for cap, tx, tp, desc in CASOS_JUROS:
    linhas_juros.append((desc, f"C={cap!r}, i={tx!r}, n={tp!r}",
                         juros(ant_mvc, cap, tx, tp), juros(nov_mvc, cap, tx, tp)))


# --- Persistência ------------------------------------------------------------
def estudante():
    return types.SimpleNamespace(user_name="Ana", escola="E. M. Exemplo", turma="7A",
                                 moedas=3, nivel_modulo1=2, nivel_modulo2=1, nivel_modulo3=1)


def chama(f, obj):
    try:
        r = f(obj)
        return "ok" if r is None or r is True else f"retornou {r!r}"
    except Exception as e:
        return f"exceção {type(e).__name__}"


linhas_pers = []
orig_cwd = os.getcwd()

# 1. Salvar e reabrir
d = tempfile.mkdtemp(); os.chdir(d); _pasta_app["dir"] = d
a = estudante(); r_ant_s = chama(ant_per.save_data, a)
b = types.SimpleNamespace(); r_ant_l = chama(ant_per.load_data, b)
a2 = estudante(); r_nov_s = chama(nov_per.save_data, a2)
b2 = types.SimpleNamespace(); r_nov_l = chama(nov_per.load_data, b2)
linhas_pers.append(("Salvar o perfil e reabrir",
                    f"salvar: {r_ant_s}; reabrir: {r_ant_l}",
                    f"salvar: {r_nov_s}; reabrir: {r_nov_l}"
                    + ("; dados recuperados" if getattr(b2, "moedas", None) == 3 else "")))

# 2. Primeiro uso (sem arquivo)
d = tempfile.mkdtemp(); os.chdir(d); _pasta_app["dir"] = d
b = types.SimpleNamespace(); r_ant = chama(ant_per.load_data, b)
b2 = types.SimpleNamespace(); r_nov = chama(nov_per.load_data, b2)
linhas_pers.append(("Primeiro uso, sem arquivo salvo", r_ant,
                    r_nov + ("; valores padrão definidos" if getattr(b2, "moedas", None) == 0 else "")))

# 3. Arquivo corrompido
d = tempfile.mkdtemp(); os.chdir(d); _pasta_app["dir"] = d
open("user_data.json", "w").write("{corrompido")
b = types.SimpleNamespace(); r_ant = chama(ant_per.load_data, b)
ant_per.os = os  # mesmo supondo "import os" em outro ponto do arquivo:
b1 = types.SimpleNamespace(); chama(ant_per.load_data, b1)
del ant_per.os
sem_attr = "nenhum atributo definido" if not vars(b1) else "atributos definidos"
b2 = types.SimpleNamespace(); r_nov = chama(nov_per.load_data, b2)
linhas_pers.append(("Arquivo de dados corrompido",
                    f"{r_ant}; com \\texttt{{os}} importado: erro silenciado e {sem_attr}",
                    r_nov + ("; valores padrão e aviso ao estudante" if getattr(b2, "aviso_dados", "") else "")))

# 4. Falha de gravação
d = tempfile.mkdtemp(); os.chdir(d)
os.mkdir("user_data.json")  # impede a gravação no diretório corrente
a = estudante()
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    r_ant = chama(ant_per.save_data, a)
bloqueio = os.path.join(d, "arquivo_comum"); open(bloqueio, "w").close()
_pasta_app["dir"] = os.path.join(bloqueio, "sub")  # caminho impossível
a2 = estudante(); r_nov = chama(nov_per.save_data, a2)
linhas_pers.append(("Falha na gravação",
                    "sem aviso ao estudante; erro só no console (\\texttt{print})" if buf.getvalue() else r_ant,
                    r_nov + ("; aviso ao estudante" if getattr(a2, "aviso_dados", "") else "")))
os.chdir(orig_cwd)

# --- Saídas ------------------------------------------------------------------
md = ["# Execução dos trechos de código da dissertação", "",
      "## Simulador de juros (Código 1)", "",
      "| Caso | Entrada | Versão anterior | Versão corrigida |", "|---|---|---|---|"]
for desc, ent, ant, nov in linhas_juros:
    md.append(f"| {desc} | {ent} | {ant} | {nov} |")
md += ["", "## Persistência (Código 2)", "", "| Cenário | Versão anterior | Versão corrigida |", "|---|---|---|"]
for desc, ant, nov in linhas_pers:
    md.append(f"| {desc} | {ant.replace(chr(92)+'texttt{os}', 'os').replace(chr(92)+'texttt{print}', 'print')} | {nov} |")
open(os.path.join(SAIDA, "execucao_trechos.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


def esc(s):
    s = s.replace("\\texttt{os}", "@@OS@@").replace("\\texttt{print}", "@@PRINT@@")
    s = (s.replace("\\", "\\textbackslash{}").replace("$", "\\$").replace("%", "\\%")
         .replace("_", "\\_").replace("&", "\\&").replace("{", "\\{").replace("}", "\\}")
         .replace("'", "\\textquotesingle{}"))
    return s.replace("@@OS@@", "\\texttt{os}").replace("@@PRINT@@", "\\texttt{print}")


with open(os.path.join(TEX, "tab_execucao_trechos.tex"), "w", encoding="utf-8") as f:
    f.write("% Gerado por executar_trechos.py — não editar à mão\n")
    f.write("\\begin{table}[htb]\n\\centering\n\\caption{Execução do trecho do simulador de juros "
            "(Código~\\ref{lst:mvc}) na versão anterior e na corrigida}\n\\label{tab:execucao-juros}\n\\footnotesize\n")
    f.write("\\begin{tabular}{L{2.7cm} L{3.4cm} L{4.0cm} L{4.0cm}}\n\\hline\n")
    f.write("Caso & Entrada & Versão anterior (1.ª linha da resposta) & Versão corrigida (1.ª linha da resposta) \\\\ \\hline\n")
    for desc, ent, ant, nov in linhas_juros:
        f.write(f"{esc(desc)} & {esc(ent)} & {esc(ant)} & {esc(nov)} \\\\ \\hline\n")
    f.write("\\end{tabular}\n\\par\\vspace{0.1cm}\n{\\small Fonte: Elaborada pelo autor (2026), "
            "com o script \\texttt{executar\\_trechos.py} (Apêndice~\\ref{ap:registro}).}\n\\end{table}\n\n")
    f.write("\\begin{table}[htb]\n\\centering\n\\caption{Execução do trecho de persistência "
            "(Código~\\ref{lst:json}) na versão anterior e na corrigida}\n\\label{tab:execucao-persistencia}\n\\footnotesize\n")
    f.write("\\begin{tabular}{L{3.2cm} L{5.6cm} L{5.6cm}}\n\\hline\n")
    f.write("Cenário & Versão anterior & Versão corrigida \\\\ \\hline\n")
    for desc, ant, nov in linhas_pers:
        f.write(f"{esc(desc)} & {esc(ant)} & {esc(nov)} \\\\ \\hline\n")
    f.write("\\end{tabular}\n\\par\\vspace{0.1cm}\n{\\small Fonte: Elaborada pelo autor (2026), "
            "com o script \\texttt{executar\\_trechos.py} (Apêndice~\\ref{ap:registro}).}\n\\end{table}\n")

print("\n".join(md))
