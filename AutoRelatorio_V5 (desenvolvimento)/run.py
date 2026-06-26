"""
AutoRelatorio V5 — Launcher
Inicia o app Next.js e abre no navegador.
"""

import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# ─── Config ─────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
FRONTEND   = BASE_DIR / "frontend"
PORT       = 3000
URL        = f"http://localhost:{PORT}"

print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║        🚀 AutoRelatorio V5 — Launcher                 ║
║        Desenvolvido por: Thiago Nascimento Barbosa    ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")

# ─── Verificar pasta frontend ─────────────────────────
if not FRONTEND.exists():
    print(f"❌ ERRO: Pasta 'frontend/' não encontrada em {BASE_DIR}")
    print("   Certifique-se de que o Next.js foi instalado corretamente.")
    sys.exit(1)

if not (FRONTEND / "package.json").exists():
    print("❌ ERRO: package.json não encontrado em frontend/")
    sys.exit(1)

print(f"✅ Projeto Next.js encontrado: {FRONTEND}")
print(f"🌐 URL: {URL}")
print(f"\n🔄 Iniciando Next.js (npm run dev)...\n")

# ─── Iniciar Next.js ─────────────────────────────────
try:
    dev_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=str(FRONTEND),
        shell=True,   # necessário no Windows para encontrar npm
    )

    # Aguarda Next.js compilar (primeira vez pode demorar mais)
    print("⏳ Aguardando compilação inicial (~5s)...")
    time.sleep(5)

    # Abre navegador
    print(f"🌐 Abrindo navegador: {URL}")
    webbrowser.open(URL)

    print(f"""
╔════════════════════════════════════════════════════════╗
║                    ✅ PRONTO!                         ║
║                                                        ║
║  App rodando em: {URL:<38}║
║  Pressione Ctrl+C para desligar                       ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")

    try:
        dev_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Desligando servidor Next.js...")
        dev_process.terminate()
        try:
            dev_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            dev_process.kill()
        print("✅ Servidor desligado.")

except FileNotFoundError:
    print("❌ ERRO: 'npm' não encontrado.")
    print("   Instale o Node.js em https://nodejs.org e tente novamente.")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERRO ao iniciar: {e}")
    sys.exit(1)
