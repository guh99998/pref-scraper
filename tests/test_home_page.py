import pytest

from pref_scraper.pages.home_page import InscricaoInvalidaError, aguardar_validacao

pytestmark = pytest.mark.navegador


def test_inscricao_rejeitada_mostra_a_mensagem_do_portal(abrir_fixture):
    driver = abrir_fixture("inscricao_invalida.html")
    with pytest.raises(InscricaoInvalidaError, match="cadastro não pode acessar o sistema"):
        aguardar_validacao(driver, timeout=2)


def test_inscricao_valida_segue_o_fluxo(abrir_fixture):
    aguardar_validacao(abrir_fixture("menu_imovel.html"), timeout=2)


def test_tela_irreconhecivel_e_erro_claro(chrome, tmp_path):
    arquivo = tmp_path / "x.html"
    arquivo.write_text("<html><body>manutenção</body></html>", encoding="utf-8")
    chrome.get(arquivo.as_uri())
    with pytest.raises(InscricaoInvalidaError, match="não respondeu"):
        aguardar_validacao(chrome, timeout=1)
