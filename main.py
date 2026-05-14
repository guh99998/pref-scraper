import time
from browser import Browser
from pages.home_page import HomePage

driver = Browser.criar_driver_segundo_plano()

inscricao_com_debito_vencido = "0001030890194001"
inscricao_sem_debito_vencido = "0001030830062001"
inscricao_sem_debito = "0001030830032001"
inscricao_com_debito_vencido_muitas_paginas = "0001030920287001"

caminho_salvar_arquivo = "C:\\Users\\gusta\\Downloads\\pref-scraper\\files"

home_page = HomePage(driver)
home_page.acessar_pagina_inicial_imovel()
home_page.preencher_campo_inscricao(inscricao_com_debito_vencido)

inscricao_imovel = home_page.clicar_botao_validar()

debitos_imovel = inscricao_imovel.acessar_debitos_em_aberto()

debitos_imovel.gerar_arquivo_pdf_debitos_em_aberto(caminho_salvar_arquivo)