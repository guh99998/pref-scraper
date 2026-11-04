from selenium.webdriver.common.by import By

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import XPATH_BOTAO_CERTIDAO_NEGATIVA_DEBITOS
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class CertidaoNegativaDebitosPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_certidao_negativa_debitos(self):
        botao = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BOTAO_CERTIDAO_NEGATIVA_DEBITOS)
        nome = nome_documento(self.driver.dados_imovel, "certidao_negativa")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
