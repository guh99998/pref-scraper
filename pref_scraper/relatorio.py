import csv
from pathlib import Path

COLUNAS = ["inscricao", "proprietario", "quadra", "lote", "existe_debito", "erro"]


def gravar_resultados_csv(pasta, linhas: list[dict]) -> Path:
    """Grava resultados.csv em utf-8-sig (abre com acentos corretos no Excel)."""
    caminho = Path(pasta) / "resultados.csv"
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas)
    return caminho
