import csv
from pathlib import Path

import openpyxl
import pytest
from typer.testing import CliRunner

from pref_scraper import cli, ui
from pref_scraper.models import DadosImovel, InformacoesImovel
from pref_scraper.scraper_service import DocumentoIndisponivel

runner = CliRunner()


class ServicoFalso:
    """Substitui o ScraperService: nada de Chrome."""

    def __init__(self, pasta, falhas=(), sem_debito=(), indisponiveis=()):
        self.pasta = Path(pasta)
        self.falhas = set(falhas)          # inscrições que dão erro
        self.sem_debito = set(sem_debito)
        self.indisponiveis = set(indisponiveis)  # flags de documento indisponíveis
        self.fechado = False
        self._atual = None
        self.dados = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.fechado = True

    def buscar_imovel(self, inscricao):
        self._atual = inscricao
        if inscricao in self.falhas:
            raise RuntimeError("inscrição não encontrada")
        self.dados = DadosImovel("CENTRO", "3", "8", "RUA A", "10", "", f"DONO {inscricao[-3:]}", "000")
        return self.dados

    def obter_informacoes(self, inscricao):
        dados = self.buscar_imovel(inscricao)
        return InformacoesImovel(dados.quadra, dados.lote, dados.nome_proprietario,
                                 existe_debito=inscricao not in self.sem_debito)

    def gerar(self, documento):
        if documento.flag in self.indisponiveis:
            raise DocumentoIndisponivel("sem parcelas em aberto")
        if documento.flag == "existencia":
            raise ValueError("[+] [red]quebrou[/red]")
        return self.pasta / f"CENTRO_3_8 - {documento.flag}.pdf"


@pytest.fixture
def servico(monkeypatch):
    criados = []

    def fabrica(pasta, visivel, **extra):
        s = ServicoFalso(pasta, **fixture_kwargs)
        criados.append(s)
        return s

    fixture_kwargs = {}
    monkeypatch.setattr(cli, "criar_servico", fabrica)
    fabrica.criados = criados
    fabrica.kwargs = fixture_kwargs
    return fabrica


def _planilha(tmp_path, valores, coluna="Numero"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append([coluna])
    for v in valores:
        ws.append([v])
    caminho = tmp_path / "in.xlsx"
    wb.save(caminho)
    return caminho


def test_version(servico):
    r = runner.invoke(cli.app, ["--version"])
    assert r.exit_code == 0
    assert ui.versao() in r.stdout


def test_banner_vai_para_stderr_e_nunca_para_stdout(servico):
    r = runner.invoke(cli.app, ["info", "-i", "0001"])
    assert "____" in r.stderr
    assert "____" not in r.stdout


def test_sem_banner(servico):
    r = runner.invoke(cli.app, ["--sem-banner", "info", "-i", "0001"])
    assert "____" not in r.stderr


def test_banner_de_uma_linha_em_terminal_estreito():
    assert "\n" not in ui.texto_banner(largura=60).strip("\n")
    assert "\n" in ui.texto_banner(largura=120).strip("\n")


def test_info_com_debito(servico):
    r = runner.invoke(cli.app, ["--sem-banner", "info", "-i", "0001000"])
    assert r.exit_code == 0
    assert "COM DÉBITOS" in r.stdout
    assert servico.criados[0].fechado


def test_info_sem_debito(servico):
    servico.kwargs["sem_debito"] = {"0001000"}
    r = runner.invoke(cli.app, ["--sem-banner", "info", "-i", "0001000"])
    assert r.exit_code == 0
    assert "SEM DÉBITOS" in r.stdout


def test_info_falha_sai_com_1_e_fecha_o_chrome(servico):
    servico.kwargs["falhas"] = {"0001000"}
    r = runner.invoke(cli.app, ["--sem-banner", "info", "-i", "0001000"])
    assert r.exit_code == 1
    assert "[!]" in r.stdout and "inscrição não encontrada" in r.stdout
    assert servico.criados[0].fechado


def test_documentos_sem_selecao_e_uso_incorreto(servico, tmp_path):
    r = runner.invoke(cli.app, ["--sem-banner", "documentos", "-i", "1", "-p", str(tmp_path)])
    assert r.exit_code == 2


def test_documentos_marcadores_e_exit_code(servico, tmp_path):
    servico.kwargs["indisponiveis"] = {"carne-iptu"}
    r = runner.invoke(cli.app, ["--sem-banner", "documentos", "-i", "0001", "-p", str(tmp_path), "--todos"])
    assert r.exit_code == 1  # "existencia" quebra no serviço falso
    assert "[+] 0001" in r.stdout and "extrato.pdf" in r.stdout
    assert "[-] 0001" in r.stdout and "sem parcelas em aberto" in r.stdout
    assert "[!] 0001" in r.stdout
    # texto vindo de exceção aparece literalmente, sem o Rich interpretar como markup
    assert "[+] [red]quebrou[/red]" in r.stdout
    assert "1 falha" in r.stderr and "1 ignorada" in r.stderr and "4 ok" in r.stderr


def test_documentos_so_ignorada_nao_e_falha(servico, tmp_path):
    servico.kwargs["indisponiveis"] = {"carne-iptu"}
    r = runner.invoke(cli.app, ["--sem-banner", "documentos", "-i", "1", "-p", str(tmp_path), "--carne-iptu"])
    assert r.exit_code == 0


def test_lote_continua_apos_falha_e_grava_csv(servico, tmp_path):
    servico.kwargs["falhas"] = {"0002"}
    arq = _planilha(tmp_path, ["0001", "0002", "0003"])
    pasta = tmp_path / "saida"
    r = runner.invoke(cli.app, ["--sem-banner", "lote", "-a", str(arq), "-c", "numero", "-p", str(pasta)])
    assert r.exit_code == 1
    assert r.stdout.count("[+]") == 2 and r.stdout.count("[!]") == 1
    bruto = (pasta / "resultados.csv").read_bytes()
    assert bruto.startswith(b"\xef\xbb\xbf")  # utf-8-sig, abre certo no Excel
    texto = (pasta / "resultados.csv").read_text(encoding="utf-8-sig")
    linhas = list(csv.DictReader(texto.splitlines(), delimiter=";"))
    assert [x["inscricao"] for x in linhas] == ["0001", "0002", "0003"]
    assert linhas[1]["erro"] == "inscrição não encontrada"
    assert servico.criados[0].fechado


def test_lote_preserva_zeros_da_planilha(servico, tmp_path):
    arq = _planilha(tmp_path, ["000100"])
    r = runner.invoke(cli.app, ["--sem-banner", "lote", "-a", str(arq), "-c", "Numero", "-p", str(tmp_path)])
    assert "000100" in r.stdout


def test_lote_coluna_inexistente_e_uso_incorreto(servico, tmp_path):
    arq = _planilha(tmp_path, ["1"])
    r = runner.invoke(cli.app, ["--sem-banner", "lote", "-a", str(arq), "-c", "Nada", "-p", str(tmp_path)])
    assert r.exit_code == 2
    assert "Coluna 'Nada' não encontrada" in r.stderr


def test_lote_documentos_continua_apos_falha(servico, tmp_path):
    servico.kwargs["falhas"] = {"0001"}
    arq = _planilha(tmp_path, ["0001", "0002"])
    r = runner.invoke(cli.app, ["--sem-banner", "lote-documentos", "-a", str(arq), "-c", "Numero",
                                "-p", str(tmp_path / "pdfs"), "--extrato"])
    assert r.exit_code == 1
    assert "[!] 0001" in r.stdout
    assert "[+] 0002" in r.stdout


def test_stdout_limpo_para_pipe(servico, tmp_path):
    arq = _planilha(tmp_path, ["0001"])
    r = runner.invoke(cli.app, ["lote", "-a", str(arq), "-c", "Numero", "-p", str(tmp_path)])
    assert "____" not in r.stdout and "Concluído" not in r.stdout
    assert "Concluído" in r.stderr


def test_erro_do_selenium_sem_mensagem_fica_legivel(servico):
    from selenium.common.exceptions import TimeoutException

    class Quebrado(ServicoFalso):
        def obter_informacoes(self, inscricao):
            raise TimeoutException()  # str() vira "Message: \nStacktrace: ..."

    servico.kwargs.clear()
    cli.criar_servico = lambda pasta, visivel: Quebrado(pasta)
    r = runner.invoke(cli.app, ["--sem-banner", "info", "-i", "0001"])
    assert r.exit_code == 1
    assert "[!] 0001" in r.stdout
    assert "TimeoutException" in r.stdout
    assert "Stacktrace" not in r.stdout and "Message:" not in r.stdout


def test_cabecalho_nao_quebra_caminho_longo(servico, tmp_path):
    longa = tmp_path / ("pasta_com_nome_bem_comprido_" * 4)
    r = runner.invoke(cli.app, ["--sem-banner", "documentos", "-i", "1", "-p", str(longa), "--extrato"])
    assert any(str(longa.resolve()) in linha for linha in r.stderr.splitlines())
