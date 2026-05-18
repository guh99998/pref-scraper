# Pref Scraper

Automação de consulta e download de documentos imobiliários municipais via interface desktop.

## Sobre o Projeto

O **Pref Scraper** automatiza o acesso ao portal imobiliário da prefeitura, eliminando a necessidade de navegar manualmente pelo site para cada inscrição municipal. Com ele, é possível baixar múltiplos documentos em PDF e consultar informações de imóveis em lote — tudo em alguns cliques.

**Problema resolvido:** profissionais que precisam consultar ou baixar documentos de dezenas (ou centenas) de imóveis gastam horas navegando manualmente no portal. O Pref Scraper reduz isso a minutos.

---

## Funcionalidades

### Aba Documentos
- Seleção individual ou em massa de documentos por inscrição municipal
- Download automático dos PDFs selecionados na pasta de destino escolhida
- Barra de progresso em tempo real por documento
- Documentos suportados:
  - Extrato de Pagamentos
  - Certidão Negativa de Débitos
  - Certidão de Existência
  - Valor Venal do Imóvel
  - Listagem de IPTUs
  - Carnê do IPTU

### Aba Informações
- **Consulta individual:** retorna proprietário, quadra, lote e status de débito de uma inscrição
- **Consulta em lote via Excel:** importa uma planilha com múltiplas inscrições, processa cada uma sequencialmente e exibe os resultados em tabela com indicador visual de débito (verde/vermelho)

---

## Arquitetura

```
┌─────────────────────────────┐
│     Frontend (Flet)         │  Interface desktop multiplataforma
│  • Aba Documentos           │  construída em Python puro
│  • Aba Informações          │
└────────────┬────────────────┘
             │ HTTP (httpx async)
             ▼
┌─────────────────────────────┐
│     Backend (FastAPI)       │  API REST local na porta 8000
│  • /imovel/buscar           │
│  • /imovel/pdf/*            │
│  • /imovel/informacoes      │
└────────────┬────────────────┘
             │ Selenium WebDriver
             ▼
┌─────────────────────────────┐
│   Portal Imobiliário        │  Chrome headless navega,
│   da Prefeitura             │  preenche e baixa os PDFs
└─────────────────────────────┘
```

**Padrão de design:** [Page Object Model](https://martinfowler.com/bliki/PageObject.html) — cada tela do portal é representada por uma classe Python independente, tornando o código de automação organizado e fácil de manter.

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| Frontend | [Flet](https://flet.dev/) 0.85 |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| Automação | [Selenium](https://www.selenium.dev/) 4.43 + Chrome headless |
| HTTP Client | [httpx](https://www.python-httpx.org/) (async) |
| Planilhas | [pandas](https://pandas.pydata.org/) + openpyxl |
| Linguagem | Python 3.13 |

---

## Como Executar

### Pré-requisitos

- Python 3.10+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pref-scraper.git
cd pref-scraper

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

### Executando

Abra dois terminais na raiz do projeto:

```bash
# Terminal 1 — Backend
python backend/main.py

# Terminal 2 — Frontend
python frontend/main.py
```

---

## Como Usar

1. **Escolha a pasta de download** usando o botão no topo da janela
2. **Aba Documentos:** informe a inscrição municipal, marque os documentos desejados e clique em *Realizar Consulta*
3. **Aba Informações (individual):** informe a inscrição e clique em *Consultar* para ver proprietário, quadra, lote e status de débito
4. **Aba Informações (lote):** clique em *Importar Excel*, informe o nome da coluna com as inscrições e clique em *Processar*

---

## Estrutura do Projeto

```
pref-scraper/
├── backend/
│   ├── main.py                  # Entrada do servidor Uvicorn
│   ├── api.py                   # Endpoints FastAPI
│   ├── scraper_service.py       # Orquestração da automação
│   ├── browser.py               # Configuração do Chrome
│   ├── schemas.py               # Modelos Pydantic
│   ├── config/
│   │   └── selectors.py         # Seletores CSS/XPath do portal
│   ├── pages/                   # Page Objects (um por tela)
│   │   ├── home_page.py
│   │   ├── inscricao_home_page.py
│   │   ├── informacoes_completas_page.py
│   │   └── ...
│   └── utils/
│       └── waits.py             # Helpers de espera Selenium
└── frontend/
    └── main.py                  # Interface Flet (async)
```

---

## Aviso

Este projeto foi desenvolvido para o portal imobiliário de um município específico. O sistema de automação é dependente da estrutura do site local — **não funcionará em portais de outras prefeituras sem adaptações**.
