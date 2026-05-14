from config.selectors import XPATH_TABELA_DEBITOS_EM_ABERTO, XPATH_PRIMEIRO_VENCIMENTO_TABELA_DEBITOS_EM_ABERTO
import datetime

class DebitosEmAbertoPage:
    def __init__(self, driver):
        self.driver = driver

    def verificar_se_existe_tabela(self):
        if(XPATH_TABELA_DEBITOS_EM_ABERTO in self.driver.page_source):
            return True
        return False
    
    def verifica_vencimento_atrasado(self):
        data_primeiro_item = XPATH_PRIMEIRO_VENCIMENTO_TABELA_DEBITOS_EM_ABERTO.text
        data_formated = data_primeiro_item.split("/").datetime.date(int(data_formated[2]), int(data_formated[1]), int(data_formated[0]))
        data_atual = datetime.date.today()
        if(data_formated < data_atual):
            return True
        return False

    def existe_debitos_em_aberto(self):
        if(self.verificar_se_existe_tabela()):
            if (self.verifica_vencimento_atrasado()):
                return True
            return False
        return False
    
    