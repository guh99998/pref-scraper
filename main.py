from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.home_page import HomePage

inscricao_com_debito_vencido = "0001030890194001"
inscricao_sem_debito_vencido = "0001030830062001"
inscricao_sem_debito = "0001030830032001"

browser_options = Options()
browser_options.add_experimental_option("detach", True)
browser_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=browser_options)

home_page = HomePage(driver)
home_page.acessar_pagina_inicial_imovel()
home_page.preencher_campo_inscricao(inscricao_com_debito_vencido)

inscricao_imovel = home_page.clicar_botao_validar()

debitos_imovel = inscricao_imovel.acessar_debitos_em_aberto()

print(debitos_imovel.existe_debitos_em_aberto())