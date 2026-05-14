from selenium.webdriver.common.by import By
from utils.waits import esperar_elemento_clicavel
from pages.debitos_em_aberto_page import DebitosEmAbertoPage
from config.selectors import XPATH_PAGINA_DEBITOS

class InscricaoHomePage:
    def __init__(self, driver):
        self.driver = driver

    def acessar_informacoes_completas(self):
        pass

    def acessar_debitos_em_aberto(self):
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_PAGINA_DEBITOS).click()
        return DebitosEmAbertoPage(self.driver)

    def acessar_certidao_negativa_de_debitos(self):
        pass

    def acessar_certidao_de_existencia(self):
        pass

    def acessar_certidao_de_valor_venal(self):
        pass

    def acessar_emitir_carne_de_iptu(self):
        pass

    def acessar_consultar_movimentacoes_extrato(self):
        pass