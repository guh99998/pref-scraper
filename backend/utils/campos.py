from selenium.webdriver.common.by import By

from utils.waits import esperar_elemento_visivel


def valor_do_campo(driver, rotulo, ocorrencia=1):
    """Lê o valor de um campo da tela de dados pelo texto do rótulo.

    O portal mostra os dados em tabelas onde uma linha traz os rótulos e a linha
    seguinte traz os valores, na mesma coluna. Localizar pelo rótulo não quebra
    quando o portal reorganiza os blocos da página (como acontece com XPath absoluto).
    """
    celula_rotulo = esperar_elemento_visivel(
        driver, By.XPATH, f"(//td[label[normalize-space()='{rotulo}']])[{ocorrencia}]"
    )
    coluna = len(celula_rotulo.find_elements(By.XPATH, "preceding-sibling::td")) + 1
    celula_valor = celula_rotulo.find_element(
        By.XPATH, f"../following-sibling::tr[1]/td[{coluna}]"
    )
    return celula_valor.text.strip()
