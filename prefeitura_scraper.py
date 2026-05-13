import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class PrefeituraScraper:
    def __init__(self, url, driver, data_atual):
        self.url = url
        self.driver = driver
        self.nome_proprietario = '';
        self.quadra_lote = '';
        self.numero_lote = '';
        self.lote_com_debitos = False
        self.data_atual = data_atual

    def acessar_pagina(self):
        '''
        Acessa a página da prefeitura que contém os dados de interesse.
        '''
        self.driver.get(self.url)

    def pagina_imvovel_inscricao(self, inscricao):
        '''
        Acessa a página inicial do imóvel correspondente à inscrição fornecida.
        '''
        self.driver.find_element(By.LINK_TEXT, "Imobiliário").click()
        WebDriverWait(self.driver, 0.5).until(
            EC.element_to_be_clickable((By.ID, "compInformarImovel:formNumero:itIdentText"))
        ).send_keys(inscricao)
        self.driver.find_element(By.ID, "compInformarImovel:formNumero:btnValidar").click()
        self.driver.implicitly_wait(3)

    def acessar_pagina_debitos(self):
        '''
        Acessa a página de débitos do imóvel e verifica se o IPTU está quitado ou se possuem débitos a vencer e vencidos
        '''
        WebDriverWait(self.driver, 1.5).until(
            EC.element_to_be_clickable((By.ID, "formImobiliario:repeat:1:clLinkImobiliario"))
        ).click()
        self.driver.implicitly_wait(3)
        
    def verificar_debitos_vencidos(self):
        '''
        Verifica se existem débitos vencidos para o imóvel.
        '''

        if(self.driver.find_element(By.ID, "formDebitos:formMessages").find_element(By.TAG_NAME, "div").get_attribute("class") == "ui-messages-info ui-corner-all"):
            self.lote_com_debitos = False
        else:   
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Débitos"))
            ).click()

            data_primeiro_vencimento_value = self.driver.find_element(locate_with(By.TAG_NAME, "td").below(self.driver.find_element(By.ID, "formDebitos:tabViewDebitos:dataTableDados:j_idt812"))).text

            data_array_mode = data_primeiro_vencimento_value.split("/")
    
            data_formated = datetime.date(int(data_array_mode[2]), int(data_array_mode[1]), int(data_array_mode[0]))

            if (data_formated < self.data_atual):
                self.lote_com_debitos = True
        self.driver.implicitly_wait(3)

    def obter_informacoes_gerais(self):
        '''
        Obtém informações gerais do imóvel, como nome do proprietário, quadra e lote.
        '''
        if(not self.driver.find_element(By.ID, "formDebitos:formMessages").find_element(By.TAG_NAME, "div").get_attribute("class") == "ui-messages-info ui-corner-all"):
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Dados gerais"))
            ).click()

        self.nome_proprietario = self.driver.find_element(By.ID, "formCabecalho:textProprietarioNome").text

        for i in self.driver.find_elements(By.TAG_NAME, "td"):
            if (i.text == "Quadra (lot.)"):
                quadra_lot_title = i
                self.quadra_lote = self.driver.find_element(locate_with(By.TAG_NAME, "td").below(quadra_lot_title)).text
                break;

        # Pegando o valor de "Lote (lot.)"
        for i in self.driver.find_elements(By.TAG_NAME, "td"):
            if (i.text == "Lote (lot.)"):
                lote_title = i
                self.numero_lote = self.driver.find_element(locate_with(By.TAG_NAME, "td").below(lote_title)).text
                break;
    
    def realizar_consulta_debitos_titularidade(self, inscricao):
        '''
        Realiza a função de consulta de débitos e titularidade do imóvel, verificando se o lote possui débitos vencidos ou a vencer.
        '''
        self.acessar_pagina()
        self.pagina_imvovel_inscricao(inscricao)
        self.acessar_pagina_debitos()
        self.verificar_debitos_vencidos()
        self.obter_informacoes_gerais()

        print(f"""
        --- RESULTADOS DA BUSCA ---
        Proprietário: {self.nome_proprietario}
        Quadra: {self.quadra_lote}
        Lote: {self.numero_lote}
        Situação do lote: {"Débitos em aberto" if self.lote_com_debitos else "Sem débitos em aberto"}
        """)