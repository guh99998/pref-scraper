from selenium.webdriver.common.by import By

from pages.informacoes_completas_page import InformacoesCompletasPage
from utils.waits import esperar_elemento_clicavel, esperar_elemento_visivel
from pages.debitos_em_aberto_page import DebitosEmAbertoPage
from config.selectors import ID_PAGINA_DEBITOS, XPATH_PAGINA_INFORMACOES_COMPLETAS, \
    ID_FORMULARIO_PAGINA_INFORMACOES_COMPLETAS, ID_CAMPO_CABECALHO_CPF_CNPJ, XPATH_BOTAO_VALIDAR_DADOS


class InscricaoHomePage:
    def __init__(self, driver):
        self.driver = driver

    def acessar_informacoes_completas(self):
        doc_proprietario = esperar_elemento_visivel(self.driver, By.ID, ID_CAMPO_CABECALHO_CPF_CNPJ).text
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_PAGINA_INFORMACOES_COMPLETAS).click()
        esperar_elemento_clicavel(self.driver, By.ID, ID_FORMULARIO_PAGINA_INFORMACOES_COMPLETAS).send_keys(doc_proprietario)
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_BOTAO_VALIDAR_DADOS).click()
        return InformacoesCompletasPage(self.driver)

    def acessar_debitos_em_aberto(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_DEBITOS).click()
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
