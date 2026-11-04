from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pref_scraper.browser import Browser
from pref_scraper.config.selectors import XPATH_DIV_VOLTAR_INICIO
from pref_scraper.documentos import Documento
from pref_scraper.models import DadosImovel, InformacoesImovel
from pref_scraper.pages.home_page import HomePage
from pref_scraper.pages.inscricao_home_page import InscricaoHomePage
from pref_scraper.utils.waits import esperar_elemento_clicavel


class ScraperService:
    """Orquestra o fluxo no portal. Use como context manager para o Chrome ser sempre fechado.

    Com `headless=False` (--visivel) a janela é mantida aberta ao final, para debug.
    """

    def __init__(self, pasta_download, headless: bool = True, driver=None):
        self._pasta_download = str(pasta_download)
        self._headless = headless
        self._driver = driver
        self._inscricao = None
        self._inscricao_page = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.fechar()

    @property
    def driver(self):
        if self._driver is None:
            criar = Browser.criar_driver_segundo_plano if self._headless else Browser.criar_driver_primeiro_plano
            self._driver = criar(self._pasta_download)
        return self._driver

    @property
    def dados(self) -> DadosImovel | None:
        return getattr(self._driver, "dados_imovel", None)

    def fechar(self):
        driver, self._driver = self._driver, None
        self._inscricao_page = None
        if driver is not None and self._headless:
            driver.quit()

    # --- navegação ---------------------------------------------------------

    def _abrir_inscricao(self):
        home = HomePage(self.driver)
        home.acessar_pagina_inicial_imovel()
        home.preencher_campo_inscricao(self._inscricao)
        informacoes = home.clicar_botao_validar().acessar_informacoes_completas()
        self._inscricao_page = informacoes.voltar_para_inscricao_home_page()

    def _voltar_para_inscricao(self):
        """Volta ao menu do imóvel; se falhar, tenta reabrir. Nunca levanta: não pode mascarar o erro original."""
        try:
            esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_DIV_VOLTAR_INICIO).click()
            self._inscricao_page = InscricaoHomePage(self.driver)
        except Exception:
            self._inscricao_page = None
            try:
                self._abrir_inscricao()
            except Exception:
                self._inscricao_page = None

    def _gerar(self, acessar, gerar):
        """Acessa uma tela do imóvel e gera algo nela, voltando ao menu mesmo em caso de falha."""
        if self._inscricao_page is None:
            raise RuntimeError("Busque um imóvel antes de gerar documentos")
        try:
            return gerar(acessar(self._inscricao_page))
        finally:
            self._voltar_para_inscricao()

    # --- operações públicas -----------------------------------------------

    def buscar_imovel(self, inscricao: str) -> DadosImovel:
        self._inscricao = inscricao
        self._inscricao_page = None
        self._abrir_inscricao()
        return self.dados

    def obter_informacoes(self, inscricao: str) -> InformacoesImovel:
        dados = self.buscar_imovel(inscricao)
        existe_debito = self._gerar(
            lambda inicio: inicio.acessar_debitos_em_aberto(),
            lambda page: page.existe_debito_vencido(),
        )
        return InformacoesImovel(
            quadra=dados.quadra,
            lote=dados.lote,
            nome_proprietario=dados.nome_proprietario,
            existe_debito=existe_debito,
        )

    def gerar(self, documento: Documento) -> Path:
        return getattr(self, documento.metodo)()

    def gerar_pdf_extrato(self) -> Path:
        return self._gerar(
            lambda inicio: inicio.acessar_consultar_movimentacoes_extrato(),
            lambda page: page.gerar_pdf_movimentacoes_extrato(),
        )

    def gerar_pdf_certidao_negativa(self) -> Path:
        return self._gerar(
            lambda inicio: inicio.acessar_certidao_negativa_de_debitos(),
            lambda page: page.gerar_pdf_certidao_negativa_debitos(),
        )

    def gerar_pdf_existencia(self) -> Path:
        return self._gerar(
            lambda inicio: inicio.acessar_certidao_de_existencia(),
            lambda page: page.gerar_pdf_certidao_existencia_imovel(),
        )

    def gerar_pdf_valor_venal(self) -> Path:
        return self._gerar(
            lambda inicio: inicio.acessar_certidao_de_valor_venal(),
            lambda page: page.gerar_pdf_certidao_valor_venal(),
        )

    def gerar_pdf_listagem_iptu(self) -> Path:
        return self._gerar(
            lambda inicio: inicio.acessar_emitir_carne_de_iptu(),
            lambda page: page.gerar_pdf_listagem_iptu(),
        )

    def gerar_pdf_carne_iptu(self) -> Path:
        def gerar(page):
            try:
                return page.gerar_carne_iptu()
            except TimeoutException as e:
                raise RuntimeError(
                    "Nenhum carnê de IPTU disponível — IPTU já quitado ou sem parcelas em aberto"
                ) from e

        return self._gerar(lambda inicio: inicio.acessar_emitir_carne_de_iptu(), gerar)
