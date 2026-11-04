from selenium.webdriver.common.by import By

from pref_scraper.config.selectors import ID_BOTAO_CERTIDAO_NEGATIVA_DEBITOS
from pref_scraper.utils.waits import esperar_elemento_visivel, esperar_download_completo


class CertidaoNegativaDebitosPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_certidao_negativa_debitos(self):

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - certidao_negativa.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_CERTIDAO_NEGATIVA_DEBITOS).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)
