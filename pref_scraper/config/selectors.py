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

ID_BOTAO_IMPRIMIR_TODOS_DEBITOS = "formDebitos:tabViewDebitos:j_idt868"

ID_BOTAO_IMPRIMIR_FICHA_CADASTRAL = "formInformacoesCompletas:j_idt649"

ID_CAMPO_CABECALHO_PROPRIETARIO = "formCabecalho:textProprietarioNome"

ID_CAMPO_CABECALHO_CPF_CNPJ = "formCabecalho:textProprietarioCpf"

LINK_TEXT_IMOBILIARIO = "Imobiliário"

LINK_TEXT_DEBITOS = "Débitos"

LINK_TEXT_DADOS_GERAIS = "Dados gerais"

XPATH_DIV_VOLTAR_INICIO = (
    "//div[contains(@class, 'ui-breadcrumb')]//a[contains(@href, 'formImobiliario.jsf')]"
)

ID_BOTAO_CERTIDAO_NEGATIVA_DEBITOS = "formCertidaoNegativaDebitos:tabView:j_idt557:j_idt604"

ID_BOTAO_CERTIDAO_EXISTENCIA = "formCertidaoExistencia:tabView:compCertidao:j_idt602"

ID_BOTAO_CERTIDAO_VALOR_VENAL = "formCertidaoValorVenal:tabView:j_idt588:j_idt635"

ID_BOTAO_CARNE_IPTU = "formCarne:tabIptu:dataTableDados:0:j_idt609:j_idt611"

ID_BOTAO_LISTAGEM_IPTU = "formCarne:tabIptu:j_idt641"

ID_BOTAO_MOVIMENTACOES_EXTRATO = "formExtrato:j_idt362:j_idt617"