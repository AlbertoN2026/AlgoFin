"""
config_segura.py — Leitura da credencial do Tutor IA sem chave no código.

Ordem de busca (a primeira que existir vence):
  1. variável de ambiente ALGOFIN_API_KEY           (desenvolvimento)
  2. arquivo .env na pasta do projeto, não versionado (desenvolvimento)
  3. arquivo tutor.cfg em App.user_data_dir          (chave digitada pelo professor
                                                      no próprio aparelho)
Se nenhuma existir, devolve None e o app deve exibir "Tutor indisponível".

Nunca registre a chave em log, print, mensagem de erro ou captura de tela.
"""
import json
import os
from typing import Optional

NOME_VARIAVEL = "ALGOFIN_API_KEY"


def _ler_env(caminho: str) -> Optional[str]:
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            nome, valor = linha.split("=", 1)
            if nome.strip() == NOME_VARIAVEL:
                return valor.strip().strip('"').strip("'") or None
    return None


def _pasta_dados_app() -> Optional[str]:
    try:
        from kivy.app import App
        app = App.get_running_app()
        return app.user_data_dir if app else None
    except Exception:
        return None


def obter_chave_api() -> Optional[str]:
    chave = os.environ.get(NOME_VARIAVEL)
    if chave:
        return chave
    chave = _ler_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
    if chave:
        return chave
    pasta = _pasta_dados_app()
    if pasta:
        caminho = os.path.join(pasta, "tutor.cfg")
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    return json.load(f).get("chave") or None
            except (OSError, ValueError):
                return None
    return None


def salvar_chave_professor(chave: str) -> bool:
    """Chamada pela tela de configuração do professor. Grava só no aparelho."""
    pasta = _pasta_dados_app()
    if not pasta or not chave.strip():
        return False
    try:
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, "tutor.cfg")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump({"chave": chave.strip()}, f)
        try:
            os.chmod(caminho, 0o600)   # leitura só pelo app (efeito em Linux/Android)
        except OSError:
            pass
        return True
    except OSError:
        return False


def remover_chave_professor() -> bool:
    """Apaga a chave gravada no aparelho. Devolve True se havia uma chave."""
    pasta = _pasta_dados_app()
    if not pasta:
        return False
    caminho = os.path.join(pasta, "tutor.cfg")
    try:
        os.remove(caminho)
        return True
    except OSError:
        return False


def tutor_disponivel() -> bool:
    return obter_chave_api() is not None
