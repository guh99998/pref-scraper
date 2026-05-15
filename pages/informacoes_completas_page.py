from selenium.webdriver.common.by import By

from config.selectors import XPATH_NOME_PROPRIETARIO_TELA_DADOS, \
    XPATH_DOC_PROPRIETARIO_TELA_DADOS, XPATH_BAIRRO_DADOS_GERAIS, XPATH_QUADRA_DADOS_GERAIS, XPATH_LOTE_DADOS_GERAIS, \
    XPATH_LOGRADOURO_DADOS_GERAIS, XPATH_NUMERO_DADOS_GERAIS, XPATH_COMPLEMENTO_DADOS_GERAIS, \
    ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL
from utils.waits import esperar_elemento_visivel, esperar_download_completo

class InformacoesCompletasPage:
    def __init__(self, driver):
        self.driver = driver
        self.nome_proprietario = ""
        self.doc_proprietario = ""
        self.nome_bairro = ""
        self.quadra = ""
        self.lote = ""
        self.logradouro = ""
        self.numero = ""
        self.complemento = ""
        self._obter_dados_completos()


    def _obter_dados_completos(self):
        self.nome_proprietario = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_NOME_PROPRIETARIO_TELA_DADOS).text
        self.doc_proprietario = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_DOC_PROPRIETARIO_TELA_DADOS).text
        self.nome_bairro = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BAIRRO_DADOS_GERAIS).text
        self.quadra = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_QUADRA_DADOS_GERAIS).text
        self.lote = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_LOTE_DADOS_GERAIS).text
        self.logradouro = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_LOGRADOURO_DADOS_GERAIS).text
        self.numero = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_NUMERO_DADOS_GERAIS).text
        self.complemento = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_COMPLEMENTO_DADOS_GERAIS).text


    def pdf_ficha_cadastral_lotes(self):
        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL).click()
        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=f"Ficha Cadastral - {self.nome_bairro} ({self.quadra.lstrip('0')}_{self.lote.lstrip('0')}).pdf")

    def pdf_ficha_cadastral_residencial(self):
        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL).click()
        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=f"Ficha Cadastral - {self.nome_bairro} ({self.logradouro}_{self.numero.lstrip('0')}) {self.complemento}.pdf")
