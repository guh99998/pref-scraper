from selenium.webdriver.common.by import By

from config.selectors import ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL, XPATH_DIV_VOLTAR_INICIO
from utils.campos import valor_do_campo
from utils.waits import esperar_elemento_visivel, esperar_elemento_clicavel, esperar_download_completo

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
        self.obter_dados_completos()

    def obter_dados_completos(self):
        self.nome_proprietario = valor_do_campo(self.driver, "Proprietário")
        self.doc_proprietario = valor_do_campo(self.driver, "CPF")
        self.nome_bairro = valor_do_campo(self.driver, "Bairro")
        self.quadra = valor_do_campo(self.driver, "Quadra")
        self.lote = valor_do_campo(self.driver, "Lote")
        self.logradouro = valor_do_campo(self.driver, "Logradouro")
        self.numero = valor_do_campo(self.driver, "Número")
        self.complemento = valor_do_campo(self.driver, "Complemento")
        self.driver.dados_imovel = {
            "bairro": self.nome_bairro,
            "quadra": self.quadra.lstrip("0"),
            "lote": self.lote.lstrip("0"),
            "logradouro": self.logradouro,
            "numero": self.numero.lstrip("0"),
            "complemento": self.complemento,
            "nome_proprietario": self.nome_proprietario,
            "doc_proprietario": self.doc_proprietario
        }

    def voltar_para_inscricao_home_page(self):
        from pages.inscricao_home_page import InscricaoHomePage
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_DIV_VOLTAR_INICIO).click()
        return InscricaoHomePage(self.driver)

    def pdf_ficha_cadastral_lotes(self):
        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL).click()
        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=f"Ficha Cadastral - {self.nome_bairro} ({self.quadra.lstrip('0')}_{self.lote.lstrip('0')}).pdf")

    def pdf_ficha_cadastral_residencial(self):
        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL).click()
        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=f"Ficha Cadastral - {self.nome_bairro} ({self.logradouro}_{self.numero.lstrip('0')}) {self.complemento}.pdf")
