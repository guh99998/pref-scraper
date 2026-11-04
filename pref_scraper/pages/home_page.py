from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pref_scraper.config.selectors import (
    ID_CAMPO_CABECALHO_CPF_CNPJ,
    LINK_TEXT_IMOBILIARIO,
    XPATH_BOTAO_VALIDAR_INSCRICAO,
    XPATH_CAMPO_INSCRICAO,
    XPATH_ERRO_VALIDACAO_INSCRICAO,
)
from pref_scraper.pages.inscricao_home_page import InscricaoHomePage
from pref_scraper.utils.waits import esperar_elemento_clicavel


class InscricaoInvalidaError(RuntimeError):
    """O portal rejeitou a inscrição (ou não respondeu como esperado)."""


def aguardar_validacao(driver, timeout=10):
    """Espera o resultado do 'validar': o menu do imóvel (sucesso) ou a mensagem de erro do portal."""

    def resultado(d):
        erros = d.find_elements(By.XPATH, XPATH_ERRO_VALIDACAO_INSCRICAO)
        if erros and erros[0].text.strip():
            return ("erro", erros[0].text.strip())
        if d.find_elements(By.ID, ID_CAMPO_CABECALHO_CPF_CNPJ):
            return ("ok", None)
        return False

    try:
        tipo, mensagem = WebDriverWait(driver, timeout).until(resultado)
    except TimeoutException as e:
        raise InscricaoInvalidaError("O portal não respondeu como esperado ao validar a inscrição") from e
    if tipo == "erro":
        raise InscricaoInvalidaError(mensagem)


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def acessar_pagina_inicial_imovel(self):
        self.driver.get("https://nfe.sgpcloud.net:9175/servicosweb/home.jsf")
        self.driver.find_element(By.LINK_TEXT, LINK_TEXT_IMOBILIARIO).click()

    def preencher_campo_inscricao(self, incricao):
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_CAMPO_INSCRICAO).send_keys(incricao)

    def clicar_botao_validar(self):
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_BOTAO_VALIDAR_INSCRICAO).click()
        aguardar_validacao(self.driver)
        return InscricaoHomePage(self.driver)
