import tempfile
import time
from pathlib import Path

import typer
from rich.text import Text

from pref_scraper import ui
from pref_scraper.documentos import Documento, selecionar
from pref_scraper.planilha import PlanilhaError, ler_inscricoes
from pref_scraper.relatorio import gravar_resultados_csv
from pref_scraper.scraper_service import DocumentoIndisponivel, ScraperService

app = typer.Typer(
    help="Scraper do portal imobiliário municipal de Monte Sião-MG (SGP Cloud).",
    pretty_exceptions_show_locals=False,  # CPF e nomes não podem aparecer em tracebacks
    no_args_is_help=True,
    add_completion=False,
)

estado = {"banner": True}

OPCAO_INSCRICAO = typer.Option(..., "--inscricao", "-i", help="Número de inscrição municipal")
OPCAO_VISIVEL = typer.Option(False, "--visivel", help="Abre o Chrome visível e o mantém aberto (debug)")


def criar_servico(pasta, visivel: bool) -> ScraperService:
    return ScraperService(pasta, headless=not visivel)


def _pasta_temporaria():
    # com --visivel o Chrome pode continuar segurando arquivos: não falhar ao limpar
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def _versao(mostrar: bool):
    if mostrar:
        typer.echo(f"pref-scraper {ui.versao()}")
        raise typer.Exit()


@app.callback()
def principal(
    versao: bool = typer.Option(False, "--version", callback=_versao, is_eager=True, help="Mostra a versão"),
    sem_banner: bool = typer.Option(False, "--sem-banner", help="Não exibe o banner"),
):
    estado["banner"] = not sem_banner


def _iniciar(comando: str, itens: list[tuple[str, str]]):
    if estado["banner"]:
        ui.exibir_banner()
    ui.cabecalho([("Comando", comando), *itens])


def _descrever(e: Exception) -> str:
    # Selenium traz "Message: ..." seguido de "Stacktrace: ..." e, às vezes, a mensagem vem vazia
    msg = getattr(e, "msg", None)
    texto = msg if isinstance(msg, str) else str(e)
    primeira = (texto.strip().splitlines() or [""])[0].strip().removeprefix("Message:").strip()
    if primeira == "None":
        primeira = ""
    return primeira or f"{type(e).__name__} (o portal não respondeu como esperado)"


def _uso_incorreto(mensagem: str):
    ui.aviso("!", mensagem)
    raise typer.Exit(2)


def _ler_planilha(arquivo: Path, coluna: str) -> list[str]:
    try:
        return ler_inscricoes(arquivo, coluna)
    except PlanilhaError as e:
        _uso_incorreto(str(e))


def _selecionar(todos: bool, flags: dict[str, bool]) -> list[Documento]:
    docs = selecionar(todos, [flag for flag, ativo in flags.items() if ativo])
    if not docs:
        _uso_incorreto("Nenhum documento selecionado. Use --todos ou escolha ao menos um.")
    return docs


def _flags(extrato, certidao_negativa, existencia, valor_venal, listagem_iptu, carne_iptu) -> dict[str, bool]:
    return {
        "extrato": extrato,
        "certidao-negativa": certidao_negativa,
        "existencia": existencia,
        "valor-venal": valor_venal,
        "listagem-iptu": listagem_iptu,
        "carne-iptu": carne_iptu,
    }


class Contagem:
    def __init__(self):
        self.inicio = time.monotonic()
        self.ok = self.falhas = self.ignoradas = 0

    def finalizar(self):
        ui.resumo(time.monotonic() - self.inicio, self.ok, self.falhas, self.ignoradas)
        if self.falhas:
            raise typer.Exit(1)


def _gerar_documentos(servico, inscricao: str, docs: list[Documento], contagem: Contagem):
    for doc in docs:
        try:
            caminho = servico.gerar(doc)
            ui.resultado("+", inscricao, doc.nome, Path(caminho).name)
            contagem.ok += 1
        except DocumentoIndisponivel as e:
            ui.resultado("-", inscricao, doc.nome, str(e))
            contagem.ignoradas += 1
        except Exception as e:
            ui.resultado("!", inscricao, doc.nome, _descrever(e))
            contagem.falhas += 1


def _endereco(dados) -> str:
    endereco = f"{dados.logradouro}, {dados.numero}" if dados.numero else dados.logradouro
    if dados.complemento:
        endereco += f" - {dados.complemento}"
    if dados.bairro:
        endereco += f" - {dados.bairro}"
    return endereco


@app.command("info")
def info(inscricao: str = OPCAO_INSCRICAO, visivel: bool = OPCAO_VISIVEL):
    """Consulta informações e situação de débitos de um imóvel."""
    _iniciar("info", [("Inscrição", inscricao)])
    contagem = Contagem()
    with _pasta_temporaria() as pasta, criar_servico(pasta, visivel) as servico:
        try:
            informacoes = servico.obter_informacoes(inscricao)
        except Exception as e:
            ui.resultado("!", inscricao, "", _descrever(e))
            contagem.falhas += 1
        else:
            itens = [
                ("Proprietário", informacoes.nome_proprietario),
                ("Quadra/Lote", f"{informacoes.quadra} / {informacoes.lote}"),
            ]
            dados = servico.dados
            if dados and dados.logradouro:
                itens.append(("Endereço", _endereco(dados)))
            itens.append(("Situação", ui.debito(informacoes.existe_debito)))
            ui.bloco("+", f"Imóvel {inscricao}", itens)
            contagem.ok += 1
    contagem.finalizar()


@app.command("documentos")
def documentos(
    inscricao: str = OPCAO_INSCRICAO,
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde os PDFs serão salvos"),
    todos: bool = typer.Option(False, "--todos", help="Gera todos os documentos"),
    extrato: bool = typer.Option(False, "--extrato", help="Extrato de pagamentos"),
    certidao_negativa: bool = typer.Option(False, "--certidao-negativa", help="Certidão negativa de débitos"),
    existencia: bool = typer.Option(False, "--existencia", help="Certidão de existência do imóvel"),
    valor_venal: bool = typer.Option(False, "--valor-venal", help="Certidão de valor venal"),
    listagem_iptu: bool = typer.Option(False, "--listagem-iptu", help="Listagem de IPTUs"),
    carne_iptu: bool = typer.Option(False, "--carne-iptu", help="Carnê do IPTU"),
    visivel: bool = OPCAO_VISIVEL,
):
    """Gera documentos PDF para um imóvel."""
    docs = _selecionar(
        todos, _flags(extrato, certidao_negativa, existencia, valor_venal, listagem_iptu, carne_iptu)
    )
    pasta.mkdir(parents=True, exist_ok=True)
    _iniciar(
        "documentos",
        [
            ("Inscrição", inscricao),
            ("Documentos", ", ".join(d.flag for d in docs)),
            ("Saída", str(pasta.resolve())),
        ],
    )
    contagem = Contagem()
    with criar_servico(pasta.resolve(), visivel) as servico:
        try:
            servico.buscar_imovel(inscricao)
        except Exception as e:
            ui.resultado("!", inscricao, "", _descrever(e))
            contagem.falhas += 1
        else:
            _gerar_documentos(servico, inscricao, docs, contagem)
    contagem.finalizar()


@app.command("lote")
def lote(
    arquivo: Path = typer.Option(..., "--arquivo", "-a", help="Planilha Excel (.xlsx) com as inscrições"),
    coluna: str = typer.Option(..., "--coluna", "-c", help="Nome da coluna com as inscrições"),
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde resultados.csv será salvo"),
    visivel: bool = OPCAO_VISIVEL,
):
    """Consulta várias inscrições de uma planilha e grava resultados.csv."""
    inscricoes = _ler_planilha(arquivo, coluna)
    pasta.mkdir(parents=True, exist_ok=True)
    _iniciar("lote", [("Inscrições", str(len(inscricoes))), ("Saída", str(pasta.resolve()))])
    contagem = Contagem()
    linhas = []
    with _pasta_temporaria() as tmp, criar_servico(tmp, visivel) as servico:
        for inscricao in inscricoes:
            with ui.erro.status(f"Consultando {inscricao}..."):
                try:
                    inf = servico.obter_informacoes(inscricao)
                except Exception as e:
                    mensagem = _descrever(e)
                    ui.resultado("!", inscricao, "", mensagem)
                    linhas.append({"inscricao": inscricao, "proprietario": "", "quadra": "", "lote": "",
                                   "existe_debito": "", "erro": mensagem})
                    contagem.falhas += 1
                    continue
            ui.resultado(
                "+", inscricao, inf.nome_proprietario,
                Text.assemble(f"Qd {inf.quadra} Lt {inf.lote}  ", ui.debito(inf.existe_debito)),
            )
            linhas.append({"inscricao": inscricao, "proprietario": inf.nome_proprietario,
                           "quadra": inf.quadra, "lote": inf.lote,
                           "existe_debito": "sim" if inf.existe_debito else "não", "erro": ""})
            contagem.ok += 1
    caminho = gravar_resultados_csv(pasta, linhas)
    ui.aviso("*", f"Resultados salvos em {caminho}")
    contagem.finalizar()


@app.command("lote-documentos")
def lote_documentos(
    arquivo: Path = typer.Option(..., "--arquivo", "-a", help="Planilha Excel (.xlsx) com as inscrições"),
    coluna: str = typer.Option(..., "--coluna", "-c", help="Nome da coluna com as inscrições"),
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde os PDFs serão salvos"),
    todos: bool = typer.Option(False, "--todos", help="Gera todos os documentos"),
    extrato: bool = typer.Option(False, "--extrato", help="Extrato de pagamentos"),
    certidao_negativa: bool = typer.Option(False, "--certidao-negativa", help="Certidão negativa de débitos"),
    existencia: bool = typer.Option(False, "--existencia", help="Certidão de existência do imóvel"),
    valor_venal: bool = typer.Option(False, "--valor-venal", help="Certidão de valor venal"),
    listagem_iptu: bool = typer.Option(False, "--listagem-iptu", help="Listagem de IPTUs"),
    carne_iptu: bool = typer.Option(False, "--carne-iptu", help="Carnê do IPTU"),
    visivel: bool = OPCAO_VISIVEL,
):
    """Gera documentos PDF para várias inscrições de uma planilha."""
    inscricoes = _ler_planilha(arquivo, coluna)
    docs = _selecionar(
        todos, _flags(extrato, certidao_negativa, existencia, valor_venal, listagem_iptu, carne_iptu)
    )
    pasta.mkdir(parents=True, exist_ok=True)
    _iniciar(
        "lote-documentos",
        [
            ("Inscrições", str(len(inscricoes))),
            ("Documentos", ", ".join(d.flag for d in docs)),
            ("Saída", str(pasta.resolve())),
        ],
    )
    contagem = Contagem()
    with criar_servico(pasta.resolve(), visivel) as servico:
        for inscricao in inscricoes:
            try:
                with ui.erro.status(f"Buscando {inscricao}..."):
                    servico.buscar_imovel(inscricao)
            except Exception as e:
                ui.resultado("!", inscricao, "", _descrever(e))
                contagem.falhas += 1
                continue
            _gerar_documentos(servico, inscricao, docs, contagem)
    contagem.finalizar()


if __name__ == "__main__":
    app()
