from dataclasses import dataclass


@dataclass(frozen=True)
class DadosImovel:
    bairro: str
    quadra: str
    lote: str
    logradouro: str
    numero: str
    complemento: str
    nome_proprietario: str
    doc_proprietario: str


@dataclass(frozen=True)
class InformacoesImovel:
    quadra: str
    lote: str
    nome_proprietario: str
    existe_debito: bool
