#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TM-Testes — TM Gerenciador E2E Suite"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser

BASE_URL  = "http://localhost:3000"
SHOTS_DIR = Path("C:/Users/thiag/Desktop/tm-tecnologia/TM_Gerenciador/test_screenshots")
REPORT    = Path("C:/Users/thiag/Desktop/tm-tecnologia/TM_Gerenciador/test_report.html")

results = []
console_errors = []

IGNORAR = [
    "favicon", "fonts.googleapis", "fonts.gstatic",
    "ERR_CONNECTION_REFUSED", "ERR_NAME_NOT_RESOLVED",
    "analytics", "cdn.", "gtag", "ResizeObserver",
    "cross-origin", "React DevTools", "localhost:8000",
    "Download the React", "hydrat",
]

def add(name, passed, detail="", shot_path=""):
    results.append({"name": name, "passed": passed, "detail": detail, "screenshot": shot_path})
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} {name}" + (f"\n         -> {detail[:160]}" if not passed and detail else ""))

def make_page(browser: Browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.on("console", lambda m: console_errors.append(f"[{m.type.upper()}] {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: console_errors.append(f"[PAGEERROR] {e}"))
    return page

def goto(page: Page, url: str):
    page.goto(url, timeout=35000, wait_until="domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except:
        pass

def shot(page: Page, name: str):
    p = str(SHOTS_DIR / f"{name}.png")
    try:
        page.screenshot(path=p, full_page=True)
    except Exception as e:
        print(f"    [screenshot falhou: {e}]")
        p = ""
    return p

def test_pagina(browser: Browser, label: str, url: str, shot_name: str, checks):
    print(f"\n{label}")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + url)
        for check in checks:
            check(page, shot_name)
        shot(page, shot_name)
        page.context.close()
    except Exception as e:
        add(f"{label} — carrega", False, str(e)[:160])

def run(pw):
    SHOTS_DIR.mkdir(exist_ok=True)
    browser = pw.chromium.launch(headless=False, slow_mo=250)

    # ── 1. Dashboard ──────────────────────────────────────────
    print("\n[1/9] Dashboard /")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/")

        logo = page.locator("img[alt='TM Gerenciador']")
        add("Header — logo TM visível", logo.count() > 0 and logo.first.is_visible())

        sidebar = page.locator("aside")
        add("Sidebar dark visível", sidebar.count() > 0 and sidebar.first.is_visible())

        cards = page.locator("main .text-2xl").all_text_contents()
        kpi_ok = any(t.strip() not in ("", "—", "…") for t in cards)
        add("KPI cards com dados reais", kpi_ok, str(cards[:4]))

        svgs = page.locator("main svg").count()
        add(f"Gráficos Recharts renderizados ({svgs} SVGs)", svgs >= 4)

        shot(page, "01_dashboard")
        page.context.close()
    except Exception as e:
        add("Dashboard carrega", False, str(e)[:160])

    # ── 2. Sidebar toggle ─────────────────────────────────────
    print("\n[2/9] Sidebar toggle")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/")
        toggle = page.locator("button[title='Recolher']")
        if toggle.count() > 0:
            w_antes = page.locator("aside").first.bounding_box()["width"]
            toggle.click()
            page.wait_for_timeout(450)
            w_depois = page.locator("aside").first.bounding_box()["width"]
            add("Sidebar colapsa ao clicar toggle", w_depois < w_antes, f"{w_antes}→{w_depois}")
            shot(page, "02_sidebar_colapsada")
            page.locator("button[title='Expandir']").click()
            page.wait_for_timeout(450)
        else:
            add("Sidebar toggle — botão encontrado", False, "title='Recolher' não encontrado")
        page.context.close()
    except Exception as e:
        add("Sidebar toggle", False, str(e)[:160])

    # ── 3. Todas as O.S ───────────────────────────────────────
    print("\n[3/9] /ordens")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/ordens")
        # Aguarda tabela ou empty state
        page.wait_for_timeout(2000)
        rows = page.locator("table tbody tr").count()
        # Fallback: divs com número de OS (pode ser lista card)
        if rows == 0:
            rows = page.locator("[data-row], .os-row").count()
        sem = page.locator("text=Nenhuma ordem, text=nenhum").count()
        add(f"Ordens — {rows} linhas carregadas", rows > 0, f"0 linhas — pode ser renderização assíncrona" if rows == 0 else "")
        filtros = page.locator("input[placeholder], select").count()
        add(f"Ordens — filtros visíveis ({filtros})", filtros > 0)
        shot(page, "03_ordens")
        page.context.close()
    except Exception as e:
        add("Tela /ordens carrega", False, str(e)[:160])

    # ── 4. Notificações ───────────────────────────────────────
    print("\n[4/9] /notificacoes")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/notificacoes")
        stub = page.locator("text=em construção").count()
        add("Notificações — não é stub", stub == 0)
        add("Notificações — página renderizou", page.locator("main").count() > 0)
        shot(page, "04_notificacoes")
        page.context.close()
    except Exception as e:
        add("Tela /notificacoes carrega", False, str(e)[:160])

    # ── 5. Agenda ─────────────────────────────────────────────
    print("\n[5/9] /agenda")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/agenda")
        page.wait_for_timeout(2000)
        stub = page.locator("text=em construção").count()
        add("Agenda — não é stub", stub == 0)
        itens = page.locator("main .divide-y > div").count()
        vazio = page.locator("text=Nenhuma O.S").count()
        add(f"Agenda — itens ou empty state ({itens})", itens > 0 or vazio > 0,
            "Nenhuma OS com prazo encontrada" if itens == 0 and vazio == 0 else "")
        shot(page, "05_agenda")
        page.context.close()
    except Exception as e:
        add("Tela /agenda carrega", False, str(e)[:160])

    # ── 6. Balanço ────────────────────────────────────────────
    print("\n[6/9] /balanco")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/balanco")
        page.wait_for_timeout(2000)
        stub = page.locator("text=em construção").count()
        add("Balanço — não é stub", stub == 0)
        nums = page.locator("main .text-2xl").all_text_contents()
        has_data = any(t.strip() not in ("", "—", "…") for t in nums)
        add("Balanço — números renderizados", has_data, str(nums[:4]))
        shot(page, "06_balanco")
        page.context.close()
    except Exception as e:
        add("Tela /balanco carrega", False, str(e)[:160])

    # ── 7. Equipe ─────────────────────────────────────────────
    print("\n[7/9] /equipe")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/equipe")
        page.wait_for_timeout(2000)
        stub = page.locator("text=em construção").count()
        add("Equipe — não é stub", stub == 0)
        membros = page.locator("main .divide-y > div").count()
        vazio = page.locator("text=Nenhum responsável").count()
        add(f"Equipe — {membros} responsáveis listados", membros > 0 or vazio > 0)
        shot(page, "07_equipe")
        page.context.close()
    except Exception as e:
        add("Tela /equipe carrega", False, str(e)[:160])

    # ── 8. Relatórios ─────────────────────────────────────────
    print("\n[8/9] /relatorios")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/relatorios")
        page.wait_for_timeout(3000)
        stub = page.locator("text=em construção").count()
        add("Relatórios — não é stub", stub == 0)
        linhas = page.locator("table tbody tr").count()
        add(f"Relatórios — {linhas} contratos na tabela", linhas > 0, "Tabela vazia" if linhas == 0 else "")
        shot(page, "08_relatorios")
        page.context.close()
    except Exception as e:
        add("Tela /relatorios carrega", False, str(e)[:160])

    # ── 9. Importar ───────────────────────────────────────────
    print("\n[9/9] /importar")
    try:
        page = make_page(browser)
        goto(page, BASE_URL + "/importar")
        drop = page.locator("input[type='file']").count()
        drop2 = page.locator("text=Arraste, text=arraste, text=upload, text=Upload").count()
        add("Importar — zona de upload visível", drop > 0 or drop2 > 0)
        shot(page, "09_importar")
        page.context.close()
    except Exception as e:
        add("Tela /importar carrega", False, str(e)[:160])

    # ── Console errors ────────────────────────────────────────
    print("\nAnalisando erros de console...")
    criticos = [
        e for e in console_errors
        if ("PAGEERROR" in e or "ERROR" in e)
        and not any(p in e for p in IGNORAR)
    ]
    if not criticos:
        add("Console — sem erros críticos", True)
    else:
        for err in criticos[:3]:
            add("Console ERROR detectado", False, err[:200])

    browser.close()
    return criticos

# ── Relatório HTML ────────────────────────────────────────────
def gerar_html():
    passed = sum(1 for r in results if r["passed"])
    total  = len(results)
    pct    = int(passed / total * 100) if total else 0
    ts     = datetime.now().strftime("%d/%m/%Y %H:%M")

    rows = ""
    for r in results:
        cor   = "#22c55e" if r["passed"] else "#ef4444"
        badge = "PASS" if r["passed"] else "FAIL"
        img   = ""
        if r["screenshot"] and Path(r["screenshot"]).exists():
            img = f'<br><img src="{r["screenshot"]}" style="max-width:500px;margin-top:6px;border-radius:6px;border:1px solid #334155">'
        det = f'<span style="color:#94a3b8;font-size:11px">{r["detail"]}</span>' if r["detail"] else ""
        rows += f"""
        <tr>
          <td style="padding:8px 12px;white-space:nowrap">
            <span style="background:{cor};color:#fff;border-radius:4px;padding:2px 8px;font-size:11px;font-weight:bold">{badge}</span>
          </td>
          <td style="padding:8px 12px;color:#e2e8f0">{r["name"]}</td>
          <td style="padding:8px 12px">{det}{img}</td>
        </tr>"""

    erros_html = "".join(
        f'<li style="color:#fca5a5;font-size:11px;font-family:monospace;margin-bottom:4px">{e[:250]}</li>'
        for e in console_errors[:15]
    )

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>TM-Testes — TM Gerenciador</title>
<style>
  body{{background:#0f172a;color:#e2e8f0;font-family:Inter,system-ui,sans-serif;padding:32px;max-width:1100px;margin:auto}}
  h1{{color:#f97316;margin-bottom:4px;font-size:22px}}
  .badge{{padding:4px 14px;border-radius:6px;font-weight:bold;font-size:13px}}
  table{{width:100%;border-collapse:collapse;margin-top:20px}}
  tr:hover td{{background:#1e293b}}
  th{{text-align:left;color:#64748b;padding:8px 12px;border-bottom:1px solid #1e293b;font-size:12px;text-transform:uppercase;letter-spacing:.06em}}
  td{{border-bottom:1px solid #1e293b;vertical-align:top}}
</style></head>
<body>
<h1>TM-Testes — TM Gerenciador</h1>
<p style="color:#64748b;font-size:13px;margin-bottom:24px">Gerado em {ts} · Next.js :3000 · FastAPI :8000</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">
  <span class="badge" style="background:#22c55e20;color:#22c55e">{passed} PASSOU</span>
  <span class="badge" style="background:#ef444420;color:#ef4444">{total-passed} FALHOU</span>
  <span class="badge" style="background:#3b82f620;color:#3b82f6">{pct}% aprovação</span>
</div>
<table>
  <tr><th>Status</th><th>Teste</th><th>Detalhe / Screenshot</th></tr>
  {rows}
</table>
{"<h3 style='color:#f97316;margin-top:32px;font-size:15px'>Erros de Console Capturados</h3><ul style='padding-left:16px'>" + erros_html + "</ul>" if erros_html else ""}
<p style="margin-top:32px;color:#334155;font-size:11px">Screenshots: {SHOTS_DIR}</p>
</body></html>"""

    REPORT.write_text(html, encoding="utf-8")
    print(f"\n  Relatório: {REPORT}")

# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  TM-TESTES — TM Gerenciador")
    print("  Next.js :3000  |  FastAPI :8000")
    print("=" * 60)

    with sync_playwright() as pw:
        criticos = run(pw)

    gerar_html()

    passed = sum(1 for r in results if r["passed"])
    total  = len(results)
    pct    = int(passed / total * 100) if total else 0

    print("\n" + "=" * 60)
    print(f"  TM-TESTES — RESULTADO FINAL")
    print(f"  {passed}/{total} testes passaram ({pct}%)")
    print("=" * 60)
    for r in results:
        s = "[PASS]" if r["passed"] else "[FAIL]"
        print(f"  {s} {r['name']}")
    print("=" * 60)
    print(f"  Relatório:   {REPORT}")
    print(f"  Screenshots: {SHOTS_DIR}/")
    print("=" * 60)
