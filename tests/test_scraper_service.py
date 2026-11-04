import pytest
from selenium.common.exceptions import TimeoutException

from pref_scraper.scraper_service import ScraperService


class DriverFalso:
    def __init__(self):
        self.encerrado = False

    def quit(self):
        self.encerrado = True


class ServicoSemPortal(ScraperService):
    """Troca só a navegação de volta, para contar chamadas sem abrir o portal."""

    def __init__(self, driver, **kw):
        super().__init__("pasta", driver=driver, **kw)
        self.voltas = 0
        self._inscricao_page = object()

    def _voltar_para_inscricao(self):
        self.voltas += 1


def test_gerar_volta_para_a_inscricao_em_caso_de_sucesso():
    s = ServicoSemPortal(DriverFalso())
    assert s._gerar(lambda page: "pagina", lambda pagina: "arquivo.pdf") == "arquivo.pdf"
    assert s.voltas == 1


def test_gerar_volta_para_a_inscricao_mesmo_quando_falha():
    s = ServicoSemPortal(DriverFalso())

    def quebra(pagina):
        raise ValueError("falhou")

    with pytest.raises(ValueError, match="falhou"):
        s._gerar(lambda page: "pagina", quebra)
    assert s.voltas == 1


def test_gerar_volta_mesmo_quando_o_acesso_a_pagina_falha():
    s = ServicoSemPortal(DriverFalso())

    def acessar(page):
        raise TimeoutException("link não clicável")

    with pytest.raises(TimeoutException):
        s._gerar(acessar, lambda pagina: "x")
    assert s.voltas == 1


def test_gerar_sem_buscar_imovel_antes_e_erro_claro():
    s = ServicoSemPortal(DriverFalso())
    s._inscricao_page = None
    with pytest.raises(RuntimeError, match="Busque um imóvel"):
        s._gerar(lambda page: "p", lambda p: "x")
    assert s.voltas == 0


def test_carne_sem_parcelas_vira_erro_legivel():
    s = ServicoSemPortal(DriverFalso())

    class PaginaCarne:
        def gerar_carne_iptu(self):
            raise TimeoutException()

    s._inscricao_page = type("P", (), {"acessar_emitir_carne_de_iptu": lambda self: PaginaCarne()})()
    with pytest.raises(RuntimeError, match="Nenhum carnê"):
        s.gerar_pdf_carne_iptu()
    assert s.voltas == 1


def test_contexto_fecha_o_chrome_mesmo_com_erro():
    driver = DriverFalso()
    with pytest.raises(ValueError):
        with ServicoSemPortal(driver):
            raise ValueError("x")
    assert driver.encerrado


def test_visivel_mantem_a_janela_aberta_para_debug():
    driver = DriverFalso()
    with ServicoSemPortal(driver, headless=False):
        pass
    assert not driver.encerrado


def test_fechar_e_idempotente():
    driver = DriverFalso()
    s = ServicoSemPortal(driver)
    s.fechar()
    s.fechar()
    assert driver.encerrado


def test_gerar_reabre_a_inscricao_se_a_volta_anterior_falhou():
    s = ServicoSemPortal(DriverFalso())
    s._inscricao = "0001"
    s._inscricao_page = None
    reabertas = []

    def reabrir():
        reabertas.append(1)
        s._inscricao_page = object()

    s._abrir_inscricao = reabrir
    assert s._gerar(lambda page: "p", lambda p: "ok") == "ok"
    assert reabertas == [1]
