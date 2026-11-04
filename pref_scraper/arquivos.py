import re
from pathlib import Path

from pref_scraper.models import DadosImovel

_INVALIDOS = re.compile(r'[<>:"/\|?*\x00-\x1f]')


def _limpar(texto: str) -> str:
    return _INVALIDOS.sub("-", texto).strip(" .")


def nome_documento(dados: DadosImovel, tipo: str) -> str:
    base = "_".join(_limpar(parte) for parte in (dados.bairro, dados.quadra, dados.lote))
    return f"{base} - {_limpar(tipo)}.pdf"


def caminho_livre(pasta, nome: str) -> Path:
    """Devolve um caminho que não existe ainda, usando sufixo ' (2)', ' (3)'... Nunca sobrescreve."""
    pasta = Path(pasta)
    candidato = pasta / nome
    if not candidato.exists():
        return candidato
    original = Path(nome)
    n = 2
    while True:
        candidato = pasta / f"{original.stem} ({n}){original.suffix}"
        if not candidato.exists():
            return candidato
        n += 1
