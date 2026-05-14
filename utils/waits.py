import glob
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def esperar_elemento_visivel(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def esperar_elemento_clicavel(driver, by, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )

def esperar_download_completo(pasta, extensao=".pdf", timeout=30):
    arquivos_antes = set(glob.glob(os.path.join(pasta, f"*{extensao}")))

    fim = time.time() + timeout
    while time.time() < fim:
        arquivos_agora = set(glob.glob(os.path.join(pasta, f"*{extensao}")))
        novos = arquivos_agora - arquivos_antes
        crdownloads = glob.glob(os.path.join(pasta, "*.crdownload"))

        if novos and not crdownloads:
            return list(novos)[0]

        time.sleep(0.5)

    raise TimeoutException(f"Download não concluído após {timeout}s")