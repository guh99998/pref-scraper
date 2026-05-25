# Pref Scraper

Automação de consulta e download de documentos imobiliários municipais via terminal.

## Sobre o Projeto

O **Pref Scraper** automatiza o acesso ao portal imobiliário da prefeitura, eliminando a necessidade de navegar manualmente pelo site para cada inscrição municipal. Com ele, é possível consultar informações de imóveis, baixar múltiplos documentos em PDF e processar centenas de inscrições em lote — tudo pelo terminal.

**Problema resolvido:** profissionais que precisam consultar ou baixar documentos de dezenas (ou centenas) de imóveis gastam horas navegando manualmente no portal. O Pref Scraper reduz isso a minutos.

---

## Funcionalidades

- **`info`** — consulta proprietário, endereço e status de débito de um imóvel
- **`documentos`** — baixa PDFs selecionados para uma inscrição
- **`lote`** — processa uma planilha Excel com múltiplas inscrições e exibe os resultados em tabela

Documentos suportados:
- Extrato de Pagamentos
- Certidão Negativa de Débitos
- Certidão de Existência
- Valor Venal do Imóvel
- Listagem de IPTUs
- Carnê do IPTU

---

## Pré-requisitos

- Python 3.10+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome (o Selenium baixa automaticamente)

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pref-scraper.git
cd pref-scraper

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

---

## Como Usar

Todos os comandos são executados a partir da raiz do projeto:

```bash
python main.py <comando> [opções]
```

---

### `info` — Consultar informações de um imóvel

```bash
python main.py info --inscricao <inscricao>
```

**Opções:**

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--inscricao` / `-i` | Sim | Número de inscrição municipal |
| `--visivel` | Não | Abre o Chrome visível (útil para debug) |

**Exemplo:**

```bash
python main.py info --inscricao 0001030830032001
```

**Saída:**
```
╭─ Imóvel 0001030830032001 ──────────────────────────────╮
│ Proprietário: JOÃO DA SILVA                            │
│ Quadra: 003  Lote: 0008                                │
│ Endereço: RUA DAS FLORES, 123 - CENTRO                 │
│ Status: SEM DÉBITOS                                    │
╰────────────────────────────────────────────────────────╯
```

---

### `documentos` — Gerar PDFs de um imóvel

```bash
python main.py documentos --inscricao <inscricao> --pasta <pasta> [documentos]
```

**Opções:**

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--inscricao` / `-i` | Sim | Número de inscrição municipal |
| `--pasta` / `-p` | Sim | Pasta onde os PDFs serão salvos |
| `--todos` | Não | Gera todos os documentos disponíveis |
| `--extrato` | Não | Extrato de pagamentos |
| `--certidao-negativa` | Não | Certidão negativa de débitos |
| `--existencia` | Não | Certidão de existência do imóvel |
| `--valor-venal` | Não | Certidão de valor venal |
| `--listagem-iptu` | Não | Listagem de IPTUs |
| `--carne-iptu` | Não | Carnê do IPTU |
| `--visivel` | Não | Abre o Chrome visível (útil para debug) |

**Exemplos:**

```bash
# Gerar todos os documentos
python main.py documentos --inscricao 0001030830032001 --pasta C:\Downloads --todos

# Gerar apenas extrato e certidão negativa
python main.py documentos --inscricao 0001030830032001 --pasta C:\Downloads --extrato --certidao-negativa
```

**Saída:**
```
╭─ Documentos Gerados ───────────────────────────────────────────────╮
│ Extrato de Pagamentos      C:\Downloads\CENTRO_003_0008_extrato.pdf │
│ Certidão Negativa          C:\Downloads\CENTRO_003_0008_certidao.pdf│
╰─────────────────────────────────────────────────────────────────────╯
```

---

### `lote` — Processar planilha Excel em lote

```bash
python main.py lote --arquivo <arquivo.xlsx> --coluna <coluna> --pasta <pasta>
```

**Opções:**

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--arquivo` / `-a` | Sim | Caminho para a planilha Excel (.xlsx ou .xls) |
| `--coluna` / `-c` | Sim | Nome da coluna que contém as inscrições |
| `--pasta` / `-p` | Sim | Pasta onde os resultados serão salvos |
| `--visivel` | Não | Abre o Chrome visível (útil para debug) |

**Exemplo:**

```bash
python main.py lote --arquivo imoveis.xlsx --coluna inscricao --pasta C:\Downloads\resultados
```

**Saída:**
```
3 inscrições encontradas.

╭─ Resultados do Processamento em Lote ──────────────────────────────────────╮
│ Inscrição          Proprietário     Quadra  Lote  Débito  Erro             │
│ 0001030830032001   JOÃO DA SILVA    003     0008  Não                      │
│ 0001030830033001   MARIA SOUZA      004     0012  Sim                      │
│ 0001030830034001   PEDRO LIMA       005     0003  Não                      │
╰────────────────────────────────────────────────────────────────────────────╯
```

> A coluna `--coluna` é case-insensitive. Se a planilha tiver a coluna `Inscricao`, `INSCRICAO` ou `inscricao`, todas funcionam.

---

### `lote-documentos` — Gerar PDFs em lote a partir de planilha Excel

```bash
python main.py lote-documentos --arquivo <arquivo.xlsx> --coluna <coluna> --pasta <pasta> [documentos]
```

**Opções:**

| Opção | Obrigatório | Descrição |
|-------|-------------|-----------|
| `--arquivo` / `-a` | Sim | Caminho para a planilha Excel (.xlsx ou .xls) |
| `--coluna` / `-c` | Sim | Nome da coluna que contém as inscrições |
| `--pasta` / `-p` | Sim | Pasta onde os PDFs serão salvos |
| `--todos` | Não | Gera todos os documentos disponíveis |
| `--extrato` | Não | Extrato de pagamentos |
| `--certidao-negativa` | Não | Certidão negativa de débitos |
| `--existencia` | Não | Certidão de existência do imóvel |
| `--valor-venal` | Não | Certidão de valor venal |
| `--listagem-iptu` | Não | Listagem de IPTUs |
| `--carne-iptu` | Não | Carnê do IPTU |
| `--visivel` | Não | Abre o Chrome visível (útil para debug) |

**Exemplos:**

```bash
# Gerar todos os documentos para cada inscrição da planilha
python main.py lote-documentos --arquivo imoveis.xlsx --coluna inscricao --pasta C:\Downloads\pdfs --todos

# Gerar apenas extrato e certidão negativa
python main.py lote-documentos --arquivo imoveis.xlsx --coluna inscricao --pasta C:\Downloads\pdfs --extrato --certidao-negativa
```

**Saída:**
```
3 inscrições encontradas. Gerando 2 documento(s) cada.

╭─ Resultados — Documentos em Lote ────────────────────────────────────────────────────────────╮
│ Inscrição          Proprietário    Documento                Resultado                         │
│ 0001030830032001   JOÃO DA SILVA   Extrato de Pagamentos    C:\Downloads\pdfs\...extrato.pdf  │
│ 0001030830032001   JOÃO DA SILVA   Certidão Negativa        C:\Downloads\pdfs\...certidao.pdf │
│ 0001030830033001   MARIA SOUZA     Extrato de Pagamentos    C:\Downloads\pdfs\...extrato.pdf  │
│ 0001030830033001   MARIA SOUZA     Certidão Negativa        C:\Downloads\pdfs\...certidao.pdf │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
```

> Erros em uma inscrição específica não interrompem o processamento das demais.

---

## Modo Debug (`--visivel`)

Todos os comandos aceitam a flag `--visivel`, que abre o Chrome em primeiro plano em vez de rodar em segundo plano (headless). Útil para acompanhar a navegação ou investigar erros:

```bash
python main.py info --inscricao 0001030830032001 --visivel
```

---

## Estrutura do Projeto

```
pref-scraper/
├── main.py                      # Entry point CLI (4 comandos)
├── requirements.txt
├── backend/
│   ├── scraper_service.py       # Orquestração da automação
│   ├── browser.py               # Configuração do Chrome
│   ├── schemas.py               # Modelos de dados
│   ├── config/
│   │   └── selectors.py         # Seletores XPath do portal
│   ├── pages/                   # Page Objects (um por tela do portal)
│   │   ├── home_page.py
│   │   ├── inscricao_home_page.py
│   │   ├── informacoes_completas_page.py
│   │   ├── debitos_em_aberto_page.py
│   │   ├── certidao_negativa_debitos_page.py
│   │   ├── certidao_existencia_imovel_page.py
│   │   ├── certidao_valor_venal_page.py
│   │   ├── consultar_movimentacoes_extrato_page.py
│   │   └── emitir_carne_iptu_page.py
│   └── utils/
│       └── waits.py             # Helpers de espera Selenium
└── README.md
```

---

## Aviso

Este projeto foi desenvolvido para o portal imobiliário de um município específico (Monte Sião - MG). O sistema de automação é dependente da estrutura do site — **não funcionará em portais de outras prefeituras sem adaptações**.
