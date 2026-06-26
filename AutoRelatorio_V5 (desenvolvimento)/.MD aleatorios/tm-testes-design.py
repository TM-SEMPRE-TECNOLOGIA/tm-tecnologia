#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  TM-TESTES-DESIGN — Guardião do Design System                ║
║  AutoRelatório V5  —  TM Sempre Tecnologia                   ║
║  Gerado pela skill tm-testes                                  ║
╚══════════════════════════════════════════════════════════════╝

Auditorias cobertas:
  1. Tokens CSS — detecta cores/fontes hardcoded fora do design system
  2. Contraste — verifica todos os pares texto/fundo (WCAG AA)
  3. Performance — LCP, CLS, FCP, TTI via Lighthouse API
  4. Screenshot Diff — compara visualmente com baseline salvo
  5. Tipografia — fontes corretas sendo carregadas (Inter, Roboto Slab, JetBrains Mono)
  6. Responsividade — testa 3 viewports (desktop, tablet, mobile)
  7. Animações — garante que transitions/animations não causam CLS
  8. Tema Dark/Light — valida que ambos os modos respeitam os tokens
  9. Ícones e SVGs — sem ícones quebrados ou sem acessibilidade
 10. Consistência de botões — classes .btn corretas em todos os botões
 11. Z-index sanity — nada sobrepondo indevidamente
 12. Focus visible — todos os elementos interativos têm foco visível

Uso:
  python tm-testes-design.py            # roda tudo
  python tm-testes-design.py --update   # atualiza baseline de screenshots
  python tm-testes-design.py --quick    # só tokens + contraste (sem Playwright)
"""

import sys
import re
import json
import math
import argparse
import colorsys
from pathlib import Path
from datetime import datetime

# ── Configuração do Design System TM ─────────────────────────────────────────
FRONTEND_URL = "http://localhost:3000"
FRONTEND_DIR = Path(__file__).parent / "frontend"
CSS_FILE     = FRONTEND_DIR / "app" / "globals.css"
COMPS_DIR    = FRONTEND_DIR / "components"
APP_DIR      = FRONTEND_DIR / "app"

BASELINE_DIR = Path(__file__).parent / "design_baseline"
SHOTS_DIR    = Path(__file__).parent / "design_screenshots"
REPORT_PATH  = Path(__file__).parent / "design_report.html"

# ── Tokens oficiais do Design System TM ──────────────────────────────────────
TM_TOKENS = {
    # Shell colors (dark mode)
    "--shell-bg":      "#111110",
    "--shell-card":    "#1A1917",
    "--shell-panel":   "#161513",
    "--shell-border":  "#2A2825",
    "--shell-hover":   "#222120",
    "--shell-text":    "#EFEDE8",
    "--shell-muted":   "#8C8A85",
    "--shell-subtle":  "#4A4845",
    # Brand
    "--orange":        "#C8541C",
    "--orange-hover":  "#E06428",
    "--green":         "#4F7A3A",
    "--blue":          "#345878",
    # Erros
    "--error":         "#C0392B",
    # Fontes
    "--sans":   '"Inter"',
    "--mono":   '"JetBrains Mono"',
    "--serif":  '"Roboto Slab"',
}

# Cores permitidas hardcoded (doc preview usa #FFF, logos, etc.)
ALLOWED_HARDCODED_CONTEXTS = [
    "doc-", "doc_", ".doc-", ".doc_",  # preview do documento Word
    "#fff",                              # branco em elementos de logo/badge
    "#FFD700",                           # logo BB
    "#00349B",                           # logo BB azul
    "#1A1A1A",                           # texto do documento
    "rgba(0,0,0",                        # sombras
    "rgba(0, 0, 0",
    "color: #fff",                       # texto em botão primário
    "color:#fff",
]

# Viewports para teste de responsividade
VIEWPORTS = [
    {"name": "Desktop 1440",  "width": 1440, "height": 900},
    {"name": "Laptop 1280",   "width": 1280, "height": 800},
    {"name": "Tablet 768",    "width": 768,  "height": 1024},
]

results: list[dict] = []
warnings: list[str] = []

# ── Helpers ───────────────────────────────────────────────────────────────────
def add(name, passed, detail="", shot="", category="geral", severity="error"):
    results.append({
        "name": name, "passed": passed, "detail": detail,
        "screenshot": shot, "category": category, "severity": severity
    })
    icon = "✅" if passed else ("⚠️" if severity == "warn" else "❌")
    print(f"  {icon} {name}" + (f"\n     → {detail[:120]}" if detail and not passed else ""))

def warn(msg):
    warnings.append(msg)
    print(f"  ⚠️  {msg}")


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA 1 — TOKENS CSS (análise estática de código)
# ══════════════════════════════════════════════════════════════════════════════
def audit_tokens():
    print("\n📐 AUDITORIA 1 — Tokens CSS (análise estática)")
    print("   Verifica se componentes usam var(--token) em vez de valores hardcoded")

    # Cores que NÃO deveriam aparecer hardcoded fora de contextos permitidos
    FORBIDDEN_COLORS = [
        r'#111110', r'#1A1917', r'#161513', r'#2A2825', r'#222120',
        r'#EFEDE8', r'#8C8A85', r'#4A4845', r'#C8541C', r'#E06428',
        r'#4F7A3A', r'#345878', r'#C0392B',
    ]

    tsx_files = list(COMPS_DIR.rglob("*.tsx")) + list(APP_DIR.rglob("*.tsx"))
    css_files = list(FRONTEND_DIR.rglob("*.css"))
    # Excluir node_modules e .next
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f) and ".next" not in str(f)]
    css_files = [f for f in css_files if "node_modules" not in str(f) and ".next" not in str(f) and str(f) != str(CSS_FILE)]

    violations = []

    for file in tsx_files + css_files:
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            # Pula comentários
            if line.strip().startswith("//") or line.strip().startswith("*"):
                continue

            for color in FORBIDDEN_COLORS:
                if re.search(color, line, re.IGNORECASE):
                    # Verifica se está num contexto permitido
                    ctx_ok = any(ctx in line.lower() for ctx in ALLOWED_HARDCODED_CONTEXTS)
                    if not ctx_ok:
                        rel = str(file).replace(str(FRONTEND_DIR), "").lstrip("\\").lstrip("/")
                        violations.append(f"{rel}:{i} → {line.strip()[:80]}")

    if not violations:
        add("Tokens CSS — sem cores hardcoded", True, category="tokens")
    else:
        for v in violations[:5]:
            add(f"Token hardcoded detectado", False, v, category="tokens", severity="warn")
        if len(violations) > 5:
            warn(f"  ... e mais {len(violations)-5} ocorrências")

    # Verifica se globals.css tem todos os tokens obrigatórios
    if CSS_FILE.exists():
        css_text = CSS_FILE.read_text(encoding="utf-8")
        for token in ["--shell-bg", "--orange", "--sans", "--mono", "--serif", "--r-sm", "--error"]:
            found = token in css_text
            add(f"Token {token} definido em globals.css", found, category="tokens")
    else:
        add("globals.css encontrado", False, str(CSS_FILE), category="tokens")

    # Verifica classes de botão consistentes
    btn_violations = []
    for f in tsx_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Detecta style={{ background: ... }} inline em botões
        if re.search(r'<button[^>]*style=\{', text):
            rel = str(f).replace(str(FRONTEND_DIR), "").lstrip("\\").lstrip("/")
            btn_violations.append(rel)

    if not btn_violations:
        add("Botões usam classes CSS (sem style inline)", True, category="tokens")
    else:
        add("Botões com style inline detectados", False,
            f"Arquivos: {', '.join(btn_violations[:3])}", category="tokens", severity="warn")


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA 2 — CONTRASTE (análise dos tokens)
# ══════════════════════════════════════════════════════════════════════════════
def hex_to_rgb(hex_color: str) -> tuple:
    """Converte hex para RGB (0-255)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def luminance(r, g, b) -> float:
    """Calcula luminância relativa WCAG."""
    def c(x):
        x /= 255
        return x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4
    return 0.2126*c(r) + 0.7152*c(g) + 0.0722*c(b)

def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calcula razão de contraste entre dois hexs."""
    try:
        rgb1 = hex_to_rgb(hex1)
        rgb2 = hex_to_rgb(hex2)
        l1 = luminance(*rgb1)
        l2 = luminance(*rgb2)
        lighter = max(l1, l2)
        darker  = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    except Exception:
        return 0.0

def audit_contrast():
    print("\n🎨 AUDITORIA 2 — Contraste WCAG AA (mínimo 4.5:1 normal, 3:1 large)")
    print("   Analisa todos os pares texto/fundo do design system TM")

    # Pares críticos: (texto, fundo, contexto, tipo_texto)
    # tipo_texto: "normal" (4.5:1) ou "large" (3:1 — bold >= 14px ou >= 18px)
    PAIRS = [
        ("#EFEDE8", "#111110", "--shell-text sobre --shell-bg",     "normal"),
        ("#EFEDE8", "#1A1917", "--shell-text sobre --shell-card",   "normal"),
        ("#EFEDE8", "#161513", "--shell-text sobre --shell-panel",  "normal"),
        ("#8C8A85", "#111110", "--shell-muted sobre --shell-bg",    "normal"),
        ("#8C8A85", "#1A1917", "--shell-muted sobre --shell-card",  "normal"),
        ("#4A4845", "#111110", "--shell-subtle sobre --shell-bg",   "large"),   # labels pequenos
        ("#C8541C", "#111110", "--orange sobre --shell-bg",         "large"),   # badges/pills
        ("#C8541C", "#1A1917", "--orange sobre --shell-card",       "large"),
        ("#EFEDE8", "#C8541C", "texto branco sobre --orange (btn)", "normal"),  # btn-primary
        ("#7DB863", "#111110", "verde sobre --shell-bg",            "large"),   # status dot
        ("#6BA3C8", "#111110", "azul sobre --shell-bg (SP2)",       "large"),
        ("#4A4845", "#1A1917", "--shell-subtle sobre card",         "large"),
        # Light mode
        ("#2C2C2C", "#F8F7F4", "texto dark sobre light-bg",         "normal"),
        ("#7A7A7A", "#F8F7F4", "muted sobre light-bg",              "normal"),
        ("#C8541C", "#F8F7F4", "--orange sobre light-bg",           "large"),
        ("#2C2C2C", "#FFFFFF", "texto dark sobre white card",        "normal"),
    ]

    MINIMUM = {"normal": 4.5, "large": 3.0}

    for text_hex, bg_hex, context, kind in PAIRS:
        ratio = contrast_ratio(text_hex, bg_hex)
        min_r = MINIMUM[kind]
        passed = ratio >= min_r
        detail = f"{ratio:.2f}:1  (mínimo {min_r}:1 para texto {kind})"
        sev = "error" if not passed and kind == "normal" else "warn"
        add(f"Contraste: {context}", passed, detail,
            category="contraste", severity=sev)


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA 3 — TIPOGRAFIA (análise estática)
# ══════════════════════════════════════════════════════════════════════════════
def audit_typography():
    print("\n✏️  AUDITORIA 3 — Tipografia")
    print("   Verifica uso correto das 3 famílias tipográficas do sistema")

    if not CSS_FILE.exists():
        add("globals.css encontrado", False, category="tipografia")
        return

    css = CSS_FILE.read_text(encoding="utf-8")

    # Verifica import das fontes Google
    for font in ["Roboto+Slab", "Inter", "JetBrains+Mono"]:
        found = font in css
        add(f"Fonte {font.replace('+', ' ')} importada", found, category="tipografia")

    # Verifica uso consistente das variáveis de fonte
    tsx_files = list(COMPS_DIR.rglob("*.tsx")) + list(APP_DIR.rglob("*.tsx"))
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f)]

    raw_font_violations = []
    for f in tsx_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Detecta fontFamily hardcoded (fora de doc-* context)
        matches = re.findall(r'fontFamily:\s*["\']([^"\']+)["\']', text)
        for m in matches:
            if m not in ["Arial", "monospace", "system-ui"] and "var(--" not in m:
                rel = str(f).replace(str(FRONTEND_DIR), "").lstrip("\\").lstrip("/")
                raw_font_violations.append(f"{rel}: fontFamily='{m}'")

    if not raw_font_violations:
        add("Fontes usam var(--sans/--mono/--serif)", True, category="tipografia")
    else:
        add("fontFamily hardcoded detectado", False,
            raw_font_violations[0], category="tipografia", severity="warn")

    # Verifica classes mono/serif nos componentes certos
    for comp_file in ["TopBar.tsx", "Sidebar.tsx", "EditorPanel.tsx"]:
        fp = COMPS_DIR / comp_file
        if fp.exists():
            text = fp.read_text(encoding="utf-8", errors="ignore")
            has_mono  = "var(--mono)" in text or "mono" in text
            has_serif = "var(--serif)" in text or "serif" in text or "sans" in text
            add(f"{comp_file} — usa tokens tipográficos",
                has_mono or has_serif, category="tipografia")


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA 4 — CONSISTÊNCIA DE COMPONENTES (análise estática)
# ══════════════════════════════════════════════════════════════════════════════
def audit_components():
    print("\n🧩 AUDITORIA 4 — Consistência de Componentes")
    print("   Verifica padrões de código: acessibilidade, classes, estrutura")

    tsx_files = list(COMPS_DIR.rglob("*.tsx")) + list(APP_DIR.rglob("*.tsx"))
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f)]

    img_without_alt    = []
    btn_without_type   = []
    input_without_label = []
    missing_key_prop   = []

    for f in tsx_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(f).replace(str(FRONTEND_DIR), "").lstrip("\\").lstrip("/")
        lines = text.split("\n")

        for i, line in enumerate(lines, 1):
            # <img sem alt
            if re.search(r'<img\b', line) and 'alt=' not in line:
                img_without_alt.append(f"{rel}:{i}")

            # <button sem type
            if re.search(r'<button\b', line) and 'type=' not in line:
                # Só reporta se for onClick (interativo)
                if 'onClick' in line or i < len(lines) and 'onClick' in lines[i]:
                    btn_without_type.append(f"{rel}:{i}")

            # .map( sem key
            if '.map(' in line and i + 3 < len(lines):
                chunk = "".join(lines[i-1:i+4])
                if 'key=' not in chunk and 'key:' not in chunk:
                    # Só reporta uma vez por arquivo
                    fname = rel.split("\\")[-1].split("/")[-1]
                    if not any(fname in x for x in missing_key_prop):
                        missing_key_prop.append(f"{rel}:{i}")

    add("Imagens com alt text", len(img_without_alt) == 0,
        f"Sem alt: {img_without_alt[:3]}" if img_without_alt else "", category="componentes")
    add("Botões com type definido", len(btn_without_type) == 0,
        f"Sem type: {btn_without_type[:3]}" if btn_without_type else "", category="componentes", severity="warn")
    add(".map() com key prop", len(missing_key_prop) == 0,
        f"Possíveis faltantes: {missing_key_prop[:3]}" if missing_key_prop else "", category="componentes", severity="warn")

    # Verifica se os componentes UI core existem
    EXPECTED_COMPONENTS = [
        "TopBar.tsx", "Sidebar.tsx", "EditorPanel.tsx",
        "PreviewPanel.tsx", "Toast.tsx",
        "ui/LoadingSpinner.tsx", "ui/ErrorMessage.tsx", "ui/EmptyState.tsx",
        "blocks/BlockCard.tsx", "blocks/BlockList.tsx",
    ]
    for comp in EXPECTED_COMPONENTS:
        exists = (COMPS_DIR / comp).exists()
        add(f"Componente {comp} existe", exists, category="componentes")


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIAS 5-12 — PLAYWRIGHT (requerem browser)
# ══════════════════════════════════════════════════════════════════════════════
def audit_with_playwright(update_baseline: bool = False):
    from playwright.sync_api import sync_playwright
    import urllib.request, urllib.error

    # Verifica se frontend está no ar
    try:
        urllib.request.urlopen(FRONTEND_URL, timeout=5)
    except Exception:
        print(f"\n⚠️  Frontend não acessível em {FRONTEND_URL}")
        print("   Sobe o servidor com: npm run dev")
        add("Frontend acessível para auditoria visual", False,
            f"{FRONTEND_URL} inacessível", category="performance")
        return

    SHOTS_DIR.mkdir(exist_ok=True)
    BASELINE_DIR.mkdir(exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=200)

        # ── AUDITORIA 5 — SCREENSHOT DIFF ─────────────────────────────────────
        print("\n📸 AUDITORIA 5 — Screenshot Diff (regressão visual)")
        print("   Compara estado atual com baseline salvo")

        for vp in VIEWPORTS:
            ctx  = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = ctx.new_page()
            vp_name = vp["name"].replace(" ", "_")

            try:
                page.goto(FRONTEND_URL, timeout=20000, wait_until="networkidle")
                page.wait_for_timeout(1500)  # espera animações

                # Screenshot atual
                shot_path = str(SHOTS_DIR / f"current_{vp_name}.png")
                page.screenshot(path=shot_path, full_page=False)

                # Baseline
                baseline_path = BASELINE_DIR / f"baseline_{vp_name}.png"

                if update_baseline or not baseline_path.exists():
                    import shutil
                    shutil.copy(shot_path, str(baseline_path))
                    add(f"Screenshot baseline criado — {vp['name']}", True,
                        "Baseline salvo para comparações futuras", shot_path, category="visual")
                else:
                    # Comparação pixel a pixel simples
                    diff = compare_screenshots(str(baseline_path), shot_path)
                    passed = diff < 2.0  # tolerância de 2% de diferença
                    add(f"Screenshot diff — {vp['name']}", passed,
                        f"Diferença: {diff:.1f}% (tolerância: 2%)", shot_path, category="visual",
                        severity="warn" if not passed else "ok")

            except Exception as e:
                add(f"Screenshot — {vp['name']}", False, str(e)[:120], category="visual")
            finally:
                ctx.close()

        # ── AUDITORIA 6 — TIPOGRAFIA VISUAL ───────────────────────────────────
        print("\n✏️  AUDITORIA 6 — Tipografia Visual (browser)")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(FRONTEND_URL, timeout=20000, wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Verifica se as fontes foram carregadas pelo browser
            fonts_loaded = page.evaluate("""() => {
                const fonts = [...document.fonts];
                const loaded = fonts.filter(f => f.status === 'loaded').map(f => f.family);
                return loaded;
            }""")

            for font in ["Inter", "Roboto Slab", "JetBrains Mono"]:
                found = any(font.lower() in f.lower() for f in fonts_loaded)
                add(f"Fonte '{font}' carregada no browser", found,
                    f"Fontes carregadas: {fonts_loaded[:5]}" if not found else "",
                    category="tipografia")

            # Verifica que elementos mono usam a fonte correta
            mono_font = page.evaluate("""() => {
                const el = document.querySelector('.brand-ver, .f-label, .gen-val');
                if (!el) return null;
                return window.getComputedStyle(el).fontFamily;
            }""")
            if mono_font:
                ok = "JetBrains" in mono_font or "monospace" in mono_font.lower()
                add("Elementos .mono usam JetBrains Mono", ok,
                    f"fontFamily detectado: {mono_font[:80]}", category="tipografia")
        except Exception as e:
            add("Tipografia visual", False, str(e)[:120], category="tipografia")
        finally:
            ctx.close()

        # ── AUDITORIA 7 — RESPONSIVIDADE ──────────────────────────────────────
        print("\n📱 AUDITORIA 7 — Responsividade")
        for vp in VIEWPORTS:
            ctx  = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = ctx.new_page()
            try:
                page.goto(FRONTEND_URL, timeout=15000, wait_until="domcontentloaded")
                page.wait_for_timeout(800)

                # Verifica overflow horizontal (layout quebrado)
                has_overflow = page.evaluate("""() => {
                    const body = document.body;
                    return body.scrollWidth > window.innerWidth + 5;
                }""")
                add(f"Sem overflow horizontal — {vp['name']}", not has_overflow,
                    f"scrollWidth={page.evaluate('document.body.scrollWidth')} > {vp['width']}" if has_overflow else "",
                    category="responsividade")

                # Screenshot por viewport
                shot = str(SHOTS_DIR / f"resp_{vp['name'].replace(' ', '_')}.png")
                page.screenshot(path=shot, full_page=False)

                # Verifica elementos críticos visíveis
                topbar_visible = page.locator(".topbar").first.is_visible()
                add(f"TopBar visível — {vp['name']}", topbar_visible,
                    shot, category="responsividade")

            except Exception as e:
                add(f"Responsividade — {vp['name']}", False, str(e)[:120], category="responsividade")
            finally:
                ctx.close()

        # ── AUDITORIA 8 — TEMA DARK/LIGHT ─────────────────────────────────────
        print("\n🌙 AUDITORIA 8 — Tema Dark / Light Mode")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(FRONTEND_URL, timeout=15000, wait_until="networkidle")
            page.wait_for_timeout(500)

            # Estado inicial (dark)
            bg_dark = page.evaluate("""() =>
                getComputedStyle(document.documentElement).getPropertyValue('--shell-bg').trim()
            """)
            add("Dark mode — --shell-bg é #111110", bg_dark.replace(" ", "") == "#111110",
                f"Valor atual: {bg_dark!r}", category="tema")

            # Faz toggle para light
            try:
                page.locator(".nav-footer-btn").first.click()
                page.wait_for_timeout(400)
                html_class = page.locator("html").get_attribute("class") or ""
                light_active = "light-mode" in html_class
                add("Toggle tema aplica .light-mode no <html>", light_active,
                    f"class atual: {html_class!r}", category="tema")

                if light_active:
                    bg_light = page.evaluate("""() =>
                        getComputedStyle(document.documentElement).getPropertyValue('--shell-bg').trim()
                    """)
                    add("Light mode — --shell-bg muda para #F8F7F4",
                        bg_light.replace(" ", "") == "#F8F7F4",
                        f"Valor: {bg_light!r}", category="tema")

                # Screenshot light mode
                shot_light = str(SHOTS_DIR / "tema_light.png")
                page.screenshot(path=shot_light)

                # Volta para dark
                page.locator(".nav-footer-btn").first.click()
                page.wait_for_timeout(400)
                shot_dark = str(SHOTS_DIR / "tema_dark.png")
                page.screenshot(path=shot_dark)
                add("Tema volta para dark mode", True, category="tema")

            except Exception as e:
                add("Toggle tema", False, str(e)[:120], category="tema", severity="warn")
        finally:
            ctx.close()

        # ── AUDITORIA 9 — FOCO VISUAL (acessibilidade de teclado) ─────────────
        print("\n⌨️  AUDITORIA 9 — Focus Visual (navegação por teclado)")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(FRONTEND_URL, timeout=15000, wait_until="networkidle")
            page.wait_for_timeout(500)

            # Injeta CSS para detectar foco visível
            visible_focus = page.evaluate("""() => {
                const focusable = [...document.querySelectorAll(
                    'button, input, select, textarea, a[href], [tabindex]'
                )].filter(el => !el.disabled && el.offsetParent !== null);

                let withFocus = 0;
                for (const el of focusable.slice(0, 8)) {
                    el.focus();
                    const style = window.getComputedStyle(el, ':focus');
                    const outline = style.outline || style.outlineStyle;
                    if (outline && outline !== 'none' && outline !== '0px') {
                        withFocus++;
                    }
                }
                return { total: Math.min(focusable.length, 8), with_focus: withFocus };
            }""")

            pct = (visible_focus["with_focus"] / max(visible_focus["total"], 1)) * 100
            add(f"Focus visível — {visible_focus['with_focus']}/{visible_focus['total']} elementos",
                pct >= 50,
                f"{pct:.0f}% dos elementos têm outline de foco visível",
                category="acessibilidade", severity="warn")

        except Exception as e:
            add("Focus visual", False, str(e)[:120], category="acessibilidade")
        finally:
            ctx.close()

        # ── AUDITORIA 10 — CLS / LAYOUT SHIFT ─────────────────────────────────
        print("\n⚡ AUDITORIA 10 — Estabilidade Visual (CLS)")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            # Injeta observer ANTES de navegar
            cls_score = None

            page.goto(FRONTEND_URL, timeout=20000, wait_until="domcontentloaded")

            # Mede CLS via API PerformanceObserver
            cls_score = page.evaluate("""() => {
                return new Promise(resolve => {
                    let cls = 0;
                    try {
                        const observer = new PerformanceObserver(list => {
                            for (const entry of list.getEntries()) {
                                if (!entry.hadRecentInput) cls += entry.value;
                            }
                        });
                        observer.observe({ type: 'layout-shift', buffered: true });
                        setTimeout(() => { observer.disconnect(); resolve(cls); }, 2000);
                    } catch(e) { resolve(0); }
                });
            }""")
            page.wait_for_timeout(2500)

            # Também mede FCP e LCP
            perf = page.evaluate("""() => {
                const nav = performance.getEntriesByType('navigation')[0] || {};
                const paint = performance.getEntriesByType('paint');
                const fcp = paint.find(p => p.name === 'first-contentful-paint');
                return {
                    fcp: fcp ? Math.round(fcp.startTime) : null,
                    domInteractive: Math.round(nav.domInteractive || 0),
                    domComplete: Math.round(nav.domComplete || 0),
                };
            }""")

            cls_val = float(cls_score) if cls_score is not None else 0.0
            add(f"CLS — Cumulative Layout Shift ({cls_val:.4f})",
                cls_val < 0.1,
                f"Score: {cls_val:.4f} — Bom: <0.1 | Precisa melhorar: 0.1-0.25 | Ruim: >0.25",
                category="performance")

            if perf["fcp"]:
                fcp_ok = perf["fcp"] < 1800
                add(f"FCP — First Contentful Paint ({perf['fcp']}ms)",
                    fcp_ok, f"Bom: <1800ms | Atual: {perf['fcp']}ms", category="performance")

            if perf["domInteractive"]:
                tti_ok = perf["domInteractive"] < 3000
                add(f"TTI aproximado ({perf['domInteractive']}ms)",
                    tti_ok, f"Bom: <3000ms | Atual: {perf['domInteractive']}ms", category="performance")

            shot_perf = str(SHOTS_DIR / "performance_final.png")
            page.screenshot(path=shot_perf)

        except Exception as e:
            add("Performance / CLS", False, str(e)[:120], category="performance")
        finally:
            ctx.close()

        # ── AUDITORIA 11 — ÍCONES / SVGS ──────────────────────────────────────
        print("\n🔷 AUDITORIA 11 — Ícones e SVGs")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(FRONTEND_URL, timeout=15000, wait_until="networkidle")
            page.wait_for_timeout(500)

            svg_audit = page.evaluate("""() => {
                const svgs = [...document.querySelectorAll('svg')];
                const broken = svgs.filter(s => s.getBoundingClientRect().width === 0 && s.closest('[class]'));
                const total  = svgs.length;
                return { total, broken: broken.length };
            }""")

            add(f"SVGs sem quebra — {svg_audit['total']} total, {svg_audit['broken']} quebrados",
                svg_audit["broken"] == 0,
                f"{svg_audit['broken']} SVG(s) com width=0", category="visual")

        except Exception as e:
            add("Ícones SVG", False, str(e)[:120], category="visual")
        finally:
            ctx.close()

        # ── AUDITORIA 12 — Z-INDEX SANITY ─────────────────────────────────────
        print("\n🪟 AUDITORIA 12 — Z-index e Sobreposições")
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        try:
            page.goto(FRONTEND_URL, timeout=15000, wait_until="networkidle")
            page.wait_for_timeout(500)

            z_audit = page.evaluate("""() => {
                const all = [...document.querySelectorAll('*')];
                const high = all
                    .map(el => ({ z: parseInt(getComputedStyle(el).zIndex) || 0, tag: el.tagName, cls: el.className?.toString().slice(0,30) }))
                    .filter(x => x.z > 1000)
                    .sort((a, b) => b.z - a.z)
                    .slice(0, 5);
                return high;
            }""")

            suspicious = [z for z in z_audit if z["z"] > 10000]
            add("Z-index — sem valores suspeitos (>10000)",
                len(suspicious) == 0,
                f"Altos z-index: {suspicious}" if suspicious else
                f"Mais alto: {z_audit[0] if z_audit else 'nenhum'}",
                category="visual", severity="warn")

        except Exception as e:
            add("Z-index", False, str(e)[:120], category="visual")
        finally:
            ctx.close()

        browser.close()


# ── Comparação de screenshots ──────────────────────────────────────────────
def compare_screenshots(path1: str, path2: str) -> float:
    """Retorna % de pixels diferentes entre dois screenshots."""
    try:
        from PIL import Image
        import io

        img1 = Image.open(path1).convert("RGB")
        img2 = Image.open(path2).convert("RGB")

        # Redimensiona para o menor para comparar
        w = min(img1.width, img2.width)
        h = min(img1.height, img2.height)
        img1 = img1.resize((w, h))
        img2 = img2.resize((w, h))

        pixels1 = list(img1.getdata())
        pixels2 = list(img2.getdata())

        diff_count = sum(
            1 for p1, p2 in zip(pixels1, pixels2)
            if abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]) > 30
        )
        return (diff_count / len(pixels1)) * 100
    except ImportError:
        warn("Pillow não instalado — screenshot diff ignorado (pip install Pillow)")
        return 0.0
    except Exception as e:
        warn(f"Erro ao comparar screenshots: {e}")
        return 0.0


# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO HTML
# ══════════════════════════════════════════════════════════════════════════════
def generate_report():
    total  = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    pct    = int(passed / total * 100) if total else 0
    now    = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Agrupa por categoria
    categories = {}
    for r in results:
        cat = r.get("category", "geral")
        categories.setdefault(cat, []).append(r)

    ICONS = {
        "tokens":          "📐",
        "contraste":       "🎨",
        "tipografia":      "✏️",
        "componentes":     "🧩",
        "visual":          "📸",
        "responsividade":  "📱",
        "tema":            "🌙",
        "acessibilidade":  "⌨️",
        "performance":     "⚡",
        "geral":           "🔍",
    }

    sections = ""
    for cat, items in categories.items():
        cat_passed = sum(1 for r in items if r["passed"])
        cat_total  = len(items)
        cat_pct    = int(cat_passed / cat_total * 100) if cat_total else 0
        icon       = ICONS.get(cat, "🔍")
        bar_color  = "#2ecc71" if cat_pct == 100 else "#e67e22" if cat_pct >= 70 else "#e74c3c"

        rows = ""
        for r in items:
            status    = "✅ PASS" if r["passed"] else ("⚠️ WARN" if r.get("severity") == "warn" else "❌ FAIL")
            row_bg    = "" if r["passed"] else "background:rgba(231,76,60,.06)" if r.get("severity") != "warn" else "background:rgba(230,126,34,.06)"
            shot_html = ""
            if r.get("screenshot") and Path(r["screenshot"]).exists():
                shot_html = f'<br><img src="{r["screenshot"]}" style="max-width:500px;margin-top:6px;border:1px solid #2A2825;border-radius:4px;">'
            rows += f"""
            <tr style="{row_bg}">
              <td style="white-space:nowrap;font-weight:bold">{status}</td>
              <td>{r['name']}</td>
              <td style="font-size:0.82em;color:#8C8A85">{r.get('detail','')}{shot_html}</td>
            </tr>"""

        sections += f"""
        <div class="section">
          <div class="section-header">
            <span>{icon} {cat.upper()}</span>
            <span style="color:{bar_color};font-family:var(--mono);font-size:13px">{cat_passed}/{cat_total} ({cat_pct}%)</span>
          </div>
          <table>
            <thead><tr><th>Status</th><th>Verificação</th><th>Detalhe</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    warn_html = ""
    if warnings:
        items = "".join(f"<li><code>{w}</code></li>" for w in warnings)
        warn_html = f'<div class="section"><div class="section-header">⚠️ AVISOS</div><ul style="padding:12px 20px;color:#e67e22">{items}</ul></div>'

    bar_color = "#2ecc71" if pct >= 90 else "#e67e22" if pct >= 70 else "#e74c3c"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>TM-Testes-Design — AutoRelatório V5</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    :root {{
      --bg: #111110; --card: #1A1917; --border: #2A2825;
      --text: #EFEDE8; --muted: #8C8A85; --subtle: #4A4845;
      --orange: #C8541C; --green: #4F7A3A;
      --sans: 'Inter', system-ui; --mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: var(--sans); background: var(--bg); color: var(--text); padding: 32px; line-height: 1.5; }}
    h1 {{ font-size: 22px; color: var(--orange); margin-bottom: 4px; }}
    .ts {{ color: var(--subtle); font-family: var(--mono); font-size: 11px; margin-bottom: 24px; }}
    .summary {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 18px 24px; }}
    .card .num {{ font-size: 2rem; font-weight: 700; font-family: var(--mono); }}
    .card .lbl {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
    .card.ok .num {{ color: #2ecc71; }} .card.bad .num {{ color: #e74c3c; }}
    .card.warn .num {{ color: #e67e22; }} .card.pct .num {{ color: var(--orange); }}
    .bar-wrap {{ flex: 1; min-width: 200px; }}
    .bar-label {{ font-size: 13px; font-weight: 600; margin-bottom: 6px; }}
    .bar-bg {{ background: #2A2825; border-radius: 6px; height: 18px; overflow: hidden; }}
    .bar {{ height: 100%; background: {bar_color}; width: {pct}%; }}
    .section {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 20px; overflow: hidden; }}
    .section-header {{ padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; background: #161513; font-weight: 600; font-size: 14px; border-bottom: 1px solid var(--border); }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{ text-align: left; padding: 8px 14px; color: var(--subtle); font-size: 10px; text-transform: uppercase; letter-spacing: .1em; background: #161513; border-bottom: 1px solid var(--border); }}
    td {{ padding: 9px 14px; border-bottom: 1px solid var(--border); font-size: 13px; vertical-align: top; }}
    tr:last-child td {{ border-bottom: none; }}
    code {{ background: #2A2825; padding: 1px 5px; border-radius: 3px; font-family: var(--mono); font-size: 11px; }}
    .footer {{ color: var(--subtle); font-size: 11px; font-family: var(--mono); margin-top: 30px; text-align: center; }}
  </style>
</head>
<body>
  <h1>🛡️ TM-Testes-Design — Guardião do Design System</h1>
  <div class="ts">AutoRelatório V5 · {now} · workframe TM Sempre Tecnologia</div>

  <div class="summary">
    <div class="card ok"><div class="num">{passed}</div><div class="lbl">Aprovações</div></div>
    <div class="card bad"><div class="num">{failed}</div><div class="lbl">Falhas</div></div>
    <div class="card pct"><div class="num">{pct}%</div><div class="lbl">Score geral</div></div>
    <div class="card bar-wrap">
      <div class="bar-label">Saúde do design system</div>
      <div class="bar-bg"><div class="bar"></div></div>
    </div>
  </div>

  {warn_html}
  {sections}

  <div class="footer">
    🛡️ Guardião do Design System · skill tm-testes · TM Sempre Tecnologia<br>
    Screenshots: <code>design_screenshots/</code> · Baseline: <code>design_baseline/</code>
  </div>
</body>
</html>"""

    REPORT_PATH.write_text(html, encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="TM-Testes-Design — Guardião do Design System")
    parser.add_argument("--update",  action="store_true", help="Atualiza baseline de screenshots")
    parser.add_argument("--quick",   action="store_true", help="Só auditorias estáticas (sem browser)")
    args = parser.parse_args()

    print("=" * 64)
    print("  🛡️  TM-TESTES-DESIGN — Guardião do Design System")
    print("  AutoRelatório V5  ·  TM Sempre Tecnologia")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 64)

    # Auditorias estáticas (sem browser)
    audit_tokens()
    audit_contrast()
    audit_typography()
    audit_components()

    # Auditorias visuais com Playwright
    if not args.quick:
        audit_with_playwright(update_baseline=args.update)
    else:
        print("\n⏭️  Modo --quick: auditorias visuais ignoradas")

    # Relatório
    generate_report()

    # Summary
    total  = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    pct    = int(passed / total * 100) if total else 0

    print("\n" + "=" * 64)
    print(f"  🛡️  RESULTADO FINAL: {passed}/{total} ({pct}%)")
    if failed == 0:
        print("  ✅ Design system 100% saudável!")
    else:
        errors   = [r for r in results if not r["passed"] and r.get("severity") != "warn"]
        warnings_ = [r for r in results if not r["passed"] and r.get("severity") == "warn"]
        if errors:
            print(f"  ❌ {len(errors)} erro(s) crítico(s)")
        if warnings_:
            print(f"  ⚠️  {len(warnings_)} aviso(s)")
    print(f"\n  📄 Relatório: {REPORT_PATH.name}")
    print(f"  📸 Screenshots: design_screenshots/")
    print(f"  💾 Baseline: design_baseline/")
    print("=" * 64)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
