from selenium.webdriver.common.by import By

from config.selectors import ID_BOTAO_MOVIMENTACOES_EXTRATO
from utils.waits import esperar_elemento_visivel, esperar_download_completo


class ConsultarMovimentacoesExtratoPage:
    def __init__(self, driver):
        self.driver = driver

    def gerar_pdf_movimentacoes_extrato(self):

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - extrato.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_MOVIMENTACOES_EXTRATO).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)