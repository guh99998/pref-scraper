import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from prefeitura_scraper import PrefeituraScraper

# Data
data_atual = datetime.date.today()

# Definindo URL de Busca
url = "https://nfe.sgpcloud.net:9175/servicosweb/home.jsf"

# RESULTADO ESPERADO
# Proprietário: PORTUCALE EMPREENDIMENTOS IMOB
# Quadra: 00B
# Lote: 0001
# Situação do Lote: Débitos em aberto
inscricao_b01 = "0001030830032001"


# RESULTADO ESPERADO
# Proprietário: PORTUCALE EMPREENDIMENTOS IMOB
# Quadra: 00C
# Lote: 0006
# Situação do Lote: Sem débitos em aberto
inscricao_c06 = "0001030840150001"

# Configurando as Options do Selenium para que o navegador não feche sozinho e espera a página carregar
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=chrome_options)

prefeitura_scraper = PrefeituraScraper(url, driver, data_atual)

prefeitura_scraper.realizar_consulta_debitos_titularidade(inscricao_b01)
print("\n\n")
prefeitura_scraper.realizar_consulta_debitos_titularidade(inscricao_c06)

driver.quit()