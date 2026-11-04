from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures" / "portal"


@pytest.fixture(scope="session")
def chrome():
    """Chrome headless compartilhado pelos testes marcados com `navegador`."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=opcoes)
    yield driver
    driver.quit()


@pytest.fixture
def abrir_fixture(chrome):
    def _abrir(nome):
        chrome.get((FIXTURES / nome).resolve().as_uri())
        return chrome

    return _abrir
