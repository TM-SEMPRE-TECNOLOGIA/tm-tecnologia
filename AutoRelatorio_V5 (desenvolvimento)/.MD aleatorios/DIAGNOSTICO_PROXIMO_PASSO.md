# 🔍 Diagnóstico — AutoRelatório V5 — Status Atualizado

**Última atualização:** 2026-05-25  
**Status:** Backend funcional end-to-end. Frontend conectado. Step 2 (blocos) pendente.

---

## Status Atual (após migração V4 → V5)

```
AutoRelatório V5 — Estado Real
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 UI / Layout           ████████░░  80% ✅
 Step 1 (formulário)   ██████████ 100% ✅
 Step 2 (blocos)       ░░░░░░░░░░   0% ❌  ← PRÓXIMO
 Step 3 (resumo)       ████████░░  80% ⚠️
 Preview (HTML)        ██████████ 100% ✅ (só dados cabeçalho)
 Preview (tabelas)     ░░░░░░░░░░   0% ❌  (depende do Step 2)
 Backend (estrutura)   ██████████ 100% ✅
 Backend (scanner SP2) ██████████ 100% ✅ (testado end-to-end)
 Backend (word build)  ██████████ 100% ✅ (testado, gera .docx real)
 Backend (9 contratos) ████████░░  80% ⚠️  (SP2 testado, trad/sp não)
 Bridge API            ████████░░  80% ✅  (/health e /generate implementados)

 FUNCIONALIDADE CORE (com pasta)  ██████████ 100% ✅
 (scan → build_word → download .docx)

 FUNCIONALIDADE BROWSER (sem pasta) ░░░░░░░░░░   0% ❌
 (o usuário ainda precisa de Tauri/Electron para selecionar pasta)

Progresso geral: ~70% (backend completo) / 0% (Step 2 browser)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## O que foi feito (Sprint 0 — Migração V4 → V5)

### ✅ Concluído em 2026-05-25

| Tarefa | Status |
|--------|--------|
| 9 templates .docx copiados de V4 | ✅ |
| generator_sp2.py migrado para c1565 | ✅ |
| generator_sp.py migrado para c0908 | ✅ |
| generator_trad.py migrado para 7 contratos tradicionais | ✅ |
| word_utils.py, word_utils_sp.py, word_utils_sp2.py → core/ | ✅ |
| utils_sp.py, utils_sp2.py → core/ | ✅ |
| scanner_sp2.py (wrapper V5) criado para c1565 | ✅ |
| word_builder_sp2.py (wrapper V5) criado para c1565 | ✅ |
| scanner_sp.py + word_builder_sp.py criados para c0908 | ✅ |
| scanner.py + word_builder.py criados para 7 contratos trad | ✅ |
| items.json extraído para 6 contratos (do itens_por_contrato.json) | ✅ |
| items.json extraído para c1565 (do itens_contrato.json SP2) | ✅ |
| Endpoint /health adicionado ao server.py | ✅ |
| Endpoint /generate (payload flat) adicionado ao server.py | ✅ |
| lib/api.ts atualizado para tratar FileResponse (blob download) | ✅ |
| .env.local alinhado com porta 5000 | ✅ |
| requirements.txt criado | ✅ |
| INICIAR.bat criado | ✅ |
| Teste end-to-end c1565: scan + build_word → .docx gerado ✅ | ✅ |
| Build frontend sem erros | ✅ |

---

## O que falta

### ❌ SPRINT 1 — Step 2 no Frontend (blocos dinâmicos)

O usuário ainda não consegue selecionar uma pasta de fotos no browser.

Opções:
A) Modo web puro — <input webkitdirectory> (browser nativo)
   - Usuário clica, seleciona pasta, browser envia os File[]
   - Frontend lê os nomes, detecta as medidas, mostra os blocos
   - Limitação: o backend não consegue ler esses arquivos diretamente

B) Modo desktop (futuro) — Tauri ou Electron
   - App nativo acessa o disco diretamente
   - Envia root_path para o backend, que roda o scanner real
   - O backend /generate já suporta root_path quando fornecido

Componentes a criar (Sprint 1):
- components/steps/Step2.tsx
- hooks/useBlocks.ts
- components/blocks/FolderPicker.tsx
- components/blocks/BlockList.tsx
- components/blocks/BlockCard.tsx
- components/blocks/MeasureForm.tsx

### ⚠️ Items pendentes para c2056 e c6122
Os items.json estão vazios (contratos sem dados no V4).
Precisam das planilhas reais de Thiago.

---

## Como iniciar o app

Duplo clique em INICIAR.bat

Ou manual:
  Terminal 1: cd backend && python -m uvicorn core.server:app --port 5000 --reload
  Terminal 2: cd frontend && npm run dev

URLs:
  App:      http://localhost:3000
  API docs: http://localhost:5000/docs
  Health:   http://localhost:5000/health