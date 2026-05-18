from backend.config.selectors import LINK_TEXT_IMOBILIARIO, XPATH_BOTAO_VALIDAR_INSCRICAO, XPATH_CAMPO_INSCRICAO
from selenium.webdriver.common.by import By
from backend.pages.inscricao_home_page import InscricaoHomePage
from backend.utils.waits import esperar_elemento_clicavel


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
        return InscricaoHomePage(self.driver)
