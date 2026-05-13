import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from prefeitura_scraper import PrefeituraScraper
from leitura_arquivos import LeituraArquivos

# Data
data_atual = datetime.date.today()

# Definindo URL de Busca
url = "https://nfe.sgpcloud.net:9175/servicosweb/home.jsf"

# Arquivo excel com muitas inscrições
file_xlsx = "./files/file.xlsx"

leitura_arquivo = LeituraArquivos(file_xlsx)
#leitura_arquivo.ler_arquivo_excel()

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
#chrome_options.add_experimental_option("detach", True)
#chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

prefeitura_scraper = PrefeituraScraper(url, driver, data_atual)

prefeitura_scraper.realizar_consulta_debitos_de_arquivo(leitura_arquivo.ler_arquivo_excel())

driver.quit()