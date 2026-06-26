# 🔬 Engenharia Reversa Completa — AutoRelatório V5
## Mapeamento Forense Total do Ecossistema
> Gerado em 2026-05-26 por análise forense de ~40 módulos Python, ~15 componentes React/TS e ~20 documentos MD.

---

## 📍 ÍNDICE RÁPIDO

| Seção | Conteúdo |
|-------|----------|
| [1. Status Atual](#1-status-atual-do-v5) | Progresso por módulo |
| [2. Arquitetura](#2-arquitetura-do-sistema) | Camadas, padrões, fluxo |
| [3. Inventário Backend](#3-inventário-de-módulos---backend) | Python core + contratos |
| [4. Inventário Frontend](#4-inventário-de-módulos---frontend) | React hooks + componentes |
| [5. 9 Contratos](#5-os-9-contratos-ativos) | Modos, templates, status |
| [6. Linha do Tempo](#6-linha-do-tempo-técnica) | Da proto-V1 ao V5 |
| [7. Regras de Negócio](#7-regras-de-negócio-implícitas) | RN-01 a RN-12 |
| [8. Sprints](#8-histórico-de-sprints) | Sprint 0-2 + Sprint 3 planejado |
| [9. Reaproveitamento](#9-mapa-de-reaproveitamento) | O que reusar/portar/construir |
| [10. Alertas](#10-alertas-e-riscos) | 7 riscos ativos |

---

## 1. STATUS ATUAL DO V5

```
AutoRelatório V5 — Estado em 2026-05-26
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 UI / Layout              ██████████ 100% ✅
 Step 1 (formulário)      ██████████ 100% ✅
 Step 2 (blocos)          █████████░  90% ✅
 Step 3 (resumo)          ██████████ 100% ✅
 Preview (cabeçalho)      ██████████ 100% ✅
 Preview (tabelas+thumbs) ██████████ 100% ✅
 Backend (estrutura)      ██████████ 100% ✅
 Backend (scanner SP2)    ██████████ 100% ✅ (testado e2e)
 Backend (word build)     ██████████ 100% ✅ (testado e2e)
 Backend (9 contratos)    ████████░░  80% ⚠️  (SP2 ok, trad/sp aguardam)
 Bridge API               ██████████ 100% ✅
 Upload fotos → backend   ░░░░░░░░░░   0% ❌  (Sprint 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Iniciar app:**
```
duplo clique em INICIAR.bat
ou:
  cd backend && python -m uvicorn core.server:app --port 5000 --reload
  cd frontend && npm run dev
URLs: http://localhost:3000 (app) | http://localhost:5000/docs (API)
```

---

## 2. ARQUITETURA DO SISTEMA

### Fluxo Principal (Scanner → Builder)

```
[Usuário]
  ↓ seleciona contrato + preenche formulário + seleciona fotos
  ↓ clica Gerar
  ↓ POST /generate → { contrato_id, nr_os, ag_cod, ag_nome, ... }

[FastAPI · porta 5000]
  ↓ get_engine(contrato_id)          ← registry.py
  ↓ engine.validate_folder(root)     ← ValidationResult
  ↓ engine.scan(root_path)           ← scanner_*.py → conteudo[]
  ↓ engine.build_word(tpl, conteudo) ← word_builder_*.py → output.docx
  ↓ FileResponse → binário

[Browser]
  ↓ requestFile() → blob URL
  ↓ <a download> → save to disk
```

### Padrões Arquiteturais (NUNCA quebrá-los)

**Padrão 1 — conteudo[] como contrato de dados:**
```python
# Tipos válidos no array conteudo[]:
"» Título Nível 1"              # str com prefixo »
{"imagem": path}                # foto normal
{"quebra_pagina": True}         # quebra de página
{"memoria_calculo": {...}}      # tabela SP
{"tabela_itens_sp2": {...}}     # tabela SP2
{"croqui": path, "legenda": str} # croqui SP2
{"enunciado_item": {...}}        # texto de item SP2
```

**Padrão 2 — Sort de pastas em 3 camadas:**
```python
def folder_sort_key(name):
    if "vista ampla" in name.lower(): return (0, name)   # SEMPRE 1º
    if re.match(r'^(\d+)', name):     return (1, num, rest)  # numérico
    if "detalhes" in name.lower():    return (3, name)   # SEMPRE último
    return (2, name)                                     # alfabético
```

**Padrão 3 — Dual server:**
```
FastAPI   → porta 5000  (backend)
Next.js   → porta 3000  (frontend)
CORS: allow_origins=["*"]
```

**Padrão 4 — ContractEngine ABC:**
```python
class ContractEngine(ABC):
    def scan(self, root_path, logger=None) -> list:   # scanner
    def build_word(self, tpl, conteudo, out, meta) -> str:  # builder
    def get_items(self) -> dict:                      # banco de itens
    def get_meta_fields(self) -> list[MetaField]:     # campos form
    def validate_folder(self, root_path) -> ValidationResult:
```

---

## 3. INVENTÁRIO DE MÓDULOS — BACKEND

### Core Shared

| Arquivo | Funções principais | Status |
|---------|-------------------|--------|
| `core/server.py` (5.4KB) | FastAPI app, 6 endpoints, GenerateFlatRequest | ✅ ativo |
| `core/contract_engine.py` (1.7KB) | ABC ContractEngine, MetaField, ValidationResult | ✅ ativo |
| `core/registry.py` (2.0KB) | _ENGINES dict, get_engine(), list_contracts() | ✅ ativo |
| `core/word_utils.py` (20KB) | extract_placeholders, substitute_placeholders, validate_substitutions, inserir_conteudo | ✅ ativo |
| `core/word_utils_sp.py` (15KB) | inserir_conteudo_sp, set_cell_background, tabelas memória de cálculo | ✅ ativo |
| `core/word_utils_sp2.py` (22KB) | inserir_conteudo_sp2, tabelas SP2, croquis, enunciados | ✅ ativo |
| `core/utils_sp.py` (2.6KB) | parse_medidas_arquivo, formatar_moeda_texto, formatar_descricao_tecnica | ✅ ativo |
| `core/utils_sp2.py` (14.6KB) | parse_medidas_sp2, detectar_item_por_pasta, e_croqui, extrair_legenda_croqui | ✅ ativo |

### Por Contrato

| Contrato | Modo | Scanner | Builder | items.json |
|----------|------|---------|---------|------------|
| `c0908` São Paulo | SP | scanner_sp.py | word_builder_sp.py | ✅ ok |
| `c1507` Cuiabá | Trad | scanner.py | word_builder.py | ✅ ok |
| `c1565` S.J.R.Preto ⭐ | SP2 | scanner_sp2.py | word_builder_sp2.py | ✅ ok |
| `c2056` Divinópolis | Trad | scanner.py | word_builder.py | ⚠️ vazio |
| `c2057` Varginha | Trad | scanner.py | word_builder.py | ⚠️ vazio |
| `c2626` Salinas | Trad | scanner.py | word_builder.py | ✅ ok |
| `c2627` Gov. Valadares | Trad | scanner.py | word_builder.py | ✅ ok |
| `c3575` Tangará da Serra | Trad | scanner.py | word_builder.py | ✅ ok |
| `c6122` Mato Grosso do Sul | Trad | scanner.py | word_builder.py | ⚠️ vazio |

---

## 4. INVENTÁRIO DE MÓDULOS — FRONTEND

| Arquivo | Responsabilidade | Sprint |
|---------|-----------------|--------|
| `app/page.tsx` | Entry point. Orquestra todos os hooks. handleGenerate, handleStart, handleNew | V5 base |
| `components/TopBar.tsx` | Barra superior com botões | V5 base |
| `components/Sidebar.tsx` | Contratos e navegação | V5 base |
| `components/EditorPanel.tsx` | Steps 1/2/3. Integra BlockList no Step 2 | Sprint 1 |
| `components/PreviewPanel.tsx` | Preview HTML com tabelas dinâmicas + thumbnails | Sprint 2 |
| `components/ResizableDivider.tsx` | Divisor redimensionável | V5 base |
| `hooks/useBlocks.ts` ★ | Estado blocos: carregarArquivos, setItem, setMedida, consolidado | Sprint 1 |
| `hooks/useItems.ts` ★ | GET /api/contracts/{id}/items. Sort numérico | Sprint 1 |
| `hooks/useFormData.ts` | Formulário Step 1: nr_os, ag_cod, ag_nome, etc | V5 base |
| `hooks/useContracts.ts` | Contrato atual + lista | V5 base |
| `components/blocks/BlockList.tsx` ★ | input[webkitdirectory], progress bar, lista de cards | Sprint 1 |
| `components/blocks/BlockCard.tsx` ★ | Thumbnail + dropdown item + MeasureForm + badge | Sprint 1 |
| `components/blocks/MeasureForm.tsx` ★ | Formulário adaptativo m²/m³/m/km/un | Sprint 1 |
| `store/contractStore.ts` | Zustand store (herdado V4) | V4 herdado |
| `lib/api.ts` | checkHealth(), generateReport(), requestFile() → blob URL | Sprint 0 |

---

## 5. OS 9 CONTRATOS ATIVOS

```
0908 — SÃO PAULO          → Modo SP   (scanner_sp  + word_builder_sp)
1507 — CUIABÁ             → Modo Trad (scanner     + word_builder)
1565 — S.J.R.PRETO ⭐     → Modo SP2  (scanner_sp2 + word_builder_sp2)  ← ÚNICO SP2
2056 — DIVINÓPOLIS        → Modo Trad (scanner     + word_builder)
2057 — VARGINHA           → Modo Trad (scanner     + word_builder)
2626 — SALINAS            → Modo Trad (scanner     + word_builder)
2627 — GOV. VALADARES     → Modo Trad (scanner     + word_builder)
3575 — TANGARÁ DA SERRA   → Modo Trad (scanner     + word_builder)
6122 — MATO GROSSO DO SUL → Modo Trad (scanner     + word_builder)
```

### Estrutura de Pasta por Modo

**Tradicional:**
```
AGENCIA/
├── - Área externa/
│   ├── Vista ampla/    ← SEMPRE 1º (sort priority 0)
│   ├── 01 - Fachada/
│   └── 02 - Calha/
└── - Área interna/
    ├── 01.01 - SAA/
    └── 01.02 - Banheiro/
```

**SP (c0908):**
```
AGENCIA/
├── 1 - Área - Ambiente/
│   ├── 1.1 - Serviço/
│   │   ├── 01 - 3,10 x 2,95.jpg
│   │   └── 02 - 2,50 x 1,80 - Faces 2.jpg
│   └── 1.2 - Outro Serviço/
```

**SP2 (c1565):**
```
AGENCIA/
├── [Ambiente]/
│   ├── [Serviço]/
│   │   ├── CROQUI 01 - desc.jpg   ← croqui técnico
│   │   ├── 01 - 3,10 x 2,95.jpg
│   │   └── 02 - Faces 2.jpg
```

---

## 6. LINHA DO TEMPO TÉCNICA

```
2024     → PRÉ-HISTÓRICO: TM Extrator (Vite+React, sem backend)
2025 Q1  → PROTO-V1: Legacy TM Relatorio (Python simples, sem FastAPI)
2025 Q1  → PROTO-V2: TM Studio Relatorio (PRIMEIRA FastAPI, só Trad)
2025 Q2  → V0.9: TM Relatorio (sort natural básico)
2025 Q2  → V0.95: NX Relatorios (UI Next.js, SidebarWizard nasce)
2025 Q2  → V0.97: TM Relatorio SP (Modo SP + dark mode, page.tsx monolítico)
2025 Q2  → FUSÃO: NX Relatorios SP Mais Atualizado (utils_sp.py canônico)
Apr 2026 → V2: AutoRelatorio_V2 (scaffold Next.js, backend incompleto)
Mai 2026 → V3: PRIMEIRA VERSÃO COMPLETA (FastAPI 20+ endpoints, 2 modos)
Mai 2026 → V3.2: PLACEHOLDERS ({{campo}}, 70+ testes pytest) — PRODUCTION READY
Mai 2026 → V4: SP2 + Modo App + Zustand + Views separadas
21-25/05 → V5 Sprint 0: Migração V4→V5 (ContractEngine ABC, 9 engines)
25/05    → V5 Sprint 1+2: Blocos dinâmicos + integração browser
Sprint 3 → Upload fotos multipart (PLANEJADO)
```

---

## 7. REGRAS DE NEGÓCIO IMPLÍCITAS

| ID | Regra | Detalhe |
|----|-------|---------|
| RN-01 | 9 contratos fixos | Cada um tem template .docx exclusivo |
| RN-02 | Sort 3 camadas | "vista ampla" → numérico → alfabético → "detalhes" |
| RN-03 | Medidas no nome do arquivo | `"01 - 3,10 x 2,95 - Desconto 1,89m².jpg"` |
| RN-04 | Altura padrão imagem = 7cm | Portrait = 2 colunas, Landscape = 1 coluna |
| RN-05 | 7 placeholders dinâmicos | `{{nr_os}}`, `{{data_elaboracao}}` (auto), etc. |
| RN-06 | 4 descrições padrão | Variações do texto "levantamento preventivo" |
| RN-07 | c1565 exclusivamente SP2 | SINAPI, croquis, tabelas complexas |
| RN-08 | Fator Faces (SP2) | "Faces 2" no nome = área × 2 |
| RN-09 | Croquis SP2 | Arquivos com "CROQUI" no nome = tratamento especial |
| RN-10 | Output em backend/output/ | Nunca sobrescreve — versionamento pendente |
| RN-11 | Formato BR | Vírgula decimal, ponto milhar, dd/mm/yyyy |
| RN-12 | conteudo[] é o contrato | Scanner → conteudo[] → Builder. Não quebrar esse contrato. |

---

## 8. HISTÓRICO DE SPRINTS

### Sprint 0 — Migração V4→V5 (21-24/05/2026) ✅
- ContractEngine ABC + Registry de 9 engines
- Migração de todos os generators e word_builders
- 9 templates .docx + items.json para 6 contratos
- Endpoints /health e /generate
- Teste end-to-end c1565 → .docx 70KB gerado

### Sprint 1 — Blocos Dinâmicos (25/05/2026) ✅
- useBlocks.ts + useItems.ts
- BlockList + BlockCard + MeasureForm
- Formulário adaptativo m²/m³/m/km/un
- webkitdirectory + blob URLs + progress bar

### Sprint 2 — Integração Browser↔Backend (25/05/2026) ✅
- PreviewPanel reescrito com tabelas reais + thumbnails
- requestFile() → FileResponse → blob download automático

### Sprint 3 — PLANEJADO (próximo)
| Prioridade | Tarefa |
|------------|--------|
| 🔴 ALTA | Upload fotos via multipart/form-data → /generate-with-files |
| 🟡 MÉDIA | Testar contratos Trad end-to-end |
| 🟡 MÉDIA | items.json para c2056, c2057, c6122 |
| 🟡 MÉDIA | Detecção automática de medidas no nome do arquivo |

---

## 9. MAPA DE REAPROVEITAMENTO

### ✅ Usar sem modificação (maduro)
- `core/utils_sp.py` — parse_medidas_arquivo, formatar_moeda_texto
- `core/utils_sp2.py` — parse_medidas_sp2, detectar_item_por_pasta
- `c1565/scanner_sp2.py` + `word_builder_sp2.py` — testado end-to-end
- `core/word_utils.py` — placeholder system (70+ testes V3.2)

### ⚙️ Validar antes de usar
- `scanner.py` (trad) — migrado mas não testado no V5
- `scanner_sp.py` (c0908) — idem
- `formatar_descricao_tecnica` — verificar processamento de `<RED>` em word_utils_sp.py

### 🆕 Construir do Zero
- Upload fotos multipart → backend (Sprint 3)
- App desktop Tauri/Electron (root_path real)
- Dashboard histórico de relatórios
- Exportação PDF

### 🔍 Lógica Escondida Valiosa (portar para V5)
- `TM-MEUS-APPS/scratch/process_report.py` — parser DOCX completo, classify_table, consolidate, export_excel/docx
- `Legacy/extrair_itens_docx.py` — extrator de itens de .docx antigos (nunca portado)

---

## 10. ALERTAS E RISCOS

| # | Severidade | Alerta | Ação |
|---|-----------|--------|------|
| 1 | 🔴 ALTO | c0908 + c1507-c6122 não testados pós-migração | Rodar teste de geração para cada contrato |
| 2 | 🔴 ALTO | items.json vazio em c2056, c2057, c6122 | Solicitar planilhas ao Thiago |
| 3 | 🟡 MÉDIO | `<RED>` em formatar_descricao_tecnica pode não ser processado | Buscar handler em word_utils_sp.py |
| 4 | 🟡 MÉDIO | generator_app.py (modo app) sem testes | Verificar se deve ser migrado para V5 |
| 5 | 🟡 MÉDIO | Browser não fornece root_path → .docx sem fotos | Sprint 3: multipart upload |
| 6 | 🟡 MÉDIO | Blob URLs de thumbnails podem vazar memória | Verificar cleanup em useBlocks.ts |
| 7 | 🟢 BAIXO | FormularioDinamico_integration.tsx (V4) não verificado | Comparar antes de descartar |

---

## 📁 Estrutura de Arquivos V5

```
AutoRelatorio_V5/
├── INICIAR.bat
├── ENGENHARIA_REVERSA_COMPLETA.html     ← este relatório (versão visual)
├── ENGENHARIA_REVERSA_COMPLETA.md       ← este relatório (versão texto)
├── PROXIMO_PASSO.md                     ← guia rápido do Sprint 3
├── DIAGNOSTICO_PROXIMO_PASSO.md
├── RELATORIO_EXECUCAO_SPRINTS.md
├── backend/
│   ├── requirements.txt
│   ├── core/
│   │   ├── server.py            ← FastAPI main
│   │   ├── contract_engine.py   ← ABC
│   │   ├── registry.py          ← 9 engines
│   │   ├── word_utils.py
│   │   ├── word_utils_sp.py
│   │   ├── word_utils_sp2.py
│   │   ├── utils_sp.py
│   │   └── utils_sp2.py
│   └── contracts/
│       ├── c0908/  c1507/  c1565/  c2056/
│       ├── c2057/  c2626/  c2627/  c3575/  c6122/
│       └── [cada um]/
│           ├── engine/   ← engine.py + scanner*.py + word_builder*.py
│           ├── items/    ← items.json
│           └── template/ ← MODELO-XXXX.docx
└── frontend/
    ├── app/page.tsx
    ├── app/globals.css
    ├── components/
    │   ├── TopBar.tsx  Sidebar.tsx  EditorPanel.tsx
    │   ├── PreviewPanel.tsx  ResizableDivider.tsx  Toast.tsx
    │   ├── blocks/
    │   │   ├── BlockList.tsx  BlockCard.tsx  MeasureForm.tsx
    │   └── ui/  LoadingSpinner.tsx
    ├── hooks/
    │   ├── useBlocks.ts  useItems.ts  useFormData.ts
    │   ├── useContracts.ts  useSteps.ts  useApiState.ts  useTheme.ts
    ├── store/contractStore.ts
    └── lib/api.ts
```

---

*Engenharia reversa completa — 2026-05-26*
*AutoRelatório V5 — TM Sempre Tecnologia*
