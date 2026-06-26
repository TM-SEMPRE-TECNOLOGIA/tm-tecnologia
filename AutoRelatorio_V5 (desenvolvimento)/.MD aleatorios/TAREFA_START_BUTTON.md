# 🚀 TAREFA: Criar Button START + Script Launcher (V5)

**Para:** Agente "Add collapse arrow..."  
**Baseado em:** Pattern da V4 (run.bat + run.py)  
**Prioridade:** ALTA  
**Tempo:** 30-45 min

---

## 🎯 OBJETIVO

Criar um **botão START** no frontend que:
1. Abre servidor local (se necessário)
2. Inicia aplicação V5
3. Abre navegador na URL correta
4. Mostra status de inicialização

**Padrão V4:** `run.bat` → `run.py` → FastAPI + Next.js no mesmo terminal

---

## 📋 REFERÊNCIA — Como Funciona na V4

### V4 Structure
```
AutoRelatorio_V4/
├── run.bat (2 linhas simples)
├── run.py (launcher premium com Rich UI)
├── APP/
│   ├── backend/ (FastAPI)
│   └── frontend/ (Next.js)
└── logs/
```

### V4 run.bat
```batch
@echo off
title TM Relatorio — Desenvolvedor Thiago Nascimento Barbosa
cd /d "%~dp0"
python run.py
```

### V4 run.py (conceito)
```python
# Launcher Premium
# 1. Mata processos nas portas 3000 (frontend) + 5000 (backend)
# 2. Inicia backend (FastAPI)
# 3. Inicia frontend (Next.js)
# 4. Aguarda ambos ficarem ready
# 5. Abre navegador em http://localhost:3000
# 6. Monitora saúde de ambos
# 7. Graceful shutdown ao Ctrl+C
```

---

## 🏗️ ESTRUTURA V5 (Seu Projeto)

```
AutoRelatorio_V5/
├── index.html ..................... (app real atual)
├── app.js ......................... (seu JavaScript)
├── styles.css ..................... (seu CSS)
│
├── run.bat (A CRIAR) .............. Launcher simples
├── run.py (A CRIAR) ............... Launcher com UI (opcional)
│
├── .context/ ...................... (documentação)
├── .docs/ ......................... (wireframe original)
└── scripts/ ....................... (helpers)
```

---

## ✅ TAREFA DETALHADA

### PASSO 1: Criar run.bat

**Arquivo:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\run.bat`

```batch
@echo off
title AutoRelatorio V5 — Thiago Nascimento Barbosa
cd /d "%~dp0"
python run.py
pause
```

**O que faz:**
- Define título do terminal
- Muda para pasta do projeto
- Executa run.py
- Aguarda usuário pressionar Enter para fechar

---

### PASSO 2: Criar run.py

**Arquivo:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\run.py`

```python
"""
AutoRelatorio V5 — Launcher
Inicia servidor local e abre aplicação no navegador.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# ─── Config ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
APP_FILE = BASE_DIR / "index.html"
PORT = 8000  # Porta local
URL = f"http://localhost:{PORT}"

print(f"""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║        🚀 AutoRelatorio V5 — Launcher                 ║
║        Desenvolvido por: Thiago Nascimento Barbosa    ║
║                                                        ║
╚════════════════════════════════════════════════════════╝

📂 Projeto: {BASE_DIR}
🌐 URL: {URL}
📄 App: {APP_FILE}

Iniciando servidor...
""")

# ─── Verificar se arquivo HTML existe ────────────────
if not APP_FILE.exists():
    print(f"❌ ERRO: {APP_FILE} não encontrado!")
    sys.exit(1)

print(f"✅ App encontrado: {APP_FILE.name}")

# ─── Iniciar servidor local ──────────────────────────
try:
    # Usar Python's http.server (built-in, sem dependências)
    print(f"\n🔄 Iniciando servidor em {URL}...")
    
    # Comando para Windows/Linux/Mac
    server_cmd = [
        sys.executable, 
        "-m", 
        "http.server", 
        str(PORT),
        "--directory",
        str(BASE_DIR)
    ]
    
    # Inicia servidor em background
    server_process = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(BASE_DIR)
    )
    
    # Aguarda servidor ficar ready
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(2)
    
    # Abre navegador
    print(f"🌐 Abrindo navegador: {URL}")
    webbrowser.open(URL)
    
    print(f"""
╔════════════════════════════════════════════════════════╗
║                    ✅ PRONTO!                         ║
║                                                        ║
║  Servidor rodando em: {URL}
║  Pressione Ctrl+C para desligar                       ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
""")
    
    # Aguarda até usuário pressionar Ctrl+C
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Desligando servidor...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✅ Servidor desligado.")
        
except Exception as e:
    print(f"\n❌ ERRO ao iniciar: {e}")
    sys.exit(1)
```

**O que faz:**
- Verifica se `index.html` existe
- Inicia servidor HTTP local (Python built-in)
- Aguarda servidor ficar ready
- Abre navegador automaticamente
- Monitora até Ctrl+C
- Desliga gracefully

**Dependências:** Nenhuma (só Python 3.x)

---

### PASSO 3: Botão START no HTML (Frontend)

**Arquivo:** `index.html`

**Local:** Na seção topbar (onde estão Novo + Gerar .docx)

```html
<!-- ANTES: -->
<button class="btn btn-ghost btn-sm" onclick="setStep(1)">
  <svg>...</svg>
  Novo
</button>

<!-- ADICIONAR AO LADO: -->
<button class="btn btn-primary btn-sm" onclick="iniciarApp()" title="Inicia servidor e abre no navegador">
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polygon points="5 3 19 12 5 21 5 3"></polygon>
  </svg>
  START
</button>
```

**JavaScript (adicionar ao `<script>`):**

```javascript
function iniciarApp() {
  // Opção 1: Mostrar instruções
  alert(`
🚀 Para iniciar o AutoRelatorio V5:

1. Abra terminal na pasta do projeto:
   C:\\Users\\thiag\\Desktop\\tm-tecnologia\\AutoRelatorio_V5

2. Execute:
   run.bat

3. O servidor abrirá automaticamente no navegador!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Atalho: Double-click em 'run.bat'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);
  
  // Opção 2: Tentar executar run.bat (Windows only, requer permissão)
  // fetch('/api/start') — se tiver backend
}
```

---

## 📁 Estrutura Final

```
AutoRelatorio_V5/
├── index.html
├── app.js
├── styles.css
│
├── run.bat ........................ ✅ NOVO
├── run.py ......................... ✅ NOVO
│
├── scripts/
│   └── ... (parsers, etc)
│
└── .context/ (documentação)
```

---

## 🧪 TESTE

### Windows
```bash
# 1. Navegar até pasta
cd C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5

# 2. Double-click em run.bat OU executar:
run.bat

# 3. Verificar:
# ✅ Terminal abre com título "AutoRelatorio V5"
# ✅ Servidor inicia na porta 8000
# ✅ Navegador abre em http://localhost:8000
# ✅ App está visível
# ✅ Ctrl+C desliga tudo

# OU via CMD:
.\run.bat
```

---

## 🎯 CHECKLIST

- [ ] `run.bat` criado (raiz projeto)
- [ ] `run.py` criado (raiz projeto)
- [ ] Botão START adicionado ao HTML
- [ ] run.bat testado (abre terminal + inicia servidor)
- [ ] run.py testado (abre navegador automaticamente)
- [ ] Ctrl+C desliga gracefully
- [ ] Documentação atualizada

---

## 📝 DEPOIS DISSO

Quando terminar:
1. Reporte aqui
2. Teste o botão START
3. Próximo: **Blocos Dinâmicos** (parser Excel + UI)

---

## 💡 NOTAS

- V5 é mais simples que V4 (sem backend FastAPI)
- Usa servidor HTTP built-in do Python (http.server)
- Sem dependências externas
- Mesmo padrão user-friendly da V4

**Quer começar?** Confirma quando agente terminar! 🚀

