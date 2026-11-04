from datetime import date

import pytest

from pref_scraper.pages.debitos_em_aberto_page import (
    DebitosEmAbertoPage,
    EstadoDesconhecidoError,
    SituacaoDebitos,
)

pytestmark = pytest.mark.navegador


def test_tabela_com_debitos(abrir_fixture):
    page = DebitosEmAbertoPage(abrir_fixture("debitos_com_debito.html"), timeout=2)
    assert page.situacao() is SituacaoDebitos.COM_DEBITOS
    assert page.vencimentos() == ["10/11/2026", "10/12/2026"]


def test_mensagem_de_sem_debitos(abrir_fixture):
    page = DebitosEmAbertoPage(abrir_fixture("debitos_sem_debito.html"), timeout=2)
    assert page.situacao() is SituacaoDebitos.SEM_DEBITOS
    assert page.vencimentos() == []


def test_tela_irreconhecivel_e_erro_nunca_sem_debitos(chrome, tmp_path):
    # portal reimplantado com outra estrutura: não pode virar "sem débitos" em silêncio
    arquivo = tmp_path / "outra_tela.html"
    arquivo.write_text("<html><body><p>Manutenção</p></body></html>", encoding="utf-8")
    chrome.get(arquivo.as_uri())
    with pytest.raises(EstadoDesconhecidoError):
        DebitosEmAbertoPage(chrome, timeout=1).situacao()


def test_debito_vencido_com_data_de_referencia(abrir_fixture):
    page = DebitosEmAbertoPage(abrir_fixture("debitos_com_debito.html"), timeout=2)
    assert page.existe_debito_vencido(hoje=date(2026, 11, 15)) is True
    assert page.existe_debito_vencido(hoje=date(2026, 11, 1)) is False


def test_sem_debitos_nao_ha_vencido(abrir_fixture):
    page = DebitosEmAbertoPage(abrir_fixture("debitos_sem_debito.html"), timeout=2)
    assert page.existe_debito_vencido(hoje=date(2030, 1, 1)) is False
