from pydantic import BaseModel

class BuscarImovelRequest(BaseModel):
    inscricao: str
    pasta_download: str

class DadosImovelResponse(BaseModel):
    nome_proprietario: str
    doc_proprietario: str
    bairro: str
    quadra: str
    lote: str
    logradouro: str
    numero: str
    complemento: str

class PDFResponse(BaseModel):
    caminho_arquivo: str

class InformacoesImovelResponse(BaseModel):
    quadra: str
    lote: str
    nome_proprietario: str
    existe_debito: bool
