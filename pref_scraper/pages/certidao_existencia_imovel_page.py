from selenium.webdriver.common.by import By

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import ID_BOTAO_CERTIDAO_EXISTENCIA
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class CertidaoDeExistenciaPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_certidao_existencia_imovel(self):
        botao = esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_CERTIDAO_EXISTENCIA)
        nome = nome_documento(self.driver.dados_imovel, "certidao_existencia")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
