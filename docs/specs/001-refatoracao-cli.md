# 001 — Refatoração da CLI

## Objetivo
Deixar o pref-scraper uma ferramenta CLI exclusiva, sem duplicação nem resquícios de API/GUI,
com lógica pura testada, saída no estilo nmap e comportamento seguro em lote.

## Comportamento
- Comandos: `info`, `documentos`, `lote`, `lote-documentos`.
- Banner e progresso em **stderr**; resultados em **stdout** (`|` e `>` funcionam).
- Opções globais `--version` e `--sem-banner`; `NO_COLOR` respeitado.
- Códigos de saída: 0 tudo certo, 1 alguma falha, 2 uso incorreto.
- `lote` grava `resultados.csv` (`utf-8-sig`) na `--pasta`.
- Débito: só "COM DÉBITOS" (tabela reconhecida) ou "SEM DÉBITOS" (mensagem reconhecida).
  Se nenhum dos dois for reconhecido, é **erro**, nunca "sem débitos".
- Planilhas: só `.xlsx`; inscrições lidas como texto, preservando zeros à esquerda.
- Arquivos baixados nunca sobrescrevem outros (sufixo ` (2)`).
- O Chrome sempre é fechado ao fim (exceto com `--visivel`).

## Fora de escopo
- Integração externa (spec 002).
- Trocar os demais XPaths absolutos.
- Paralelismo, retries, logging estruturado.

## Critérios de aceite
- `ruff check .` e `pytest` passam (e `pytest -m navegador` localmente).
- Teste manual no portal: `info` com e sem débito; `documentos --todos`; `lote` e
  `lote-documentos` com uma inscrição inválida terminam com exit code 1 sem interromper o lote.
- `pref-scraper lote ... > saida.txt` não contém banner; nenhum `chrome.exe` sobra.
