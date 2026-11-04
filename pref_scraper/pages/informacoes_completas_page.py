from selenium.webdriver.common.by import By

from pref_scraper.config.selectors import XPATH_BOTAO_IMPRIMIR_FICHA_CADASTRAL, XPATH_DIV_VOLTAR_INICIO
from pref_scraper.models import DadosImovel
from pref_scraper.utils.campos import valor_do_campo
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_clicavel, esperar_elemento_visivel


class InformacoesCompletasPage:
    def __init__(self, driver):
        self.driver = driver
        self.dados = self.obter_dados_completos()

    def obter_dados_completos(self) -> DadosImovel:
        lido = lambda rotulo: valor_do_campo(self.driver, rotulo)  # noqa: E731
        dados = DadosImovel(
            bairro=lido("Bairro"),
            quadra=lido("Quadra").lstrip("0"),
            lote=lido("Lote").lstrip("0"),
            logradouro=lido("Logradouro"),
            numero=lido("Número").lstrip("0"),
            complemento=lido("Complemento"),
            nome_proprietario=lido("Proprietário"),
            doc_proprietario=lido("CPF"),
        )
        self.driver.dados_imovel = dados
        return dados

    def voltar_para_inscricao_home_page(self):
        from pref_scraper.pages.inscricao_home_page import InscricaoHomePage
        esperar_elemento_clicavel(self.driver, By.XPATH, XPATH_DIV_VOLTAR_INICIO).click()
        return InscricaoHomePage(self.driver)

    def pdf_ficha_cadastral_lotes(self):
        d = self.dados
        botao = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BOTAO_IMPRIMIR_FICHA_CADASTRAL)
        nome = f"Ficha Cadastral - {d.bairro} ({d.quadra}_{d.lote}).pdf"
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)

    def pdf_ficha_cadastral_residencial(self):
        d = self.dados
        botao = esperar_elemento_visivel(self.driver, By.XPATH, XPATH_BOTAO_IMPRIMIR_FICHA_CADASTRAL)
        nome = f"Ficha Cadastral - {d.bairro} ({d.logradouro}_{d.numero}) {d.complemento}.pdf"
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
