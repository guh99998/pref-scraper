import asyncio

import flet as ft
import httpx
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


async def main(page: ft.Page):
    page.title = "Pref Scraper"
    page.window_width = 750
    page.window_height = 650
    page.window_resizable = True

    # ── Aba 1: Documentos ─────────────────────────────────────────

    ENDPOINTS = [
        "/imovel/pdf/extrato",
        "/imovel/pdf/certidao-negativa",
        "/imovel/pdf/existencia",
        "/imovel/pdf/valor-venal",
        "/imovel/pdf/listagem-iptu",
        "/imovel/pdf/carne-iptu",
    ]

    checkboxes = [
        ft.Checkbox(label="Extrato de Pagamentos"),
        ft.Checkbox(label="Certidão Negativa de Débitos"),
        ft.Checkbox(label="Certidão de Existência"),
        ft.Checkbox(label="Valor Venal do Imóvel"),
        ft.Checkbox(label="Listagem IPTUs"),
        ft.Checkbox(label="Carnê do IPTU"),
    ]

    def check_all_items(e):
        for cb in checkboxes:
            cb.value = select_all_check.value
        page.update()

    select_all_check = ft.Checkbox(label="Selecionar Todos", on_change=check_all_items)

    inscricao_doc = ft.TextField(label="Inscrição Municipal", hint_text="0001030830032001")

    pasta_selecionada = {"valor": ""}
    pasta_texto = ft.Text("Nenhuma pasta selecionada", size=12, color=ft.Colors.GREY_500)

    pasta_picker = ft.FilePicker()
    page.services.append(pasta_picker)

    async def escolher_pasta(_):
        path = await pasta_picker.get_directory_path()
        if path:
            pasta_selecionada["valor"] = path
            pasta_texto.value = path
            page.update()

    progress_doc = ft.ProgressBar(value=0, width=680)
    status_doc = ft.Text("", size=12)
    btn_consultar = ft.Button("Realizar Consulta")

    async def realizar_consulta(_):
        inscricao = inscricao_doc.value.strip()
        pasta = pasta_selecionada["valor"]
        selecionados = [
            (checkboxes[i].label, ENDPOINTS[i])
            for i in range(len(checkboxes))
            if checkboxes[i].value
        ]

        if not inscricao:
            status_doc.value = "Preencha a inscrição municipal."
            page.update()
            return
        if not pasta:
            status_doc.value = "Escolha uma pasta de destino."
            page.update()
            return
        if not selecionados:
            status_doc.value = "Selecione ao menos um documento."
            page.update()
            return

        btn_consultar.disabled = True
        progress_doc.value = 0
        status_doc.value = "Conectando ao backend..."
        page.update()

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(
                    f"{BASE_URL}/imovel/buscar",
                    json={"inscricao": inscricao, "pasta_download": pasta},
                )
                r.raise_for_status()

                total = len(selecionados)
                concluidos = 0
                erros = []

                for label, endpoint in selecionados:
                    status_doc.value = f"Gerando {label}... ({concluidos + 1}/{total})"
                    page.update()

                    try:
                        r = await client.post(
                            f"{BASE_URL}{endpoint}",
                            json={"inscricao": inscricao, "pasta_download": pasta},
                        )
                        r.raise_for_status()
                        concluidos += 1
                    except Exception as ex:
                        erros.append(f"{label}: {str(ex)[:60]}")

                    progress_doc.value = concluidos / total
                    page.update()

            if erros:
                status_doc.value = f"Concluído com {len(erros)} erro(s): {'; '.join(erros)}"
            else:
                status_doc.value = f"Concluído! {concluidos} documento(s) baixado(s)."

        except Exception as ex:
            status_doc.value = f"Erro de conexão: {str(ex)[:80]}"
        finally:
            btn_consultar.disabled = False
            page.update()

    btn_consultar.on_click = realizar_consulta

    aba_documentos = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                inscricao_doc,
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            ),
            ft.Container(
                ft.Column([
                    ft.Row([select_all_check]),
                    ft.Row(
                        [checkboxes[0], checkboxes[1]],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [checkboxes[2], checkboxes[3]],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [checkboxes[4], checkboxes[5]],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
                padding=10,
            ),
            ft.Container(
                btn_consultar,
                padding=ft.Padding.symmetric(horizontal=10),
            ),
            ft.Container(
                progress_doc,
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            ),
            ft.Container(
                status_doc,
                padding=ft.Padding.symmetric(horizontal=10),
            ),
        ],
    )

    # ── Aba 2: Informações ────────────────────────────────────────

    # Seção A: inscrição única
    inscricao_info = ft.TextField(label="Inscrição Municipal", hint_text="0001030830032001")
    btn_consultar_info = ft.Button("Consultar")

    resultado_nome = ft.Text("", size=13)
    resultado_quadra_lote = ft.Text("", size=13)
    resultado_debito = ft.Text("", size=13, weight=ft.FontWeight.BOLD)
    card_resultado = ft.Container(
        ft.Column([resultado_nome, resultado_quadra_lote, resultado_debito]),
        padding=10,
        border=ft.Border.all(1, ft.Colors.GREY_400),
        border_radius=8,
        visible=False,
    )

    async def consultar_info(_):
        inscricao = inscricao_info.value.strip()
        if not inscricao:
            resultado_nome.value = "Preencha a inscrição."
            resultado_quadra_lote.value = ""
            resultado_debito.value = ""
            card_resultado.visible = True
            page.update()
            return

        btn_consultar_info.disabled = True
        resultado_nome.value = "Consultando..."
        resultado_quadra_lote.value = ""
        resultado_debito.value = ""
        card_resultado.visible = True
        page.update()

        pasta = pasta_selecionada["valor"]
        if not pasta:
            resultado_nome.value = "Escolha uma pasta de download primeiro."
            resultado_quadra_lote.value = ""
            resultado_debito.value = ""
            card_resultado.visible = True
            btn_consultar_info.disabled = False
            page.update()
            return

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(
                    f"{BASE_URL}/imovel/buscar",
                    json={"inscricao": inscricao, "pasta_download": pasta},
                )
                r.raise_for_status()

                r = await client.post(
                    f"{BASE_URL}/imovel/informacoes",
                    json={"inscricao": inscricao, "pasta_download": pasta},
                )
                r.raise_for_status()
                dados = r.json()

            resultado_nome.value = f"Proprietário: {dados['nome_proprietario']}"
            resultado_quadra_lote.value = f"Quadra: {dados['quadra']}  |  Lote: {dados['lote']}"
            if dados["existe_debito"]:
                resultado_debito.value = "Com débitos"
                resultado_debito.color = ft.Colors.RED_600
            else:
                resultado_debito.value = "Sem débitos"
                resultado_debito.color = ft.Colors.GREEN_600

        except Exception as ex:
            resultado_nome.value = f"Erro: {str(ex)[:80]}"
            resultado_quadra_lote.value = ""
            resultado_debito.value = ""
        finally:
            btn_consultar_info.disabled = False
            page.update()

    btn_consultar_info.on_click = consultar_info

    # Seção B: lote via Excel
    excel_caminho = {"valor": ""}
    excel_texto = ft.Text("Nenhum arquivo selecionado", size=12, color=ft.Colors.GREY_500)

    excel_picker = ft.FilePicker()
    page.services.append(excel_picker)

    async def escolher_excel(_):
        files = await excel_picker.pick_files(allowed_extensions=["xlsx", "xls"])
        if files:
            excel_caminho["valor"] = files[0].path
            excel_texto.value = files[0].name
            page.update()

    coluna_nome = ft.TextField(label="Nome da coluna", hint_text="inscricao", width=200)
    progress_excel = ft.ProgressBar(value=0, width=680, visible=False)
    status_excel = ft.Text("", size=12)
    btn_processar = ft.Button("Processar")

    tabela_resultado = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Inscrição")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Quadra")),
            ft.DataColumn(ft.Text("Lote")),
            ft.DataColumn(ft.Text("Débito")),
        ],
        rows=[],
    )

    async def processar_excel(_):
        caminho = excel_caminho["valor"]
        coluna = coluna_nome.value.strip()

        if not caminho:
            status_excel.value = "Importe um arquivo Excel primeiro."
            page.update()
            return
        if not coluna:
            status_excel.value = "Informe o nome da coluna."
            page.update()
            return

        btn_processar.disabled = True
        tabela_resultado.rows.clear()
        progress_excel.visible = True
        progress_excel.value = 0
        status_excel.value = "Lendo arquivo..."
        page.update()

        try:
            df = await asyncio.to_thread(pd.read_excel, caminho)

            col_match = next(
                (c for c in df.columns if c.strip().lower() == coluna.lower()), None
            )
            if col_match is None:
                status_excel.value = f"Coluna '{coluna}' não encontrada no arquivo."
                progress_excel.visible = False
                page.update()
                return

            inscricoes = df[col_match].dropna().astype(str).str.strip().tolist()
            total = len(inscricoes)

            pasta = pasta_selecionada["valor"]
            if not pasta:
                status_excel.value = "Escolha uma pasta de download primeiro."
                progress_excel.visible = False
                btn_processar.disabled = False
                page.update()
                return

            async with httpx.AsyncClient(timeout=120) as client:
                for idx, insc in enumerate(inscricoes):
                    status_excel.value = f"Consultando {insc}... ({idx + 1}/{total})"
                    page.update()

                    try:
                        await client.post(
                            f"{BASE_URL}/imovel/buscar",
                            json={"inscricao": insc, "pasta_download": pasta},
                        )
                        r = await client.post(
                            f"{BASE_URL}/imovel/informacoes",
                            json={"inscricao": insc, "pasta_download": pasta},
                        )
                        r.raise_for_status()
                        d = r.json()
                        debito_cor = (
                            ft.Colors.RED_600 if d["existe_debito"] else ft.Colors.GREEN_600
                        )
                        tabela_resultado.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(insc)),
                                ft.DataCell(ft.Text(d["nome_proprietario"])),
                                ft.DataCell(ft.Text(d["quadra"])),
                                ft.DataCell(ft.Text(d["lote"])),
                                ft.DataCell(
                                    ft.Text(
                                        "Sim" if d["existe_debito"] else "Não",
                                        color=debito_cor,
                                    )
                                ),
                            ])
                        )
                    except Exception as ex:
                        tabela_resultado.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(insc)),
                                ft.DataCell(
                                    ft.Text(f"Erro: {str(ex)[:40]}", color=ft.Colors.RED_400)
                                ),
                                ft.DataCell(ft.Text("")),
                                ft.DataCell(ft.Text("")),
                                ft.DataCell(ft.Text("")),
                            ])
                        )

                    progress_excel.value = (idx + 1) / total
                    page.update()

            status_excel.value = f"Concluído! {total} inscrição(ões) processada(s)."

        except Exception as ex:
            status_excel.value = f"Erro ao ler Excel: {str(ex)[:80]}"
        finally:
            btn_processar.disabled = False
            page.update()

    btn_processar.on_click = processar_excel

    aba_informacoes = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Consulta Individual", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                inscricao_info,
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            ),
            ft.Container(
                btn_consultar_info,
                padding=ft.Padding.symmetric(horizontal=10),
            ),
            ft.Container(
                card_resultado,
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            ),
            ft.Divider(),
            ft.Text("Consulta em Lote (Excel)", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Button("Importar Excel", on_click=escolher_excel),
                excel_texto,
            ]),
            ft.Row([coluna_nome, btn_processar]),
            ft.Container(
                progress_excel,
                padding=ft.Padding.symmetric(vertical=5),
            ),
            ft.Container(status_excel),
            ft.Container(
                ft.Column([tabela_resultado], scroll=ft.ScrollMode.AUTO),
                padding=ft.Padding.symmetric(vertical=5),
            ),
        ],
    )

    # ── Layout principal ──────────────────────────────────────────
    # Flet 0.85: TabBar + TabBarView dentro de ft.Tabs (controller)

    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Documentos"),
            ft.Tab(label="Informações"),
        ],
    )

    tab_view = ft.TabBarView(
        controls=[
            ft.Container(aba_documentos, padding=10),
            ft.Container(aba_informacoes, padding=10),
        ],
        expand=True,
    )

    pasta_row = ft.Container(
        ft.Row(
            controls=[
                ft.Button("Escolher Pasta de Download", on_click=escolher_pasta),
                pasta_texto,
            ],
        ),
        padding=ft.Padding.symmetric(horizontal=10, vertical=8),
    )

    page.add(
        ft.Column(
            controls=[
                pasta_row,
                ft.Tabs(
                    content=ft.Column([tab_bar, tab_view], expand=True),
                    length=2,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


ft.run(main)
