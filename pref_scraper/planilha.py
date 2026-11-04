from pathlib import Path

import pandas as pd


class PlanilhaError(Exception):
    """Erro ao ler a planilha de inscrições (mensagem pronta para o usuário)."""


def ler_inscricoes(arquivo, coluna: str) -> list[str]:
    arquivo = Path(arquivo)
    if not arquivo.exists():
        raise PlanilhaError(f"Arquivo não encontrado: {arquivo}")
    if arquivo.suffix.lower() != ".xlsx":
        raise PlanilhaError(f"Formato não suportado ({arquivo.suffix}): use um arquivo .xlsx")

    try:
        df = pd.read_excel(arquivo, dtype=str)
    except Exception as e:
        raise PlanilhaError(f"Não foi possível ler a planilha: {e}") from e

    alvo = coluna.strip().lower()
    encontrada = next((c for c in df.columns if str(c).strip().lower() == alvo), None)
    if encontrada is None:
        disponiveis = ", ".join(str(c) for c in df.columns)
        raise PlanilhaError(f"Coluna '{coluna}' não encontrada. Colunas disponíveis: {disponiveis}")

    inscricoes = [v.strip() for v in df[encontrada].dropna() if v.strip()]
    if not inscricoes:
        raise PlanilhaError(f"Nenhuma inscrição encontrada na coluna '{coluna}'")
    return inscricoes
