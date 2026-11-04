XPATH_CAMPO_INSCRICAO = "/html/body/div[13]/div[2]/form/table/tbody/tr[1]/td[2]/input"

XPATH_BOTAO_VALIDAR_INSCRICAO = "/html/body/div[13]/div[2]/form/span[4]/div/button[1]"

XPATH_ERRO_VALIDACAO_INSCRICAO = (
    "//div[@id='compInformarImovel:formNumero:mensagens']"
    "//span[contains(@class, 'ui-messages-error-detail')]"
)

ID_BOTAO_VALIDAR_DADOS = "compInformarImovel:formNumero:btnValidar"

XPATH_PAGINA_INFORMACOES_COMPLETAS = "//a[starts-with(@id, 'formImobiliario:repeat:0:')]"

ID_FORMULARIO_PAGINA_INFORMACOES_COMPLETAS = "compInformarImovel:formNumero:itCnpjCpf2"

XPATH_PAGINA_DEBITOS = "//a[starts-with(@id, 'formImobiliario:repeat:1:')]"

XPATH_PAGINA_CERTIDAO_NEGATIVA_DEBITOS = "//a[starts-with(@id, 'formImobiliario:repeat:2:')]"

XPATH_PAGINA_CERTIDAO_EXISTENCIA_IMOVEL = "//a[starts-with(@id, 'formImobiliario:repeat:3:')]"

XPATH_PAGINA_CERTIDAO_VALOR_VENAL_IMOVEL = "//a[starts-with(@id, 'formImobiliario:repeat:4:')]"

XPATH_PAGINA_EMITIR_CARNE_IPTU = "//a[starts-with(@id, 'formImobiliario:repeat:5:')]"

XPATH_PAGINA_CONSULTAR_MOVIMENTACOES_EXTRATO = "//a[starts-with(@id, 'formImobiliario:repeat:6:')]"

# Tela de débitos: marcadores semânticos (não dependem dos IDs j_idtNNN, que mudam a cada implantação)
XPATH_MENSAGEM_SEM_DEBITOS = (
    "//div[@id='formDebitos:formMessages']"
    "//span[contains(@class, 'ui-messages-info-detail')][contains(., 'não possui débitos')]"
)

XPATH_LINHAS_DEBITOS = "//tbody[@id='formDebitos:tabViewDebitos:dataTableDados_data']/tr[@data-ri]"

XPATH_CABECALHO_VENCIMENTO = (
    "//thead[@id='formDebitos:tabViewDebitos:dataTableDados_head']"
    "//th[.//span[@class='ui-column-title'][normalize-space()='Venc']]"
)

XPATH_BOTAO_IMPRIMIR_TODOS_DEBITOS = "//form[@id='formDebitos']//button[.//span[normalize-space()='Imprimir Todos']]"

XPATH_BOTAO_IMPRIMIR_FICHA_CADASTRAL = "//form[@id='formInformacoesCompletas']//button[.//span[normalize-space()='Ficha Cadastral']]"

ID_CAMPO_CABECALHO_PROPRIETARIO = "formCabecalho:textProprietarioNome"

ID_CAMPO_CABECALHO_CPF_CNPJ = "formCabecalho:textProprietarioCpf"

LINK_TEXT_IMOBILIARIO = "Imobiliário"

LINK_TEXT_DEBITOS = "Débitos"

LINK_TEXT_DADOS_GERAIS = "Dados gerais"

XPATH_DIV_VOLTAR_INICIO = (
    "//div[contains(@class, 'ui-breadcrumb')]//a[contains(@href, 'formImobiliario.jsf')]"
)

XPATH_BOTAO_CERTIDAO_NEGATIVA_DEBITOS = "//form[@id='formCertidaoNegativaDebitos']//button[.//span[normalize-space()='Imprimir Certidão']]"

XPATH_BOTAO_CERTIDAO_EXISTENCIA = "//form[@id='formCertidaoExistencia']//button[.//span[normalize-space()='Imprimir Certidão']]"

XPATH_BOTAO_CERTIDAO_VALOR_VENAL = "//form[@id='formCertidaoValorVenal']//button[.//span[normalize-space()='Imprimir Certidão']]"

XPATH_BOTAO_CARNE_IPTU = "//form[@id='formCarne']//button[.//span[normalize-space()='Imprimir Carnê']]"

XPATH_BOTAO_LISTAGEM_IPTU = "//form[@id='formCarne']//button[.//span[normalize-space()='Imprimir Listagem']]"

XPATH_BOTAO_MOVIMENTACOES_EXTRATO = "//form[@id='formExtrato']//button[.//span[normalize-space()='Imprimir']]"