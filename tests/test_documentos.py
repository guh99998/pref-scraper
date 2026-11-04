import pytest

from pref_scraper.documentos import DOCUMENTOS, selecionar


def test_seis_documentos_com_flags_unicas():
    assert len(DOCUMENTOS) == 6
    assert len({d.flag for d in DOCUMENTOS}) == 6
    assert len({d.metodo for d in DOCUMENTOS}) == 6


def test_todos_retorna_todos_na_ordem_do_registro():
    assert selecionar(todos=True, escolhidos=[]) == list(DOCUMENTOS)


def test_escolhidos_mantem_ordem_do_registro():
    r = selecionar(todos=False, escolhidos=["carne-iptu", "extrato"])
    assert [d.flag for d in r] == ["extrato", "carne-iptu"]


def test_nenhum_selecionado_retorna_vazio():
    assert selecionar(todos=False, escolhidos=[]) == []


def test_flag_desconhecida_e_erro():
    with pytest.raises(ValueError, match="invalido"):
        selecionar(todos=False, escolhidos=["invalido"])
