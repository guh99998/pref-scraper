import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from schemas import BuscarImovelRequest, DadosImovelResponse, PDFResponse, InformacoesImovelResponse
from scraper_service import scraper


app = FastAPI(title="Pref Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/imovel/buscar", response_model=DadosImovelResponse)
def buscar_imovel(body: BuscarImovelRequest):
    try:
        dados = scraper.buscar_imovel(body.inscricao, body.pasta_download)
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/pdf/extrato", response_model=PDFResponse)
def gerar_extrato():
    try:
        return {"caminho_arquivo": scraper.gerar_pdf_extrato()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/pdf/certidao-negativa", response_model=PDFResponse)
def gerar_certidao_negativa():
    try:
        return {"caminho_arquivo": scraper.gerar_pdf_certidao_negativa()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/pdf/existencia", response_model=PDFResponse)
def gerar_existencia():
    try:
        return {"caminho_arquivo": scraper.gerar_pdf_existencia()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/pdf/valor-venal", response_model=PDFResponse)
def gerar_valor_venal():
    try:
        return {"caminho_arquivo": scraper.gerar_pdf_valor_venal()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/pdf/carne-iptu", response_model=PDFResponse)
def gerar_carne_iptu():
    try:
        return {"caminho_arquivo": scraper.gerar_pdf_carne_iptu()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/imovel/informacoes", response_model=InformacoesImovelResponse)
def obter_informacoes(body: BuscarImovelRequest):
    try:
        return scraper.obter_informacoes(body.inscricao, body.pasta_download)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/imovel/pdf/download")
def download_pdf(caminho: str):
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(
        caminho,
        media_type="application/pdf",
        filename=os.path.basename(caminho)
    )