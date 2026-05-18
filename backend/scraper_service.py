import threading
from browser import Browser
from pages.home_page import HomePage

class ScraperService:
    def __init__(self):
        self._driver = None
        self._lock = threading.Lock()
        self._inscricao_page = None
        self._inscricao = None
        self._pasta_download = None

    def _garantir_driver(self, pasta_download: str):
        if self._driver is not None:
            try:
                _ = self._driver.title
            except Exception:
                self._driver = None
                self._inscricao_page = None

        if self._driver is None:
            self._driver = Browser.criar_driver_segundo_plano(pasta_download)

    def _voltar_para_inscricao(self):
        from pages.inscricao_home_page import InscricaoHomePage
        from config.selectors import XPATH_DIV_VOLTAR_INICIO
        from utils.waits import esperar_elemento_clicavel
        from selenium.webdriver.common.by import By
        try:
            esperar_elemento_clicavel(self._driver, By.XPATH, XPATH_DIV_VOLTAR_INICIO).click()
            self._inscricao_page = InscricaoHomePage(self._driver)
        except Exception:
            self._inscricao_page = None
            if self._inscricao and self._pasta_download:
                home = HomePage(self._driver)
                home.acessar_pagina_inicial_imovel()
                home.preencher_campo_inscricao(self._inscricao)
                inscricao_page = home.clicar_botao_validar()
                informacoes = inscricao_page.acessar_informacoes_completas()
                self._inscricao_page = informacoes.voltar_para_inscricao_home_page()

    def buscar_imovel(self, inscricao: str, pasta_download: str) -> dict:
        with self._lock:
            self._garantir_driver(pasta_download)
            self._inscricao = inscricao
            self._pasta_download = pasta_download
            home = HomePage(self._driver)
            home.acessar_pagina_inicial_imovel()
            home.preencher_campo_inscricao(inscricao)
            inscricao_page = home.clicar_botao_validar()
            informacoes = inscricao_page.acessar_informacoes_completas()
            self._inscricao_page = informacoes.voltar_para_inscricao_home_page()
            return self._driver.dados_imovel

    def gerar_pdf_extrato(self) -> str:
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_consultar_movimentacoes_extrato()
            resultado = page.gerar_pdf_movimentacoes_extrato()
            self._voltar_para_inscricao()
            return resultado

    def gerar_pdf_certidao_negativa(self) -> str:
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_certidao_negativa_de_debitos()
            resultado = page.gerar_pdf_certidao_negativa_debitos()
            self._voltar_para_inscricao()
            return resultado

    def gerar_pdf_existencia(self) -> str:
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_certidao_de_existencia()
            resultado = page.gerar_pdf_certidao_existencia_imovel()
            self._voltar_para_inscricao()
            return resultado

    def gerar_pdf_valor_venal(self) -> str:
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_certidao_de_valor_venal()
            resultado = page.gerar_pdf_certidao_valor_venal()
            self._voltar_para_inscricao()
            return resultado

    def gerar_pdf_carne_iptu(self) -> str:
        from selenium.common.exceptions import TimeoutException
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_emitir_carne_de_iptu()
            try:
                resultado = page.gerar_carne_iptu()
            except TimeoutException:
                self._voltar_para_inscricao()
                raise RuntimeError("Nenhum carnê de IPTU disponível — IPTU já quitado ou sem parcelas em aberto")
            self._voltar_para_inscricao()
            return resultado

    def gerar_pdf_listagem_iptu(self) -> str:
        with self._lock:
            if self._inscricao_page is None:
                raise RuntimeError("Busque um imóvel antes de gerar documentos")
            page = self._inscricao_page.acessar_emitir_carne_de_iptu()
            resultado = page.gerar_pdf_listagem_iptu()
            self._voltar_para_inscricao()
            return resultado

    def obter_informacoes(self, inscricao: str, pasta_download: str) -> dict:
        with self._lock:
            self._garantir_driver(pasta_download)
            self._inscricao = inscricao
            self._pasta_download = pasta_download
            home = HomePage(self._driver)
            home.acessar_pagina_inicial_imovel()
            home.preencher_campo_inscricao(inscricao)
            inscricao_page = home.clicar_botao_validar()
            informacoes = inscricao_page.acessar_informacoes_completas()
            self._inscricao_page = informacoes.voltar_para_inscricao_home_page()

            debitos_page = self._inscricao_page.acessar_debitos_em_aberto()
            existe_debito = debitos_page._existe_debitos_em_aberto()
            self._voltar_para_inscricao()

            dados = self._driver.dados_imovel
            return {
                "quadra": dados["quadra"],
                "lote": dados["lote"],
                "nome_proprietario": dados["nome_proprietario"],
                "existe_debito": existe_debito,
            }

scraper = ScraperService()
