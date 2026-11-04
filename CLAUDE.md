# pref-scraper

CLI em Python (Selenium) que consulta o portal imobiliário de Monte Sião-MG (SGP Cloud):
informações do imóvel, situação de débitos e geração de PDFs (certidões, extrato, carnê).

## Arquitetura
- `pref_scraper/cli.py` — comandos Typer finos; `ui.py` — toda a apresentação (banner, tabelas, cores).
- `pref_scraper/scraper_service.py` — orquestra o fluxo no portal (context manager que fecha o Chrome).
- `pref_scraper/pages/` — Page Objects (um por tela do portal); `config/selectors.py` — seletores.
- Lógica pura (testável sem navegador): `planilha.py`, `arquivos.py`, `debitos.py`, `documentos.py`, `models.py`.
- `main.py` na raiz é só um atalho para a CLI.

## Comandos
- Instalar: `pip install -e ".[dev]"`
- Testes: `pytest` · com navegador: `pytest -m navegador`
- Lint: `ruff check .` · Auditoria: `pip-audit`

## Fluxo de trabalho
1. Spec curta em `docs/specs/` (modelo em `000-modelo.md`).
2. TDD na lógica pura: teste falhando → código → refatorar.
3. Commits pequenos; revisão humana de cada diff.

## Dados pessoais (regra dura)
- Nunca versionar PDFs, planilhas ou HTML real do portal (`.gitignore` já cobre `*.pdf`, `*.xlsx`, `*.xls`).
- Fixtures em `tests/fixtures/portal/` devem ser **anonimizadas** (nome, CPF/CNPJ, RG, inscrição, endereço).
- Inscrições reais só na sessão/planilha local, nunca em código, testes ou commits.
- Tracebacks não devem exibir variáveis locais (`pretty_exceptions_show_locals=False`).

## Portal
O portal muda IDs gerados (`j_idtNNN`) a cada implantação. Prefira seletores por texto/rótulo/prefixo
de ID estável. Estado desconhecido da tela deve virar erro, nunca resposta "padrão".
