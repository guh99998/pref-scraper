from pref_scraper.arquivos import caminho_livre, nome_documento
from pref_scraper.models import DadosImovel


def _dados(**kw):
    base = dict(
        bairro="CENTRO", quadra="3", lote="8", logradouro="RUA X", numero="10",
        complemento="", nome_proprietario="FULANO", doc_proprietario="000.000.000-00",
    )
    base.update(kw)
    return DadosImovel(**base)


def test_nome_documento_formato_basico():
    assert nome_documento(_dados(), "extrato") == "CENTRO_3_8 - extrato.pdf"


def test_nome_documento_remove_caracteres_invalidos_no_windows():
    nome = nome_documento(_dados(bairro='JD: "SOL"/NORTE?'), "extrato")
    assert not any(c in nome for c in '<>:"/\|?*')
    assert nome.endswith(" - extrato.pdf")


def test_nome_documento_nao_termina_com_ponto_ou_espaco_antes_da_extensao():
    nome = nome_documento(_dados(bairro="CENTRO. "), "extrato")
    assert nome.startswith("CENTRO_3_8")


def test_caminho_livre_retorna_o_proprio_se_nao_existe(tmp_path):
    assert caminho_livre(tmp_path, "a.pdf") == tmp_path / "a.pdf"


def test_caminho_livre_nunca_sobrescreve(tmp_path):
    (tmp_path / "a.pdf").write_text("1")
    assert caminho_livre(tmp_path, "a.pdf") == tmp_path / "a (2).pdf"
    (tmp_path / "a (2).pdf").write_text("2")
    assert caminho_livre(tmp_path, "a.pdf") == tmp_path / "a (3).pdf"
