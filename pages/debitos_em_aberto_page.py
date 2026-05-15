from config.selectors import ID_TABELA_DEBITOS_EM_ABERTO, ID_COLUNA_VENCIMENTO_TABELA_DEBITOS_EM_ABERTO, \
    XPATH_MENSAGEM_ENTRADA_TELA_DEBITOS, ID_ITEMS_TABELA_DE_DEBITOS, ID_COLUNA_VALOR_TOTAL_TABELA_DEBITOS_EM_ABERTO, \
    ID_BOTAO_IMPRIMIR_TODOS_DEBITOS
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
from utils.waits import esperar_elemento_visivel, esperar_download_completo
import datetime

class DebitosEmAbertoPage:
    def __init__(self, driver):
        self.driver = driver

    def _verificar_se_existe_tabela(self):
        esperar_elemento_visivel(self.driver, By.XPATH, XPATH_MENSAGEM_ENTRADA_TELA_DEBITOS)
        if ID_TABELA_DEBITOS_EM_ABERTO in self.driver.page_source:
            return True
        return False

    def _verifica_vencimento_atrasado(self):
        esperar_elemento_visivel(self.driver, By.ID, ID_TABELA_DEBITOS_EM_ABERTO)
        data_primeiro_vencimento_value = self.driver.find_element(locate_with(By.TAG_NAME, "td").below(self.driver.find_element(By.ID, ID_COLUNA_VENCIMENTO_TABELA_DEBITOS_EM_ABERTO))).text

        data_array_mode = data_primeiro_vencimento_value.split("/")

        data_formated = datetime.date(int(data_array_mode[2]), int(data_array_mode[1]), int(data_array_mode[0]))

        data_atual = datetime.date.today()
        if data_formated < data_atual:
            return True
        return False

    def _existe_debitos_em_aberto(self):
        if self._verificar_se_existe_tabela() and self._verifica_vencimento_atrasado():
            return True
        return False

    def obter_primeiros_debitos(self):
        if not self._existe_debitos_em_aberto():
            return []

        header_vencimento = self.driver.find_element(By.ID, ID_COLUNA_VENCIMENTO_TABELA_DEBITOS_EM_ABERTO)
        header_valor_total = self.driver.find_element(By.ID, ID_COLUNA_VALOR_TOTAL_TABELA_DEBITOS_EM_ABERTO)

        indice_coluna_valor_total = len(header_valor_total.find_elements(By.XPATH, "preceding-sibling::th"))
        indice_coluna_vencimento = len(header_vencimento.find_elements(By.XPATH, "preceding-sibling::th"))

        linhas = self.driver.find_element(By.ID, ID_ITEMS_TABELA_DE_DEBITOS).find_elements(By.TAG_NAME, "tr")

        informacoes = {}

        for linha in linhas:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) <= indice_coluna_valor_total:
                continue
            valor = celulas[indice_coluna_valor_total].text
            texto = celulas[indice_coluna_vencimento].text.strip()
            if texto and valor:
                informacoes.update({texto : valor})

        self._mostrar_debitos_de_iptu_mais_antigos(informacoes)

    def _mostrar_debitos_de_iptu_mais_antigos(self, dicionario_informacoes):
        print(f"{"Vencimento":<15} {"Valor Total":<10}")
        print("-"*25)
        for data, valor in dicionario_informacoes.items():
            print(
                f"{data:<15}"
                f"{valor:<10}"
            )

    def gerar_arquivo_pdf_debitos_em_aberto(self):
        if not self._existe_debitos_em_aberto():
            return "não existem débitos para serem impressos!"

        imovel = self.driver.dados_imovel
        nome_arquivo = f"{imovel['bairro']}_{imovel['quadra']}_{imovel['lote']} - debitos.pdf"

        esperar_elemento_visivel(self.driver, By.ID, ID_BOTAO_IMPRIMIR_TODOS_DEBITOS).click()

        return esperar_download_completo(self.driver.pasta_download, nome_arquivo=nome_arquivo)
