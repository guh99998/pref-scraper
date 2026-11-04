from selenium.webdriver.common.by import By

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import XPATH_BOTAO_CARNE_IPTU, XPATH_BOTAO_LISTAGEM_IPTU
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class EmitirCarneIptuPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_listagem_iptu(self):
        botao = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BOTAO_LISTAGEM_IPTU)
        nome = nome_documento(self.driver.dados_imovel, "listagem_iptu")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)

    def gerar_carne_iptu(self):
        botao = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BOTAO_CARNE_IPTU)
        nome = nome_documento(self.driver.dados_imovel, "IPTU")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
