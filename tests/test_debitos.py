from datetime import date

import pytest

from pref_scraper.debitos import DataInvalidaError, ha_debito_vencido

HOJE = date(2026, 11, 4)


def test_sem_datas_nao_ha_debito_vencido():
    assert ha_debito_vencido([], HOJE) is False


def test_so_datas_futuras():
    assert ha_debito_vencido(["10/11/2026", "10/12/2026"], HOJE) is False


def test_vence_hoje_nao_e_vencido():
    assert ha_debito_vencido(["04/11/2026"], HOJE) is False


def test_primeira_futura_mas_outra_vencida():
    # o código antigo só olhava a primeira linha
    assert ha_debito_vencido(["10/12/2026", "03/11/2026"], HOJE) is True


def test_aceita_espacos():
    assert ha_debito_vencido([" 01/01/2020 "], HOJE) is True


@pytest.mark.parametrize("ruim", ["", "2026-11-04", "31/02/2026", "abc", "10/11"])
def test_data_invalida_gera_erro_claro(ruim):
    with pytest.raises(DataInvalidaError) as erro:
        ha_debito_vencido(["10/12/2026", ruim], HOJE)
    assert repr(ruim) in str(erro.value)
