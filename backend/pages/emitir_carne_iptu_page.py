from selenium.webdriver.common.by import By

from backend.config.selectors import ID_BOTAO_LISTAGEM_IPTU, ID_BOTAO_CARNE_IPTU
from backend.utils.waits import esperar_elemento_visivel, esperar_download_completo


class EmitirCarneIptuPage:
    def __init__(self,driver):
        self.driver = driver

    def gerar_pdf_listagem_iptu(self):

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - listagem_iptu.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_LISTAGEM_IPTU).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)

    def gerar_carne_iptu(self):

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - IPTU.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_CARNE_IPTU).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)