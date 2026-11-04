from datetime import date
from enum import Enum

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pref_scraper.arquivos import nome_documento
from pref_scraper.config.selectors import (
    ID_BOTAO_IMPRIMIR_TODOS_DEBITOS,
    XPATH_CABECALHO_VENCIMENTO,
    XPATH_LINHAS_DEBITOS,
    XPATH_MENSAGEM_SEM_DEBITOS,
)
from pref_scraper.debitos import ha_debito_vencido
from pref_scraper.utils.waits import baixar_arquivo, esperar_elemento_visivel


class SituacaoDebitos(Enum):
    COM_DEBITOS = "com_debitos"
    SEM_DEBITOS = "sem_debitos"


class EstadoDesconhecidoError(RuntimeError):
    """A tela de débitos não é nem a tabela de débitos nem a mensagem de 'sem débitos'."""


class DebitosEmAbertoPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def _estado(self, driver):
        tem_tabela = bool(driver.find_elements(By.XPATH, XPATH_LINHAS_DEBITOS))
        tem_mensagem = bool(driver.find_elements(By.XPATH, XPATH_MENSAGEM_SEM_DEBITOS))
        if tem_tabela and not tem_mensagem:
            return SituacaoDebitos.COM_DEBITOS
        if tem_mensagem and not tem_tabela:
            return SituacaoDebitos.SEM_DEBITOS
        return False  # nada reconhecido (ou ambíguo): continua esperando

    def situacao(self) -> SituacaoDebitos:
        """COM_DEBITOS, SEM_DEBITOS ou erro. Estado desconhecido nunca vira 'sem débitos'."""
        try:
            return WebDriverWait(self.driver, self.timeout).until(self._estado)
        except TimeoutException as e:
            raise EstadoDesconhecidoError(
                "Não foi possível identificar a situação de débitos na tela do portal "
                "(nem a tabela de débitos nem a mensagem de 'sem débitos' foram reconhecidas). "
                "O portal pode ter sido alterado."
            ) from e

    def vencimentos(self) -> list[str]:
        if self.situacao() is SituacaoDebitos.SEM_DEBITOS:
            return []
        cabecalho = self.driver.find_element(By.XPATH, XPATH_CABECALHO_VENCIMENTO)
        coluna = len(cabecalho.find_elements(By.XPATH, "preceding-sibling::th")) + 1
        celulas = self.driver.find_elements(By.XPATH, f"{XPATH_LINHAS_DEBITOS}/td[{coluna}]")
        return [c.text.strip() for c in celulas]

    def existe_debito_vencido(self, hoje: date | None = None) -> bool:
        return ha_debito_vencido(self.vencimentos(), hoje or date.today())

    def gerar_arquivo_pdf_debitos_em_aberto(self):
        if self.situacao() is SituacaoDebitos.SEM_DEBITOS:
            return None
        botao = esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_TODOS_DEBITOS)
        nome = nome_documento(self.driver.dados_imovel, "debitos")
        return baixar_arquivo(botao.click, self.driver.pasta_download, nome)
