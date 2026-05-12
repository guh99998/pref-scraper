
import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Definindo URL de Busca
url = "https://nfe.sgpcloud.net:9175/servicosweb/home.jsf"

# Número que será colocado para teste Lote B01 - open debits
inscricao_b01 = "0001030830032001"
debitos_cor_classe = "ui-messages-warn ui-corner-all"

# Inscrição C06 - no debits
inscricao_c06 = "0001030840150001"
sem_debitos_cor_classe = "ui-messages-info ui-corner-all"

situacao_lote = "Em dia";
data_atual = datetime.datetime.now()

# Configurando as Options do Selenium para que o navegador não feche sozinho e espera a página carregar
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=chrome_options)

# Abrindo um navegador com a URL definida incialmente
driver.get(url)

# Clicando no link "Imobiliário" do site
input_imobiliario = driver.find_element(By.LINK_TEXT, "Imobiliário")
input_imobiliario.click()

# Colocando coisas no formulário
wait = WebDriverWait(driver, 3)
input_text = wait.until(
    EC.element_to_be_clickable((By.ID, "compInformarImovel:formNumero:itIdentText"))
)
input_text.clear()
input_text.send_keys(inscricao_c06)

# Clicando no botão de Ok
botao_confirmar_inscricao = driver.find_element(By.ID, "compInformarImovel:formNumero:btnValidar")
botao_confirmar_inscricao.click()

# Entrando na página de Débitos para obter o lote
botao_debitos_em_aberto = wait.until(
    EC.element_to_be_clickable((By.ID, "formImobiliario:repeat:1:clLinkImobiliario"))
)
botao_debitos_em_aberto.click()

# Entrando na página de Dados gerais
# Primeiro tem que ver se essa aba é mostrada, se não for, é porque está tudo certo
driver.implicitly_wait(10)

obter_cor_texto = driver.find_element(By.ID, "formDebitos:formMessages").find_element(By.TAG_NAME, "div").get_attribute("class")

if (obter_cor_texto == sem_debitos_cor_classe):
    # Obtendo os primeiros dados do site (nome do proprietario)
    proprietario_incricao = driver.find_element(By.ID, "formCabecalho:textProprietarioNome").text

    # Pegando o valor de "Quadra (lot.)" — busca o td que segue o td com esse label
    quadra_lot_title = ''
    lote_title = '';

    busca_td_table = driver.find_elements(By.TAG_NAME, "td")

    for i in busca_td_table:
        if (i.text == "Quadra (lot.)"):
            quadra_lot_title = i
            quadra_lot_value = driver.find_element(locate_with(By.TAG_NAME, "td").below(quadra_lot_title)).text
            break;

    # Pegando o valor de "Lote (lot.)"
    for i in busca_td_table:
        if (i.text == "Lote (lot.)"):
            lote_title = i
            lote_value = driver.find_element(locate_with(By.TAG_NAME, "td").below(lote_title)).text
            break;

else:
    pagina_dados_gerais = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Dados gerais"))
    )
    pagina_dados_gerais.click()

    # Obtendo os primeiros dados do site (nome do proprietario)
    proprietario_incricao = driver.find_element(By.ID, "formCabecalho:textProprietarioNome").text

    # Pegando o valor de "Quadra (lot.)" — busca o td que segue o td com esse label
    quadra_lot_title = ''
    lote_title = '';

    busca_td_table = driver.find_elements(By.TAG_NAME, "td")

    for i in busca_td_table:
        if (i.text == "Quadra (lot.)"):
            quadra_lot_title = i
            quadra_lot_value = driver.find_element(locate_with(By.TAG_NAME, "td").below(quadra_lot_title)).text
            break;

    # Pegando o valor de "Lote (lot.)"
    for i in busca_td_table:
        if (i.text == "Lote (lot.)"):
            lote_title = i
            lote_value = driver.find_element(locate_with(By.TAG_NAME, "td").below(lote_title)).text
            break;

    # Iniciando para ver se o cliente tem ou não tem débito em aberto

    # Clicando na aba de Débitos
    botao_debitos = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Débitos"))
    )
    botao_debitos.click()

    # Obtendo a primeira data lista
    coluna_venc_debitos = driver.find_element(By.ID, "formDebitos:tabViewDebitos:dataTableDados:j_idt812")
    data_primeiro_vencimento_value = driver.find_element(locate_with(By.TAG_NAME, "td").below(coluna_venc_debitos)).text

    # Formatando data para formato datetime
    data_array_mode = data_primeiro_vencimento_value.split("/")
    
    data_formated = datetime.datetime(int(data_array_mode[2]), int(data_array_mode[1]), int(data_array_mode[0]))


    if data_formated < data_atual:
        situacao_lote = "débitos em aberto"
        print(situacao_lote)
    else:
        print(situacao_lote)


print(f"""
    Proprietário: {proprietario_incricao}
    Quadra: {quadra_lot_value}
    Lote: {lote_value}
    Situação: {situacao_lote}
""")