from selenium.webdriver.common.by import By

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import ID_BOTAO_CERTIDAO_VALOR_VENAL
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class CertidaoValorVenalPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_certidao_valor_venal(self):
        botao = esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_CERTIDAO_VALOR_VENAL)
        nome = nome_documento(self.driver.dados_imovel, "certidao_valor_venal")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
