from selenium.webdriver.common.by import By

from pages.certidao_existencia_imovel_page import CertidaoDeExistenciaPage
from pages.certidao_negativa_debitos_page import CertidaoNegativaDebitosPage
from pages.certidao_valor_venal_page import CertidaoValorVenalPage
from pages.emitir_carne_iptu_page import EmitirCarneIptuPage
from pages.informacoes_completas_page import InformacoesCompletasPage
from utils.waits import esperar_elemento_clicavel, esperar_elemento_visivel
from pages.debitos_em_aberto_page import DebitosEmAbertoPage
from config.selectors import ID_PAGINA_DEBITOS, ID_PAGINA_INFORMACOES_COMPLETAS, \
    ID_FORMULARIO_PAGINA_INFORMACOES_COMPLETAS, ID_CAMPO_CABECALHO_CPF_CNPJ, XPATH_BOTAO_VALIDAR_DADOS, \
    ID_PAGINA_CERTIDAO_NEGATIVA_DEBITOS, ID_PAGINA_CERTIDAO_EXISTENCIA_IMOVEL, ID_PAGINA_CERTIDAO_VALOR_VENAL_IMOVEL, \
    ID_PAGINA_EMITIR_CARNE_IPTU


class InscricaoHomePage:
    def __init__(self, driver):
        self.driver = driver

    def acessar_informacoes_completas(self):
        doc_proprietario = esperar_elemento_visivel(self.driver, By.ID, ID_CAMPO_CABECALHO_CPF_CNPJ).text
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_INFORMACOES_COMPLETAS).click()
        esperar_elemento_clicavel(self.driver, By.ID, ID_FORMULARIO_PAGINA_INFORMACOES_COMPLETAS).send_keys(doc_proprietario)
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_BOTAO_VALIDAR_DADOS).click()
        return InformacoesCompletasPage(self.driver)

    def acessar_debitos_em_aberto(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_DEBITOS).click()
        return DebitosEmAbertoPage(self.driver)

    def acessar_certidao_negativa_de_debitos(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_CERTIDAO_NEGATIVA_DEBITOS).click()
        return CertidaoNegativaDebitosPage(self.driver)

    def acessar_certidao_de_existencia(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_CERTIDAO_EXISTENCIA_IMOVEL).click()
        return CertidaoDeExistenciaPage(self.driver)

    def acessar_certidao_de_valor_venal(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_CERTIDAO_VALOR_VENAL_IMOVEL).click()
        return CertidaoValorVenalPage(self.driver)

    def acessar_emitir_carne_de_iptu(self):
        esperar_elemento_clicavel(self.driver, By.ID, ID_PAGINA_EMITIR_CARNE_IPTU).click()
        return EmitirCarneIptuPage(self.driver)

    def acessar_consultar_movimentacoes_extrato(self):
        pass
