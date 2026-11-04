"""Toda a apresentação da CLI: banner, cabeçalho, linhas de resultado e resumo.

Banner, cabeçalho e resumo vão para stderr; as linhas de resultado vão para stdout,
para que `|` e `>` capturem só os dados. Usamos `Text` (sem markup) para que textos
vindos do portal ou de exceções, como "[+]", nunca sejam interpretados pelo Rich.
"""
from importlib.metadata import PackageNotFoundError, version

from rich.console import Console
from rich.text import Text

# Rich respeita NO_COLOR sozinho.
erro = Console(stderr=True)
saida = Console(highlight=False)

BANNER = r"""
    ____  ____  ___________      _____ __________  ___    ____  __________
   / __ \/ __ \/ ____/ ____/    / ___// ____/ __ \/   |  / __ \/ ____/ __ \
  / /_/ / /_/ / __/ / /_ ______\__ \/ /   / /_/ / /| | / /_/ / __/ / /_/ /
 / ____/ _, _/ /___/ __//_____/__/ / /___/ _, _/ ___ |/ ____/ /___/ _, _/
/_/   /_/ |_/_____/_/        /____/\____/_/ |_/_/  |_/_/   /_____/_/ |_|
"""

LARGURA_BANNER = 78
ESTILOS = {"+": "bold green", "-": "yellow", "!": "bold red", "*": "cyan"}


def versao() -> str:
    try:
        return version("pref-scraper")
    except PackageNotFoundError:
        return "0.2.0"


def texto_banner(largura: int) -> str:
    sub = f"v{versao()} · Monte Sião-MG"
    if largura < LARGURA_BANNER:
        return f"pref-scraper {sub}\n"
    return BANNER + sub.rjust(LARGURA_BANNER - 1) + "\n"


def exibir_banner():
    erro.print(Text(texto_banner(erro.width), style="cyan"), end="")


def _separador() -> Text:
    return Text("=" * min(erro.width, 63))


def cabecalho(itens: list[tuple[str, str]]):
    erro.print(_separador())
    largura = max(len(rotulo) for rotulo, _ in itens)
    for rotulo, valor in itens:
        erro.print(Text.assemble(("[*] ", ESTILOS["*"]), f"{rotulo:<{largura}} : {valor}"), soft_wrap=True)
    erro.print(_separador())


def _marcador(simbolo: str) -> Text:
    return Text(f"[{simbolo}]", style=ESTILOS[simbolo])


def _cortar(texto: str, largura: int) -> str:
    return texto if len(texto) <= largura else texto[: largura - 1] + "…"


def resultado(simbolo: str, inscricao: str, rotulo: str = "", detalhe: str | Text = ""):
    """Uma linha de resultado em stdout: `[+] inscrição  rótulo  detalhe`."""
    linha = Text.assemble(_marcador(simbolo), " ", f"{inscricao:<16}")
    if rotulo:
        linha.append(f"  {_cortar(rotulo, 28):<28}")
    if detalhe:
        linha.append("  ")
        linha.append(detalhe if isinstance(detalhe, Text) else Text(detalhe))
    saida.print(linha, soft_wrap=True)


def bloco(simbolo: str, titulo: str, itens: list[tuple[str, str | Text]]):
    """Bloco de chave/valor em stdout (usado pelo comando `info`)."""
    saida.print(Text.assemble(_marcador(simbolo), " ", titulo), soft_wrap=True)
    largura = max(len(chave) for chave, _ in itens)
    for chave, valor in itens:
        valor = valor if isinstance(valor, Text) else Text(valor)
        saida.print(Text.assemble(f"    {chave:<{largura}} : ", valor), soft_wrap=True)


def aviso(simbolo: str, mensagem: str):
    erro.print(Text.assemble(_marcador(simbolo), " ", mensagem), soft_wrap=True)


def _plural(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def resumo(segundos: float, ok: int, falhas: int, ignoradas: int):
    partes = [f"{ok} ok", _plural(falhas, "falha", "falhas")]
    if ignoradas:
        partes.append(_plural(ignoradas, "ignorada", "ignoradas"))
    erro.print(_separador())
    erro.print(Text.assemble(("[*] ", ESTILOS["*"]), f"Concluído em {segundos:.1f}s: {', '.join(partes)}"))


def debito(existe: bool) -> Text:
    return Text("COM DÉBITOS", style="bold red") if existe else Text("SEM DÉBITOS", style="bold green")
