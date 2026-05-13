import pandas as pd


class LeituraArquivos:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def ler_arquivo_excel(self):
        df = pd.read_excel(self.arquivo, dtype=str)
        df.columns = df.columns.str.strip().str.upper()

        if "NOME" not in df.columns or "INSCRICAO" not in df.columns:
            raise ValueError(f"Colunas esperadas: NOME e INSCRICAO. Encontradas: {list(df.columns)}")

        df = df[["NOME", "INSCRICAO"]].dropna(subset=["INSCRICAO"])

        return [str(row["INSCRICAO"]).strip() for _, row in df.iterrows()]
