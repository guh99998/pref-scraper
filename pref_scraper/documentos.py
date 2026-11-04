from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Documento:
    flag: str    # nome da opção na CLI (--flag)
    nome: str    # nome legível
    metodo: str  # método de ScraperService que gera o PDF


DOCUMENTOS: tuple[Documento, ...] = (
    Documento("extrato", "Extrato de Pagamentos", "gerar_pdf_extrato"),
    Documento("certidao-negativa", "Certidão Negativa de Débitos", "gerar_pdf_certidao_negativa"),
    Documento("existencia", "Certidão de Existência", "gerar_pdf_existencia"),
    Documento("valor-venal", "Valor Venal", "gerar_pdf_valor_venal"),
    Documento("listagem-iptu", "Listagem de IPTUs", "gerar_pdf_listagem_iptu"),
    Documento("carne-iptu", "Carnê do IPTU", "gerar_pdf_carne_iptu"),
)


def selecionar(todos: bool, escolhidos: Iterable[str]) -> list[Documento]:
    escolhidos = set(escolhidos)
    desconhecidos = escolhidos - {d.flag for d in DOCUMENTOS}
    if desconhecidos:
        raise ValueError(f"Documento desconhecido: {', '.join(sorted(desconhecidos))}")
    if todos:
        return list(DOCUMENTOS)
    return [d for d in DOCUMENTOS if d.flag in escolhidos]
