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

def esperar_download_completo(pasta, extensao=".pdf", timeout=30, nome_arquivo=None):
    # Registra nome E tempo de modificação dos arquivos existentes
    arquivos_antes = {
        f: os.path.getmtime(f)
        for f in glob.glob(os.path.join(pasta, f"*{extensao}"))
    }

    fim = time.time() + timeout
    while time.time() < fim:
        arquivos_agora = set(glob.glob(os.path.join(pasta, f"*{extensao}")))
        crdownloads = glob.glob(os.path.join(pasta, "*.crdownload"))

        novos = arquivos_agora - set(arquivos_antes.keys())
        modificados = {
            f for f in arquivos_agora
            if f in arquivos_antes and os.path.getmtime(f) != arquivos_antes[f]
        }

        detectados = novos | modificados

        if detectados and not crdownloads:
            arquivo = list(detectados)[0]
            if nome_arquivo:
                ext = os.path.splitext(arquivo)[1]
                nome_final = nome_arquivo if os.path.splitext(nome_arquivo)[1] else nome_arquivo + ext
                novo_caminho = os.path.join(pasta, nome_final)
                os.rename(arquivo, novo_caminho)
                return novo_caminho
            return arquivo

        time.sleep(0.5)

    raise TimeoutException(f"Download não concluído após {timeout}s")
