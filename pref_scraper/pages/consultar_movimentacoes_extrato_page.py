from selenium.webdriver.common.by import By

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import ID_BOTAO_MOVIMENTACOES_EXTRATO
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class ConsultarMovimentacoesExtratoPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_movimentacoes_extrato(self):
        botao = esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_MOVIMENTACOES_EXTRATO)
        nome = nome_documento(self.driver.dados_imovel, "extrato")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
