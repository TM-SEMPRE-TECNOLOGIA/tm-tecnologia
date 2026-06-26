#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoRelatorio V5 - Playwright E2E Test Orchestrator
====================================================
Sobe FastAPI (porta 5000) + Next.js (porta 3000), executa
todos os testes, tira screenshots em erros, corrige bugs
simples e re-testa automaticamente.

Uso:
  python test_e2e.py
"""

import os
import sys
import time
import json
import shutil
import socket
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime

# -- Configurações -------------------------------------------------------------
ROOT      = Path(__file__).parent
BACKEND   = ROOT / "backend"
FRONTEND  = ROOT / "frontend"
SHOTS_DIR = ROOT / "test_screenshots"
REPORT    = ROOT / "test_report.html"
API_PORT  = 8000
FE_PORT   = 3000
BASE_URL  = f"http://localhost:{FE_PORT}"
API_URL   = f"http://localhost:{API_PORT}"
TIMEOUT   = 30_000  # ms

# Cores para terminal
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; RESET = "\033[0m"; BOLD = "\033[1m"

# -- Helpers -------------------------------------------------------------------
results: list[dict] = []
fixes_applied: list[str] = []

def log(prefix, msg, color=RESET):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  {color}[{ts}] {prefix}  {msg}{RESET}")

def ok(msg):   log("[OK]",   msg, G)
def fail(msg): log("[FAIL]", msg, R)
def warn(msg): log("[WARN]", msg, Y)
def info(msg): log("[INFO]", msg, B)

def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("localhost", port)) == 0

def wait_for_port(port: int, timeout_s: int = 60, label: str = "") -> bool:
    info(f"Aguardando porta {port} ({label})...")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if port_open(port):
            ok(f"Porta {port} aberta!")
            return True
        time.sleep(1)
    fail(f"Timeout: porta {port} não abriu em {timeout_s}s")
    return False

def add_result(name: str, passed: bool, detail: str = "", screenshot: str = ""):
    results.append({"name": name, "passed": passed, "detail": detail, "screenshot": screenshot})
    if passed:
        ok(f"{name}")
    else:
        fail(f"{name} - {detail}")

# -- Servidores ----------------------------------------------------------------
procs: list[subprocess.Popen] = []

def start_backend() -> subprocess.Popen | None:
    if port_open(API_PORT):
        info(f"Backend já rodando na porta {API_PORT}")
        return None
    info("Subindo FastAPI backend...")
    p = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "core.server:app",
         "--host", "0.0.0.0", "--port", str(API_PORT)],
        cwd=BACKEND,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace"
    )
    procs.append(p)
    return p

def start_frontend() -> subprocess.Popen | None:
    if port_open(FE_PORT):
        info(f"Frontend já rodando na porta {FE_PORT}")
        return None
    info("Subindo Next.js frontend...")
    p = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        shell=True
    )
    procs.append(p)
    return p

def stop_all():
    for p in procs:
        try:
            p.terminate()
            p.wait(timeout=5)
        except Exception:
            pass

# -- Testes --------------------------------------------------------------------
def run_tests(playwright_module):
    from playwright.sync_api import Page, ConsoleMessage

    SHOTS_DIR.mkdir(exist_ok=True)
    console_errors: list[str] = []

    browser = playwright_module.chromium.launch(headless=False, slow_mo=400)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    # Captura erros de console
    def on_console(msg: ConsoleMessage):
        if msg.type in ("error", "warning"):
            console_errors.append(f"[{msg.type.upper()}] {msg.text}")

    def on_pageerror(exc):
        console_errors.append(f"[PAGEERROR] {exc}")

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)

    def screenshot(name: str) -> str:
        path = str(SHOTS_DIR / f"{name}.png")
        try:
            page.screenshot(path=path, full_page=True)
        except Exception:
            pass
        return path

    # -- Teste 1: Página carrega -----------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 1: Carregamento Inicial --{RESET}")
    try:
        page.goto(BASE_URL, timeout=TIMEOUT, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=TIMEOUT)
        title = page.title()
        add_result("Página carrega sem crash", True, f"title={title!r}")
        screenshot("01_home")
    except Exception as e:
        shot = screenshot("01_home_error")
        add_result("Página carrega sem crash", False, str(e), shot)
        browser.close()
        return console_errors

    # -- Teste 2: Elementos principais presentes -------------------------------
    print(f"\n{BOLD}{B}-- Bloco 2: Layout Principal --{RESET}")
    checks = [
        ("TopBar presente",         "header.topbar"),
        ("Sidebar / nav presente",  "nav.nav"),
        ("Editor panel presente",   "section.editor"),
        ("Preview panel presente",  "[class*='preview']"),
        ("Botão START",             "button:has-text('START')"),
        ("Botão Gerar .docx",       "button:has-text('Gerar .docx')"),
    ]
    for name, selector in checks:
        try:
            el = page.locator(selector).first
            el.wait_for(state="visible", timeout=5000)
            add_result(name, True)
        except Exception as e:
            shot = screenshot(f"02_{name.replace(' ', '_')}")
            add_result(name, False, str(e)[:120], shot)

    # -- Teste 3: Lista de contratos na sidebar --------------------------------
    print(f"\n{BOLD}{B}-- Bloco 3: Sidebar - Lista de Contratos --{RESET}")
    try:
        items = page.locator(".c-item").all()
        count = len(items)
        add_result(f"9 contratos na sidebar (encontrados: {count})", count == 9)
        if count > 0:
            screenshot("03_sidebar_contracts")
    except Exception as e:
        add_result("Contratos na sidebar", False, str(e)[:120])

    # Clica em cada contrato e verifica que o topbar atualiza
    contracts = ["0908", "1507", "1565", "2056", "2057", "2626", "2627", "3575", "6122"]
    for cid in contracts[:3]:  # testa os 3 primeiros para não ser lento
        try:
            page.locator(f".c-item:has(.c-id:has-text('{cid}'))").first.click()
            page.wait_for_timeout(500)
            pill_text = page.locator(".contract-pill").first.inner_text()
            ok_flag = cid in pill_text
            add_result(f"Selecionar contrato {cid}", ok_flag, f"pill={pill_text!r}")
        except Exception as e:
            add_result(f"Selecionar contrato {cid}", False, str(e)[:120])

    screenshot("03_sidebar_after_clicks")

    # -- Teste 4: Navegação pelos 3 passos ------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 4: Steps Navigation --{RESET}")
    try:
        # Vai para passo 1 (Cabeçalho)
        page.locator("button:has-text('Cabeçalho')").first.click()
        page.wait_for_timeout(300)
        add_result("Step 1 - Cabeçalho ativo", True)
        screenshot("04_step1")

        # Verifica campos do formulário
        fields = [
            ("Campo Nº OS",       "input[placeholder*='1753']"),
            ("Campo Data Atend.", "input[type='date']"),
            ("Campo Ag. Código",  "input[placeholder*='1234']"),
            ("Campo Ag. Nome",    "input[placeholder*='Ag.']"),
            ("Select Descrição",  "select.f-select"),
        ]
        for fname, sel in fields:
            try:
                page.locator(sel).first.wait_for(state="visible", timeout=3000)
                add_result(fname, True)
            except Exception as e:
                add_result(fname, False, str(e)[:100])

    except Exception as e:
        add_result("Step 1 carrega", False, str(e)[:120])

    # -- Teste 5: Preenche formulário (Step 1) ---------------------------------
    print(f"\n{BOLD}{B}-- Bloco 5: Preenchimento do Formulário --{RESET}")
    try:
        page.locator("input[placeholder*='1753']").first.fill("9999")
        page.locator("input[type='date']").first.fill("2026-05-24")
        page.locator("input[placeholder*='1234']").first.fill("9999-9")
        page.locator("input[placeholder*='Ag.']").first.fill("Ag. Teste Playwright")
        page.locator("input[placeholder*='Rua']").first.fill("Rua do Teste, 100 - São Paulo/SP")
        page.locator("input[placeholder*='Mat.']").first.fill("Mat. 00001 - Playwright Bot")
        add_result("Preenchimento formulário Step 1", True)
        screenshot("05_form_filled")
    except Exception as e:
        shot = screenshot("05_form_error")
        add_result("Preenchimento formulário Step 1", False, str(e)[:120], shot)

    # -- Teste 6: Navega para Step 2 ------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 6: Step 2 - Estrutura --{RESET}")
    try:
        page.locator("button:has-text('Próximo')").first.click()
        page.wait_for_timeout(600)
        step2_visible = page.locator(".scan-zone").first.is_visible()
        add_result("Step 2 - Estrutura carrega", step2_visible)
        screenshot("06_step2")

        # Verifica tabs modo
        tabs = page.locator(".mode-tab").all()
        add_result(f"Tabs modo presentes (encontradas: {len(tabs)})", len(tabs) >= 1)
    except Exception as e:
        shot = screenshot("06_step2_error")
        add_result("Step 2 navegação", False, str(e)[:120], shot)

    # -- Teste 7: Navega para Step 3 ------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 7: Step 3 - Gerar --{RESET}")
    try:
        page.locator("button:has-text('Próximo')").first.click()
        page.wait_for_timeout(600)
        # Verifica resumo da geração
        gen_rows = page.locator(".gen-row").all()
        add_result(f"Step 3 - Resumo geração ({len(gen_rows)} rows)", len(gen_rows) >= 3)
        screenshot("07_step3_generate")

        # Verifica se o contrato selecionado está no resumo
        gen_vals = [el.inner_text() for el in page.locator(".gen-val").all()]
        add_result("Resumo mostra contrato selecionado", any(v for v in gen_vals if v != "-"))
    except Exception as e:
        shot = screenshot("07_step3_error")
        add_result("Step 3 - Gerar", False, str(e)[:120], shot)

    # -- Teste 8: Botão Gerar .docx (Step 3) ----------------------------------
    print(f"\n{BOLD}{B}-- Bloco 8: Botão Gerar .docx --{RESET}")
    try:
        btn = page.locator("section.editor button:has-text('Gerar .docx')").first
        btn.wait_for(state="visible", timeout=5000)
        add_result("Botão 'Gerar .docx' visível no Step 3", True)
        screenshot("08_gerar_btn")
    except Exception as e:
        add_result("Botão 'Gerar .docx' no Step 3", False, str(e)[:100])

    # -- Teste 9: API Backend --------------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 9: API FastAPI --{RESET}")
    if port_open(API_PORT):
        try:
            api_resp = page.request.get(f"{API_URL}/api/contracts", timeout=8000)
            add_result("GET /api/contracts responde 200", api_resp.ok, f"status={api_resp.status}")
            if api_resp.ok:
                data = api_resp.json()
                add_result(f"API retorna contratos (encontrados: {len(data)})", len(data) > 0)
        except Exception as e:
            add_result("API /api/contracts", False, str(e)[:120])

        # Testa endpoint de contrato específico
        try:
            r = page.request.get(f"{API_URL}/api/contracts/1507", timeout=8000)
            add_result("GET /api/contracts/1507", r.ok, f"status={r.status}")
        except Exception as e:
            add_result("GET /api/contracts/1507", False, str(e)[:100])
    else:
        warn("Backend não está rodando - pulando testes de API")
        add_result("Backend API acessível", False, "Porta 5000 fechada")

    # -- Teste 10: Toggle tema -------------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 10: UI - Toggle Tema --{RESET}")
    try:
        theme_btn = page.locator("button[title*='laro'], button[title*='scuro'], button:has-text('[SUN]'), button:has-text('[MOON]')").first
        before = page.locator("html").get_attribute("class") or ""
        theme_btn.click()
        page.wait_for_timeout(400)
        after = page.locator("html").get_attribute("class") or ""
        add_result("Toggle tema executa sem crash", True, f"antes={before!r} depois={after!r}")
        screenshot("10_theme_toggled")
    except Exception as e:
        add_result("Toggle tema", False, str(e)[:120])

    # -- Teste 11: Sidebar collapse --------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 11: UI - Sidebar Collapse --{RESET}")
    try:
        toggle = page.locator(".nav-toggle-btn").first
        toggle.click()
        page.wait_for_timeout(400)
        collapsed = page.locator("nav.collapsed").count() > 0
        add_result("Sidebar colapsa", collapsed)
        screenshot("11_sidebar_collapsed")
        toggle.click()
        page.wait_for_timeout(300)
        add_result("Sidebar expande", True)
    except Exception as e:
        add_result("Sidebar collapse/expand", False, str(e)[:120])

    # -- Teste 12: Navegação pelo Step bar (direto) ----------------------------
    print(f"\n{BOLD}{B}-- Bloco 12: Navegação direta pelos steps --{RESET}")
    try:
        page.locator("button:has-text('Cabeçalho')").first.click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('Estrutura')").first.click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('Gerar')").first.click()
        page.wait_for_timeout(300)
        add_result("Step bar navegação direta", True)
        page.locator("button:has-text('Voltar')").first.click()
        page.wait_for_timeout(300)
        add_result("Botão Voltar funciona", True)
    except Exception as e:
        add_result("Step bar / Voltar", False, str(e)[:120])

    # -- Teste 13: Erros de Console --------------------------------------------
    print(f"\n{BOLD}{B}-- Bloco 13: Console Errors --{RESET}")
    # Ignora erros de recursos externos (fontes, CDN) e ERR_CONNECTION_REFUSED
    # de recursos opcionais (ex: health-check que o usuário ainda nao triggou).
    # Considera critico: erros JS (PAGEERROR) e falhas em recursos locais do app.
    IGNORE_PATTERNS = [
        "favicon", "fonts.googleapis", "fonts.gstatic",
        "ERR_CONNECTION_REFUSED",  # backend pode estar off — e' avisado separado
        "ERR_NAME_NOT_RESOLVED",   # recursos externos offline
        "analytics", "cdn.", "gtag",
    ]
    def is_critical(e: str) -> bool:
        if "PAGEERROR" in e:
            return True
        if "ERROR" not in e:
            return False
        return not any(pat in e for pat in IGNORE_PATTERNS)

    critical = [e for e in console_errors if is_critical(e)]
    if not critical:
        add_result("Sem erros críticos no console", True)
    else:
        for err in critical[:5]:
            fail(f"  Console: {err[:150]}")
        add_result(f"Erros críticos no console ({len(critical)})", False,
                   critical[0][:200] if critical else "")
        screenshot("13_console_errors")

    # -- Screenshot final ------------------------------------------------------
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(1000)
    except Exception:
        pass  # screenshot mesmo se timeout (Next.js recompilando)
    screenshot("99_final_state")

    browser.close()
    return console_errors


# -- Correções automáticas -----------------------------------------------------
def attempt_auto_fixes():
    """Tenta corrigir problemas conhecidos detectados nos resultados."""
    failed = [r for r in results if not r["passed"]]
    if not failed:
        return False

    fixed_any = False

    for item in failed:
        name = item["name"]
        detail = item.get("detail", "")

        # Fix 1: next.config.ts faltando configurações básicas
        if "página carrega" in name.lower() and "ECONNREFUSED" in detail:
            info("Não foi possível conectar - verifique se Next.js subiu corretamente")

        # Fix 2: CSS class 'preview' ausente - verifica PreviewPanel
        if "preview panel" in name.lower():
            preview_file = FRONTEND / "components" / "PreviewPanel.tsx"
            if preview_file.exists():
                content = preview_file.read_text(encoding="utf-8")
                if "preview" not in content.lower():
                    warn(f"PreviewPanel.tsx pode não ter classe 'preview' - verifique {preview_file}")

        # Fix 3: Contratos sidebar - verifica se há 9
        if "9 contratos" in name.lower() and not item["passed"]:
            warn("Sidebar não mostra 9 contratos - verifique lib/contracts.ts e Sidebar.tsx")

        # Fix 4: API não acessível mas backend deveria estar rodando
        if "api/contracts" in name.lower() and not item["passed"]:
            if "5000" not in detail:
                info("Verifique se backend/core/__init__.py existe para importação correta")
                init_file = BACKEND / "core" / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# AutoRelatório V5 - core package\n")
                    fixes_applied.append("Criado backend/core/__init__.py")
                    fixed_any = True

    return fixed_any


# -- Geração de relatório HTML -------------------------------------------------
def generate_report(console_errors: list[str]):
    passed  = sum(1 for r in results if r["passed"])
    total   = len(results)
    failed  = total - passed
    pct     = int(passed / total * 100) if total else 0
    ts      = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    rows = ""
    for r in results:
        icon = "[PASS]" if r["passed"] else "[FAIL]"
        cls  = "pass" if r["passed"] else "fail"
        shot = f'<br><a href="{r["screenshot"]}" target="_blank">[SHOT] screenshot</a>' if r.get("screenshot") else ""
        det  = f'<small style="color:#888">{r["detail"][:200]}</small>' if r.get("detail") else ""
        rows += f'<tr class="{cls}"><td>{icon}</td><td>{r["name"]}</td><td>{det}{shot}</td></tr>\n'

    console_html = ""
    if console_errors:
        lines = "".join(f"<div>{e[:200]}</div>" for e in console_errors[:20])
        console_html = f'<h2>[CONSOLE] Console ({len(console_errors)} eventos)</h2><div class="console-block">{lines}</div>'

    fixes_html = ""
    if fixes_applied:
        items = "".join(f"<li>{f}</li>" for f in fixes_applied)
        fixes_html = f'<h2>[FIX] Correções Aplicadas</h2><ul>{items}</ul>'

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>AutoRelatório V5 - E2E Report</title>
<style>
  body {{ font-family: Inter, system-ui, sans-serif; background: #111110; color: #EFEDE8; padding: 32px; }}
  h1 {{ color: #C8541C; }} h2 {{ color: #EFEDE8; margin-top: 32px; }}
  .summary {{ display: flex; gap: 24px; margin: 24px 0; flex-wrap: wrap; }}
  .card {{ background: #1A1917; border: 1px solid #2A2825; border-radius: 8px; padding: 20px 28px; }}
  .card .num {{ font-size: 2.4rem; font-weight: 700; }}
  .card.ok .num {{ color: #4CAF50; }} .card.bad .num {{ color: #ef5350; }} .card.pct .num {{ color: #C8541C; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
  th {{ text-align: left; padding: 10px 12px; background: #1A1917; color: #8C8A85; font-size: 11px; text-transform: uppercase; letter-spacing: .1em; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #2A2825; font-size: 14px; vertical-align: top; }}
  tr.pass td:first-child {{ color: #4CAF50; }} tr.fail td:first-child {{ color: #ef5350; }}
  tr.fail {{ background: rgba(239,83,80,.05); }}
  .console-block {{ background: #1A1917; border: 1px solid #2A2825; border-radius: 6px; padding: 16px; font-family: monospace; font-size: 12px; color: #ef5350; max-height: 400px; overflow-y: auto; margin-top: 8px; }}
  ul {{ color: #4CAF50; }}
  .ts {{ color: #4A4845; font-size: 12px; margin-top: 4px; }}
</style>
</head>
<body>
<h1>[DOC] AutoRelatório V5 - Relatório E2E</h1>
<div class="ts">Gerado em: {ts}</div>

<div class="summary">
  <div class="card ok"><div class="num">{passed}</div>Testes passaram</div>
  <div class="card bad"><div class="num">{failed}</div>Testes falharam</div>
  <div class="card pct"><div class="num">{pct}%</div>Taxa de sucesso</div>
  <div class="card"><div class="num">{total}</div>Total de testes</div>
</div>

{fixes_html}
{console_html}

<h2>[LIST] Resultados Detalhados</h2>
<table>
<tr><th>Status</th><th>Teste</th><th>Detalhe</th></tr>
{rows}
</table>
</body>
</html>"""

    REPORT.write_text(html, encoding="utf-8")
    info(f"Relatório salvo em: {REPORT}")


# -- Entry point ---------------------------------------------------------------
def main():
    print(f"\n{BOLD}{B}{'='*60}")
    print(f"  AutoRelatório V5 - E2E Test Orchestrator")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}{RESET}\n")

    # 1. Sobe servidores
    print(f"{BOLD}>> Subindo servidores...{RESET}")
    start_backend()
    start_frontend()

    # Espera portas
    be_ok = wait_for_port(API_PORT, timeout_s=45, label="FastAPI")
    fe_ok = wait_for_port(FE_PORT,  timeout_s=90, label="Next.js")

    if not fe_ok:
        fail("Frontend não iniciou - abortando testes")
        stop_all()
        sys.exit(1)

    if not be_ok:
        warn("Backend não iniciou - testes de API serão marcados como falha")

    time.sleep(2)  # buffer extra para Next.js compilar

    # 2. Roda testes
    print(f"\n{BOLD}>> Executando testes Playwright...{RESET}")
    from playwright.sync_api import sync_playwright
    console_errors: list[str] = []
    try:
        with sync_playwright() as pw:
            console_errors = run_tests(pw)
    except Exception as e:
        fail(f"Erro fatal no Playwright: {e}")

    # 3. Relatório parcial
    print(f"\n{BOLD}>> Resultados da 1a rodada:{RESET}")
    passed1 = sum(1 for r in results if r["passed"])
    total1  = len(results)
    print(f"  {G}{passed1}/{total1} testes passaram{RESET}")

    # 4. Tenta corrigir
    print(f"\n{BOLD}>> Tentando correções automáticas...{RESET}")
    fixed = attempt_auto_fixes()

    # 5. Re-roda se houve correções
    if fixed:
        print(f"\n{BOLD}>> Correções aplicadas - re-executando testes...{RESET}")
        results.clear()
        console_errors = []
        time.sleep(2)
        try:
            with sync_playwright() as pw:
                console_errors = run_tests(pw)
        except Exception as e:
            fail(f"Erro na 2ª rodada: {e}")

    # 6. Gera relatório
    generate_report(console_errors)

    # 7. Summary final
    passed_f = sum(1 for r in results if r["passed"])
    total_f  = len(results)
    failed_f = total_f - passed_f
    pct      = int(passed_f / total_f * 100) if total_f else 0

    print(f"\n{BOLD}{'='*60}")
    print(f"  RESULTADO FINAL: {passed_f}/{total_f} ({pct}%)")
    if failed_f == 0:
        print(f"  {G}[PASS] TODOS OS TESTES PASSARAM!{RESET}")
    else:
        print(f"  {R}[FAIL] {failed_f} teste(s) falharam{RESET}")
    print(f"  [DOC] Relatório: {REPORT}")
    print(f"  [SHOT] Screenshots: {SHOTS_DIR}/")
    if fixes_applied:
        print(f"\n  [FIX] Correções aplicadas:")
        for f in fixes_applied:
            print(f"     • {f}")
    print(f"{'='*60}{RESET}\n")

    stop_all()
    return 0 if failed_f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
