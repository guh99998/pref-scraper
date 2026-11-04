import threading
import time

import pytest
from selenium.common.exceptions import TimeoutException

from pref_scraper.utils.waits import baixar_arquivo


def test_download_instantaneo_e_detectado(tmp_path):
    # o snapshot precisa ser tirado ANTES da ação; um download rápido não pode passar despercebido
    def acao():
        (tmp_path / "baixado.pdf").write_bytes(b"%PDF")

    resultado = baixar_arquivo(acao, tmp_path, "CENTRO_3_8 - extrato.pdf", timeout=2)
    assert resultado == tmp_path / "CENTRO_3_8 - extrato.pdf"
    assert resultado.read_bytes() == b"%PDF"
    assert not (tmp_path / "baixado.pdf").exists()


def test_espera_o_crdownload_terminar(tmp_path):
    def acao():
        parcial = tmp_path / "x.pdf.crdownload"
        parcial.write_bytes(b"...")

        def terminar():
            time.sleep(0.4)
            (tmp_path / "x.pdf").write_bytes(b"completo")
            parcial.unlink()

        threading.Thread(target=terminar).start()

    resultado = baixar_arquivo(acao, tmp_path, "final.pdf", timeout=3, intervalo=0.05)
    assert resultado.read_bytes() == b"completo"


def test_ignora_pdfs_que_ja_existiam(tmp_path):
    (tmp_path / "antigo.pdf").write_bytes(b"antigo")

    def acao():
        (tmp_path / "novo.pdf").write_bytes(b"novo")

    resultado = baixar_arquivo(acao, tmp_path, "final.pdf", timeout=2)
    assert resultado.read_bytes() == b"novo"
    assert (tmp_path / "antigo.pdf").read_bytes() == b"antigo"


def test_nunca_sobrescreve_arquivo_existente_com_o_mesmo_nome(tmp_path):
    (tmp_path / "final.pdf").write_bytes(b"primeiro")

    def acao():
        (tmp_path / "novo.pdf").write_bytes(b"segundo")

    resultado = baixar_arquivo(acao, tmp_path, "final.pdf", timeout=2)
    assert resultado == tmp_path / "final (2).pdf"
    assert (tmp_path / "final.pdf").read_bytes() == b"primeiro"
    assert resultado.read_bytes() == b"segundo"


def test_timeout_quando_nada_e_baixado(tmp_path):
    with pytest.raises(TimeoutException):
        baixar_arquivo(lambda: None, tmp_path, "final.pdf", timeout=0.3, intervalo=0.05)


def test_crdownload_alheio_nao_bloqueia_um_pdf_ja_concluido(tmp_path):
    # o portal/Chrome deixa um 'downloads.htm.crdownload' recorrente na pasta; ele nada tem a ver com o PDF
    (tmp_path / "downloads.htm.crdownload").write_bytes(b"...")

    def acao():
        (tmp_path / "report.pdf").write_bytes(b"%PDF")

    resultado = baixar_arquivo(acao, tmp_path, "final.pdf", timeout=1, intervalo=0.05)
    assert resultado.read_bytes() == b"%PDF"


def test_nao_pega_pdf_ainda_em_download(tmp_path):
    def acao():
        (tmp_path / "report.pdf.crdownload").write_bytes(b"parcial")

    with pytest.raises(TimeoutException):
        baixar_arquivo(acao, tmp_path, "final.pdf", timeout=0.3, intervalo=0.05)
