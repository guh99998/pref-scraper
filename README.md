# Pref Scraper

Automação de consulta e download de documentos imobiliários municipais via terminal.

## Sobre o Projeto

O **Pref Scraper** automatiza o acesso ao portal imobiliário da Prefeitura de Monte Sião-MG (SGP Cloud), eliminando a necessidade de navegar manualmente pelo site para cada inscrição municipal. Com ele, é possível consultar informações e situação de débitos de imóveis, baixar documentos em PDF e processar centenas de inscrições em lote, tudo pelo terminal.

**Problema resolvido:** quem precisa consultar ou baixar documentos de dezenas (ou centenas) de imóveis gasta horas navegando no portal. O Pref Scraper reduz isso a minutos.

---

## Funcionalidades

- **`info`**: proprietário, quadra/lote, endereço e situação de débito de um imóvel
- **`documentos`**: baixa PDFs selecionados para uma inscrição
- **`lote`**: consulta várias inscrições de uma planilha `.xlsx` e grava `resultados.csv`
- **`lote-documentos`**: baixa PDFs para várias inscrições de uma planilha

Documentos suportados: Extrato de Pagamentos, Certidão Negativa de Débitos, Certidão de Existência, Valor Venal, Listagem de IPTUs e Carnê do IPTU.

**Sobre "COM DÉBITOS":** o status só é `COM DÉBITOS` quando existe ao menos uma parcela **já vencida**. Parcelas em aberto com vencimento futuro aparecem como `SEM DÉBITOS`. Se a tela do portal não for reconhecida (por exemplo, o portal foi alterado), o resultado é **erro**, nunca "sem débitos".

---

## Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado (o Selenium baixa o driver compatível automaticamente)

---

## Instalação

```bash
git clone https://github.com/guh99998/pref-scraper.git
cd pref-scraper

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install -e .
```

Isso instala o comando `pref-scraper`. Também é possível rodar sem instalar o comando, com `python main.py ...`.

---

## Como Usar

```bash
pref-scraper [--sem-banner] <comando> [opções]
pref-scraper --version
```

Opções globais: `--version` e `--sem-banner`. O banner, o cabeçalho e o resumo saem em **stderr**; as linhas de resultado saem em **stdout**. Assim `|` e `>` capturam apenas os dados:

```bash
pref-scraper lote -a imoveis.xlsx -c inscricao -p resultados > saida.txt   # saida.txt sem banner
```

A cor respeita a variável `NO_COLOR`. Em terminais estreitos o banner vira uma linha só.

**Códigos de saída:** `0` tudo certo · `1` alguma falha · `2` uso incorreto (opção faltando, coluna inexistente, planilha inválida).

Marcadores das linhas de resultado: `[+]` sucesso · `[-]` ignorado (ex.: carnê sem parcelas em aberto) · `[!]` falha.

---

### `info`: consultar um imóvel

```bash
pref-scraper info --inscricao 9999999999999999
```

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--inscricao` / `-i` | Sim | Número de inscrição municipal |
| `--visivel` | Não | Abre o Chrome visível e o mantém aberto (debug) |

Exemplo de saída (dados fictícios):

```
[+] Imóvel 9999999999999999
    Proprietário : FULANO DE TAL
    Quadra/Lote  : 3 / 8
    Endereço     : RUA DAS FLORES, 123 - CENTRO
    Situação     : SEM DÉBITOS
```

---

### `documentos`: gerar PDFs de um imóvel

```bash
pref-scraper documentos -i 9999999999999999 -p C:\Downloads\pdfs --todos
pref-scraper documentos -i 9999999999999999 -p C:\Downloads\pdfs --extrato --certidao-negativa
```

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--inscricao` / `-i` | Sim | Número de inscrição municipal |
| `--pasta` / `-p` | Sim | Pasta onde os PDFs serão salvos |
| `--todos` | Não | Gera todos os documentos |
| `--extrato` | Não | Extrato de pagamentos |
| `--certidao-negativa` | Não | Certidão negativa de débitos |
| `--existencia` | Não | Certidão de existência do imóvel |
| `--valor-venal` | Não | Certidão de valor venal |
| `--listagem-iptu` | Não | Listagem de IPTUs |
| `--carne-iptu` | Não | Carnê do IPTU |
| `--visivel` | Não | Abre o Chrome visível e o mantém aberto (debug) |

Os arquivos são nomeados `BAIRRO_QUADRA_LOTE - tipo.pdf`. Um arquivo existente **nunca é sobrescrito**: o novo recebe o sufixo ` (2)`, ` (3)`...

---

### `lote`: consultar uma planilha

```bash
pref-scraper lote -a imoveis.xlsx -c inscricao -p C:\Downloads\resultados
```

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--arquivo` / `-a` | Sim | Planilha Excel **.xlsx** |
| `--coluna` / `-c` | Sim | Nome da coluna com as inscrições (sem diferenciar maiúsculas) |
| `--pasta` / `-p` | Sim | Pasta onde `resultados.csv` será salvo |
| `--visivel` | Não | Abre o Chrome visível e o mantém aberto (debug) |

As inscrições são lidas como **texto**, então zeros à esquerda são preservados. O `resultados.csv` é gravado em `utf-8-sig` com separador `;`, para abrir direto no Excel.

Exemplo de saída (dados fictícios):

```
[+] 9999999999999991  FULANO DE TAL               Qd 3 Lt 8  SEM DÉBITOS
[+] 9999999999999992  BELTRANO DA SILVA           Qd 4 Lt 12  COM DÉBITOS
[!] 9999999999999993  Imóvel localizado, porém o cadastro não pode acessar o sistema...
```

---

### `lote-documentos`: gerar PDFs de uma planilha

```bash
pref-scraper lote-documentos -a imoveis.xlsx -c inscricao -p C:\Downloads\pdfs --extrato --carne-iptu
```

Aceita as mesmas opções de `lote` (menos o CSV) e as de seleção de documentos de `documentos`. Uma falha em uma inscrição **não interrompe** as demais, e o comando termina com código `1` se houve alguma falha.

---

## Modo Debug (`--visivel`)

Todos os comandos aceitam `--visivel`, que abre o Chrome em primeiro plano e **o mantém aberto** ao final. Sem essa opção o Chrome roda em segundo plano e é sempre fechado.

---

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest                    # testes sem navegador
pytest -m navegador       # testes que abrem o Chrome (usam HTML salvo em tests/fixtures/portal)
ruff check .
pip-audit --skip-editable
```

- O fluxo de trabalho (spec curta, TDD na lógica pura, revisão de cada diff) está descrito em [`CLAUDE.md`](CLAUDE.md); as specs ficam em [`docs/specs/`](docs/specs/).
- **Dados pessoais:** nunca versionar PDFs, planilhas ou HTML real do portal. Fixtures devem ser anonimizadas.
- O portal troca IDs gerados (`j_idtNNN`) a cada implantação. Prefira seletores por texto, rótulo ou prefixo de ID estável.

## Estrutura do Projeto

```
pref-scraper/
├── main.py                      # atalho para a CLI
├── pyproject.toml
├── CLAUDE.md
├── docs/specs/                  # especificações
├── tests/                       # testes (fixtures/portal: HTML anonimizado)
└── pref_scraper/
    ├── cli.py                   # comandos (finos)
    ├── ui.py                    # banner, cores, linhas de resultado
    ├── scraper_service.py       # orquestra o fluxo no portal (context manager)
    ├── browser.py               # configuração do Chrome
    ├── planilha.py              # leitura de .xlsx (puro)
    ├── arquivos.py              # nomes de arquivo, sem sobrescrever (puro)
    ├── debitos.py               # regra de débito vencido (puro)
    ├── documentos.py            # registro dos 6 documentos (puro)
    ├── models.py                # DadosImovel, InformacoesImovel
    ├── relatorio.py             # resultados.csv
    ├── config/selectors.py      # seletores do portal
    ├── pages/                   # Page Objects (um por tela)
    └── utils/                   # esperas, download e leitura de campos
```

---

## Aviso

Este projeto foi desenvolvido para o portal imobiliário de um município específico (Monte Sião-MG). A automação depende da estrutura do site e **não funciona em portais de outras prefeituras sem adaptações**.
