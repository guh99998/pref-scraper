import time
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pref_scraper.arquivos import caminho_livre


def esperar_elemento_visivel(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def esperar_elemento_clicavel(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )

def baixar_arquivo(acao, pasta, nome, extensao=".pdf", timeout=30, intervalo=0.5):
    """Executa `acao` (o clique que dispara o download) e devolve o arquivo baixado, renomeado.

    O snapshot da pasta é tirado antes da ação, para que um download rápido seja detectado.
    O arquivo final nunca sobrescreve outro: em colisão, recebe o sufixo ' (2)'.
    """
    pasta = Path(pasta)
    antes = {f.name for f in pasta.glob(f"*{extensao}")}

    acao()

    fim = time.monotonic() + timeout
    while time.monotonic() < fim:
        novos = [f for f in pasta.glob(f"*{extensao}") if f.name not in antes]
        if novos and not list(pasta.glob("*.crdownload")):
            destino = caminho_livre(pasta, nome)
            novos[0].rename(destino)
            return destino
        time.sleep(intervalo)

    raise TimeoutException(f"Download não concluído após {timeout}s")
