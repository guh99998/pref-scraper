import openpyxl
import pytest

from pref_scraper.planilha import PlanilhaError, ler_inscricoes


def _xlsx(tmp_path, cabecalho, linhas, nome="entrada.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(cabecalho)
    for linha in linhas:
        ws.append(linha)
    caminho = tmp_path / nome
    wb.save(caminho)
    return caminho


def test_preserva_zeros_a_esquerda(tmp_path):
    arq = _xlsx(tmp_path, ["Numero"], [["0000123456789012"], ["000200"]])
    assert ler_inscricoes(arq, "Numero") == ["0000123456789012", "000200"]


def test_celula_numerica_nao_vira_float(tmp_path):
    arq = _xlsx(tmp_path, ["Numero"], [[103], [104]])
    assert ler_inscricoes(arq, "Numero") == ["103", "104"]


def test_coluna_ignora_maiusculas_e_espacos(tmp_path):
    arq = _xlsx(tmp_path, [" NUMERO "], [["1"]])
    assert ler_inscricoes(arq, "numero") == ["1"]


def test_cabecalho_nao_textual_nao_quebra(tmp_path):
    arq = _xlsx(tmp_path, [2026, "Numero"], [["x", "7"]])
    assert ler_inscricoes(arq, "Numero") == ["7"]


def test_ignora_vazios_e_espacos_nas_pontas(tmp_path):
    arq = _xlsx(tmp_path, ["Numero"], [["  5 "], [None], ["   "], ["6"]])
    assert ler_inscricoes(arq, "Numero") == ["5", "6"]


def test_coluna_inexistente_lista_as_disponiveis(tmp_path):
    arq = _xlsx(tmp_path, ["Lote", "Numero"], [["a", "1"]])
    with pytest.raises(PlanilhaError) as erro:
        ler_inscricoes(arq, "Inscricao")
    assert "Inscricao" in str(erro.value)
    assert "Lote" in str(erro.value) and "Numero" in str(erro.value)


def test_arquivo_inexistente(tmp_path):
    with pytest.raises(PlanilhaError, match="não encontrado"):
        ler_inscricoes(tmp_path / "nao_existe.xlsx", "Numero")


def test_so_aceita_xlsx(tmp_path):
    arq = tmp_path / "antiga.xls"
    arq.write_bytes(b"x")
    with pytest.raises(PlanilhaError, match=r"\.xlsx"):
        ler_inscricoes(arq, "Numero")


def test_planilha_sem_inscricoes(tmp_path):
    arq = _xlsx(tmp_path, ["Numero"], [[None], ["  "]])
    with pytest.raises(PlanilhaError, match="Nenhuma inscrição"):
        ler_inscricoes(arq, "Numero")


def test_arquivo_corrompido(tmp_path):
    arq = tmp_path / "ruim.xlsx"
    arq.write_bytes(b"isso nao e um xlsx")
    with pytest.raises(PlanilhaError, match="ler"):
        ler_inscricoes(arq, "Numero")
