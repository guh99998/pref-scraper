from selenium.webdriver.common.by import By

from backend.config.selectors import ID_BOTAO_CERTIDAO_VALOR_VENAL
from backend.utils.waits import esperar_elemento_visivel, esperar_download_completo


class CertidaoValorVenalPage():
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_certidao_valor_venal(self):

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - certidao_valor_venal.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_CERTIDAO_VALOR_VENAL).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)