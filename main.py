import sys
import os
import tempfile
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich import box

app = typer.Typer(help="Scraper do portal imobiliário municipal (SGP Cloud)")
console = Console()


def _get_scraper(visivel: bool):
    from scraper_service import scraper
    scraper._headless = not visivel
    return scraper


@app.command("info")
def info(
    inscricao: str = typer.Option(..., "--inscricao", "-i", help="Número de inscrição municipal"),
    visivel: bool = typer.Option(False, "--visivel", help="Abre o Chrome visível (útil para debug)"),
):
    """Consulta informações e status de débito de um imóvel."""
    pasta_tmp = tempfile.mkdtemp()

    with console.status(f"[cyan]Consultando inscrição {inscricao}...[/cyan]"):
        from scraper_service import scraper
        try:
            resultado = scraper.obter_informacoes(inscricao, pasta_tmp, headless=not visivel)
        except Exception as e:
            console.print(f"[red]Erro:[/red] {e}")
            raise typer.Exit(1)

    dados = scraper._driver.dados_imovel if scraper._driver else {}
    debito_str = "[red]COM DÉBITOS[/red]" if resultado["existe_debito"] else "[green]SEM DÉBITOS[/green]"

    linhas = [
        f"[bold]Proprietário:[/bold] {resultado.get('nome_proprietario', '-')}",
        f"[bold]Quadra:[/bold] {resultado.get('quadra', '-')}  [bold]Lote:[/bold] {resultado.get('lote', '-')}",
    ]
    if dados.get("logradouro"):
        numero = dados.get("numero", "")
        complemento = dados.get("complemento", "")
        end = f"{dados['logradouro']}, {numero}" if numero else dados["logradouro"]
        if complemento:
            end += f" - {complemento}"
        if dados.get("bairro"):
            end += f" - {dados['bairro']}"
        linhas.append(f"[bold]Endereço:[/bold] {end}")
    linhas.append(f"[bold]Status:[/bold] {debito_str}")

    console.print(Panel("\n".join(linhas), title=f"Imóvel {inscricao}", expand=False))


@app.command("documentos")
def documentos(
    inscricao: str = typer.Option(..., "--inscricao", "-i", help="Número de inscrição municipal"),
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde os PDFs serão salvos"),
    todos: bool = typer.Option(False, "--todos", help="Gera todos os documentos disponíveis"),
    extrato: bool = typer.Option(False, "--extrato", help="Extrato de pagamentos"),
    certidao_negativa: bool = typer.Option(False, "--certidao-negativa", help="Certidão negativa de débitos"),
    existencia: bool = typer.Option(False, "--existencia", help="Certidão de existência do imóvel"),
    valor_venal: bool = typer.Option(False, "--valor-venal", help="Certidão de valor venal"),
    listagem_iptu: bool = typer.Option(False, "--listagem-iptu", help="Listagem de IPTUs"),
    carne_iptu: bool = typer.Option(False, "--carne-iptu", help="Carnê do IPTU"),
    visivel: bool = typer.Option(False, "--visivel", help="Abre o Chrome visível (útil para debug)"),
):
    """Gera documentos PDF para um imóvel."""
    pasta.mkdir(parents=True, exist_ok=True)
    pasta_str = str(pasta.resolve())

    if todos:
        extrato = certidao_negativa = existencia = valor_venal = listagem_iptu = carne_iptu = True

    from scraper_service import scraper

    docs_selecionados = []
    if extrato:
        docs_selecionados.append(("Extrato de Pagamentos", scraper.gerar_pdf_extrato))
    if certidao_negativa:
        docs_selecionados.append(("Certidão Negativa de Débitos", scraper.gerar_pdf_certidao_negativa))
    if existencia:
        docs_selecionados.append(("Certidão de Existência", scraper.gerar_pdf_existencia))
    if valor_venal:
        docs_selecionados.append(("Valor Venal", scraper.gerar_pdf_valor_venal))
    if listagem_iptu:
        docs_selecionados.append(("Listagem de IPTUs", scraper.gerar_pdf_listagem_iptu))
    if carne_iptu:
        docs_selecionados.append(("Carnê do IPTU", scraper.gerar_pdf_carne_iptu))

    if not docs_selecionados:
        console.print("[yellow]Nenhum documento selecionado. Use --todos ou selecione ao menos um.[/yellow]")
        raise typer.Exit(1)

    with console.status(f"[cyan]Buscando imóvel {inscricao}...[/cyan]"):
        try:
            scraper.buscar_imovel(inscricao, pasta_str, headless=not visivel)
        except Exception as e:
            console.print(f"[red]Erro ao buscar imóvel:[/red] {e}")
            raise typer.Exit(1)

    resultados = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Gerando documentos...", total=len(docs_selecionados))
        for nome, metodo in docs_selecionados:
            progress.update(task, description=f"Gerando [cyan]{nome}[/cyan]...")
            try:
                caminho = metodo()
                resultados.append((nome, caminho, None))
            except RuntimeError as e:
                resultados.append((nome, None, str(e)))
            except Exception as e:
                resultados.append((nome, None, f"Erro inesperado: {e}"))
            progress.advance(task)

    table = Table(title="Documentos Gerados", box=box.ROUNDED)
    table.add_column("Documento", style="cyan")
    table.add_column("Resultado")
    for nome, caminho, erro in resultados:
        if caminho:
            table.add_row(nome, f"[green]{caminho}[/green]")
        else:
            table.add_row(nome, f"[red]{erro}[/red]")
    console.print(table)


@app.command("lote")
def lote(
    arquivo: Path = typer.Option(..., "--arquivo", "-a", help="Planilha Excel com as inscrições (.xlsx/.xls)"),
    coluna: str = typer.Option(..., "--coluna", "-c", help="Nome da coluna com as inscrições"),
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde os resultados serão salvos"),
    visivel: bool = typer.Option(False, "--visivel", help="Abre o Chrome visível (útil para debug)"),
):
    """Processa múltiplas inscrições a partir de uma planilha Excel."""
    if not arquivo.exists():
        console.print(f"[red]Arquivo não encontrado:[/red] {arquivo}")
        raise typer.Exit(1)

    pasta.mkdir(parents=True, exist_ok=True)
    pasta_str = str(pasta.resolve())

    import pandas as pd
    try:
        df = pd.read_excel(arquivo)
    except Exception as e:
        console.print(f"[red]Erro ao ler Excel:[/red] {e}")
        raise typer.Exit(1)

    col_encontrada = next(
        (c for c in df.columns if c.strip().lower() == coluna.strip().lower()), None
    )
    if col_encontrada is None:
        console.print(f"[red]Coluna '{coluna}' não encontrada. Colunas disponíveis:[/red] {list(df.columns)}")
        raise typer.Exit(1)

    inscricoes = df[col_encontrada].dropna().astype(str).str.strip().tolist()
    if not inscricoes:
        console.print("[yellow]Nenhuma inscrição encontrada na planilha.[/yellow]")
        raise typer.Exit(1)

    console.print(f"[cyan]{len(inscricoes)} inscrições encontradas.[/cyan]\n")

    from scraper_service import scraper

    resultados = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processando...", total=len(inscricoes))
        for inscricao in inscricoes:
            progress.update(task, description=f"Consultando [cyan]{inscricao}[/cyan]...")
            try:
                resultado = scraper.obter_informacoes(inscricao, pasta_str, headless=not visivel)
                resultados.append({
                    "inscricao": inscricao,
                    "proprietario": resultado.get("nome_proprietario", ""),
                    "quadra": resultado.get("quadra", ""),
                    "lote": resultado.get("lote", ""),
                    "existe_debito": resultado.get("existe_debito", False),
                    "erro": "",
                })
            except Exception as e:
                resultados.append({
                    "inscricao": inscricao,
                    "proprietario": "", "quadra": "", "lote": "",
                    "existe_debito": None,
                    "erro": str(e),
                })
            progress.advance(task)

    table = Table(title="Resultados do Processamento em Lote", box=box.ROUNDED)
    table.add_column("Inscrição", style="cyan")
    table.add_column("Proprietário")
    table.add_column("Quadra")
    table.add_column("Lote")
    table.add_column("Débito")
    table.add_column("Erro", style="red")

    for r in resultados:
        if r["existe_debito"] is True:
            debito_str = "[red]Sim[/red]"
        elif r["existe_debito"] is False:
            debito_str = "[green]Não[/green]"
        else:
            debito_str = "-"
        table.add_row(
            r["inscricao"], r["proprietario"], r["quadra"],
            r["lote"], debito_str, r["erro"]
        )
    console.print(table)


@app.command("lote-documentos")
def lote_documentos(
    arquivo: Path = typer.Option(..., "--arquivo", "-a", help="Planilha Excel com as inscrições (.xlsx/.xls)"),
    coluna: str = typer.Option(..., "--coluna", "-c", help="Nome da coluna com as inscrições"),
    pasta: Path = typer.Option(..., "--pasta", "-p", help="Pasta onde os PDFs serão salvos"),
    todos: bool = typer.Option(False, "--todos", help="Gera todos os documentos disponíveis"),
    extrato: bool = typer.Option(False, "--extrato", help="Extrato de pagamentos"),
    certidao_negativa: bool = typer.Option(False, "--certidao-negativa", help="Certidão negativa de débitos"),
    existencia: bool = typer.Option(False, "--existencia", help="Certidão de existência do imóvel"),
    valor_venal: bool = typer.Option(False, "--valor-venal", help="Certidão de valor venal"),
    listagem_iptu: bool = typer.Option(False, "--listagem-iptu", help="Listagem de IPTUs"),
    carne_iptu: bool = typer.Option(False, "--carne-iptu", help="Carnê do IPTU"),
    visivel: bool = typer.Option(False, "--visivel", help="Abre o Chrome visível (útil para debug)"),
):
    """Gera documentos PDF para múltiplas inscrições a partir de uma planilha Excel."""
    if not arquivo.exists():
        console.print(f"[red]Arquivo não encontrado:[/red] {arquivo}")
        raise typer.Exit(1)

    pasta.mkdir(parents=True, exist_ok=True)
    pasta_str = str(pasta.resolve())

    import pandas as pd
    try:
        df = pd.read_excel(arquivo)
    except Exception as e:
        console.print(f"[red]Erro ao ler Excel:[/red] {e}")
        raise typer.Exit(1)

    col_encontrada = next(
        (c for c in df.columns if c.strip().lower() == coluna.strip().lower()), None
    )
    if col_encontrada is None:
        console.print(f"[red]Coluna '{coluna}' não encontrada. Colunas disponíveis:[/red] {list(df.columns)}")
        raise typer.Exit(1)

    inscricoes = df[col_encontrada].dropna().astype(str).str.strip().tolist()
    if not inscricoes:
        console.print("[yellow]Nenhuma inscrição encontrada na planilha.[/yellow]")
        raise typer.Exit(1)

    if todos:
        extrato = certidao_negativa = existencia = valor_venal = listagem_iptu = carne_iptu = True

    from scraper_service import scraper

    docs_selecionados = []
    if extrato:
        docs_selecionados.append(("Extrato de Pagamentos", scraper.gerar_pdf_extrato))
    if certidao_negativa:
        docs_selecionados.append(("Certidão Negativa de Débitos", scraper.gerar_pdf_certidao_negativa))
    if existencia:
        docs_selecionados.append(("Certidão de Existência", scraper.gerar_pdf_existencia))
    if valor_venal:
        docs_selecionados.append(("Valor Venal", scraper.gerar_pdf_valor_venal))
    if listagem_iptu:
        docs_selecionados.append(("Listagem de IPTUs", scraper.gerar_pdf_listagem_iptu))
    if carne_iptu:
        docs_selecionados.append(("Carnê do IPTU", scraper.gerar_pdf_carne_iptu))

    if not docs_selecionados:
        console.print("[yellow]Nenhum documento selecionado. Use --todos ou selecione ao menos um.[/yellow]")
        raise typer.Exit(1)

    console.print(f"[cyan]{len(inscricoes)} inscrições encontradas. Gerando {len(docs_selecionados)} documento(s) cada.[/cyan]\n")

    resultados = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Iniciando...", total=len(inscricoes))

        for inscricao in inscricoes:
            proprietario = ""

            progress.update(task, description=f"Buscando [cyan]{inscricao}[/cyan]...")
            try:
                scraper.buscar_imovel(inscricao, pasta_str, headless=not visivel)
                proprietario = (scraper._driver.dados_imovel or {}).get("nome_proprietario", "")
            except Exception as e:
                for nome_doc, _ in docs_selecionados:
                    resultados.append({
                        "inscricao": inscricao,
                        "proprietario": "",
                        "documento": nome_doc,
                        "caminho": None,
                        "erro": f"Erro ao buscar imóvel: {e}",
                    })
                progress.advance(task)
                continue

            for nome_doc, metodo in docs_selecionados:
                progress.update(task, description=f"Gerando [cyan]{nome_doc}[/cyan] para {inscricao}...")
                try:
                    caminho = metodo()
                    resultados.append({
                        "inscricao": inscricao,
                        "proprietario": proprietario,
                        "documento": nome_doc,
                        "caminho": caminho,
                        "erro": None,
                    })
                except RuntimeError as e:
                    resultados.append({
                        "inscricao": inscricao,
                        "proprietario": proprietario,
                        "documento": nome_doc,
                        "caminho": None,
                        "erro": str(e),
                    })
                except Exception as e:
                    resultados.append({
                        "inscricao": inscricao,
                        "proprietario": proprietario,
                        "documento": nome_doc,
                        "caminho": None,
                        "erro": f"Erro inesperado: {e}",
                    })

            progress.advance(task)

    table = Table(title="Resultados — Documentos em Lote", box=box.ROUNDED)
    table.add_column("Inscrição", style="cyan")
    table.add_column("Proprietário")
    table.add_column("Documento")
    table.add_column("Resultado")

    for r in resultados:
        if r["caminho"]:
            resultado_str = f"[green]{r['caminho']}[/green]"
        else:
            resultado_str = f"[red]{r['erro']}[/red]"
        table.add_row(r["inscricao"], r["proprietario"], r["documento"], resultado_str)

    console.print(table)


if __name__ == "__main__":
    app()
