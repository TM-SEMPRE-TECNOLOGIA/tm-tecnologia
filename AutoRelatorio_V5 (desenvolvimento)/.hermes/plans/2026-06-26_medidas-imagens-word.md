# Plano de Implementação: Medidas de Imagens → Aprovação → Word

> **Para o Hermes:** Use subagent-driven-development para implementar task por task.
> **Gerado:** 2026-06-26 · **Modelo legado V5 atual:** parcialmente funcional — imagens são inseridas no DOCX mas SEM medidas
> **Status atual do app:** Problemas para rodar — dependências, caminhos, e integração frontend↔backend quebrados

**Goal:** Fazer o fluxo completo funcionar: escanear fotos de pastas → preencher medidas no frontend → revisar/aprovar → gerar DOCX com cada imagem acompanhada de suas medidas (como texto puro OU caixa de texto) logo abaixo da foto.

**Architecture:** Pipeline de 4 estágios: (1) Scan de pastas local (backend), (2) UI de preenchimento e aprovação de medidas (frontend Step 2), (3) Serialização das medidas junto com as imagens no array `conteudo[]`, (4) Inserção no DOCX via python-docx com parágrafo de medidas abaixo de cada imagem.

**Tech Stack:** FastAPI + python-docx (backend) · Next.js 16 + React 19 + Zustand + Tailwind 4 (frontend) · Playwright (testes E2E) · TypeScript + Python 3.11+

---

## 0. DIAGNÓSTICO DOS MODELOS LEGADOS

### 0.1 Modelos de Contrato (9 variantes)

| ID | Nome | Modo | Scanner | Word Builder | Status |
|----|------|------|---------|-------------|--------|
| 0908 | São José dos Campos | SP | `scanner_0908.py` | `word_builder_0908.py` | ⚠️ Módulo não encontrado no disco |
| 1507 | Cuiabá | TRAD | `scanner_1507.py` | `word_builder_1507.py` | ⚠️ Sem engine/ (só items+template) |
| 1565 | SJRP/Ribeirão Preto | SP2 | `scanner_1565.py` | `word_builder_1565.py` | ⚠️ Módulo não encontrado no disco |
| 2056 | Divinópolis | TRAD | `scanner_2056.py` | `word_builder_2056.py` | ⚠️ Sem engine/ |
| 2057 | Varginha | TRAD | `scanner_2057.py` | `word_builder_2057.py` | ⚠️ Módulo não encontrado |
| 2626 | Salinas | TRAD | `scanner_2626.py` ✅ | `word_builder_2626.py` ✅ | ✅ Completo mas sem medidas |
| 2627 | Gov. Valadares | TRAD | `scanner_2627.py` | `word_builder_2627.py` | ⚠️ Módulo não encontrado |
| 3575 | Tangará da Serra | TRAD | `scanner_3575.py` | `word_builder_3575.py` | ⚠️ Sem engine/ |
| 6122 | Mato Grosso do Sul | TRAD | `scanner_6122.py` ✅ | `word_builder_6122.py` ✅ | ✅ Completo mas sem medidas |

**Diagnóstico:** Apenas 2 de 9 contratos (2626 e 6122) têm módulos `engine/` completos com scanner + word_builder. Os outros 7 têm apenas `items/` e `template/`. O `registry.py` importa todos os 9 — qualquer inicialização do backend vai quebrar com `ModuleNotFoundError`.

### 0.2 Funcionamento Atual dos Scanners

**Padrão comum (2626/6122):**
```python
# O que o scanner produz hoje:
conteudo = [
    "Área externa",                    # str = título de seção
    {"imagem": "C:/fotos/01.jpg"},     # dict = caminho da imagem
    {"imagem": "C:/fotos/02.jpg"},
    {"quebra_pagina": True},           # quebra de página
    "»1 - Pintura",                    # subseção
    {"imagem": "C:/fotos/03.jpg"},
]
```

**O que falta:** As imagens são inseridas no DOCX **sem nenhuma legenda ou medida**. O scanner não tem acesso aos dados de medidas que o usuário preenche no frontend.

### 0.3 Funcionamento Atual dos Word Builders

- `word_utils.inserir_conteudo()` (modo Tradicional): apenas insere imagens com `add_picture()`, centraliza, e coloca quebras de página. **Zero suporte a texto de medidas.**
- `word_utils_sp2.inserir_conteudo_sp2()` (modo SP2): insere imagens, croquis com legendas, tabelas de memória de cálculo. Já tem o conceito de legenda abaixo da imagem (`_inserir_imagem` + parágrafo de texto), mas **não recebe medidas do frontend**.

### 0.4 Frontend — O Que Já Existe

- `useBlocks.ts`: Hook completo com `Bloco` (foto + item + medidas + total), `calcularTotal()`, `consolidar()` ✅
- `BlockCard.tsx`: Card com thumbnail, dropdown de item, formulário de medidas ✅
- `MeasureForm.tsx`: Formulário adaptativo por unidade (m² → Larg+Alt+Faces+Desc; m³ → Larg+Alt+Prof; m → Comp; un → Qtd) ✅
- `EditorPanel.tsx`: 3 passos (Cabeçalho → Blocos → Gerar) ✅

**O gap:** O Step 2 preenche medidas, mas ao clicar "Gerar" no Step 3, **as medidas NUNCA são enviadas ao backend**. O `GenerateFlatRequest` não tem campo para blocos/medidas.

### 0.5 Por que o App Não Roda

1. **Backend:** 7 de 9 contratos sem módulo `engine/` → `ModuleNotFoundError` no `registry.py`
2. **Frontend:** `npm run dev` pode falhar por dependências desatualizadas (Next.js 16.1.6 pode ter breaking changes)
3. **Integração:** Fotos nunca chegam ao backend (só ficam como `File` no browser)
4. **CORS:** OK em dev (`allow_origins=["*"]`)

---

## 1. ARQUITETURA PROPOSTA PARA O FLUXO DE MEDIDAS

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FLUXO COMPLETO                              │
│                                                                    │
│  [Usuário]                                                         │
│     │                                                              │
│     ├─1─ Seleciona contrato (Sidebar)                              │
│     ├─2─ Preenche cabeçalho OS (Step 1)                            │
│     ├─3─ Seleciona pasta de fotos (Step 2 - input webkitdirectory) │
│     │     └─ Frontend monta Bloco[] com previewUrl                 │
│     ├─4─ Para cada foto: escolhe item + preenche medidas           │
│     │     └─ MeasureForm → largura, altura, faces, desconto...     │
│     ├─5─ Revisa no Preview Panel (medidas visíveis ao lado)        │
│     ├─6─ Clica "Gerar .docx" (Step 3)                             │
│     │     └─ Envia FormData (multipart) com JSON + imagens         │
│     │                                                              │
│  [Backend FastAPI :5000]                                           │
│     │                                                              │
│     ├─ POST /generate-v2                                           │
│     │   ├─ Recebe: meta (JSON) + blocos (JSON) + imagens (bin)     │
│     │   ├─ Valida contrato, itens, medidas                         │
│     │   ├─ Monta conteudo[] enriquecido COM MEDIDAS                │
│     │   │   └─ {"imagem": path,                                    │
│     │   │       "medidas": {"largura": 3.5, "altura": 2.8,        │
│     │   │                    "faces": 2, "total": 19.6},           │
│     │   │       "item": {"codigo": "17.6", "unidade": "m²"}}      │
│     │   ├─ Chama engine.build_word_v2(tpl, conteudo_enriquecido)  │
│     │   └─ Retorna FileResponse(.docx)                             │
│     │                                                              │
│  [Word Builder — python-docx]                                      │
│     │                                                              │
│     ├─ Substitui placeholders {{nr_os}}, {{ag_cod}}...             │
│     ├─ Para cada item do conteudo[]:                               │
│     │   ├─ Se {"imagem": ..., "medidas": {...}}:                  │
│     │   │   ├─ Insere imagem (10cm altura Trad/SP, 7cm SP2)       │
│     │   │   └─ Insere parágrafo abaixo com medidas formatadas      │
│     │   │      (OPÇÃO A: texto puro "3,50 × 2,80 = 9,80 m²")     │
│     │   │      (OPÇÃO B: caixa de texto/tabela 1x1 com borda)     │
│     │   ├─ Se string: título de seção                              │
│     │   └─ Se {"quebra_pagina": True}: page break                  │
│     └─ Salva .docx → retorna ao frontend                           │
│                                                                    │
│  [Usuário]                                                         │
│     └─ Download automático do .docx gerado                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. PLANO DE IMPLEMENTAÇÃO (TASK-BY-TASK)

### 🔧 FASE A — REPARO DOS MODELOS LEGADOS (pré-requisito)

#### Task A1: Scaffold dos 7 contratos faltantes
**Objective:** Criar `engine/` para c0908, c1507, c1565, c2056, c2057, c2627, c3575 para o backend iniciar sem `ModuleNotFoundError`.

**Files:**
- Criar: `backend/contracts/c0908/engine/engine.py` + `scanner_0908.py` + `word_builder_0908.py`
- Criar: `backend/contracts/c1507/engine/engine.py` + `scanner_1507.py` + `word_builder_1507.py`
- Criar: `backend/contracts/c1565/engine/engine.py` + `scanner_1565.py` + `word_builder_1565.py`
- Criar: `backend/contracts/c2056/engine/engine.py` + `scanner_2056.py` + `word_builder_2056.py`
- Criar: `backend/contracts/c2057/engine/engine.py` + `scanner_2057.py` + `word_builder_2057.py`
- Criar: `backend/contracts/c2627/engine/engine.py` + `scanner_2627.py` + `word_builder_2627.py`
- Criar: `backend/contracts/c3575/engine/engine.py` + `scanner_3575.py` + `word_builder_3575.py`

**Approach:** Clonar o padrão de c2626 para cada contrato TRAD. Para c0908 (SP) e c1565 (SP2), clonar com referências aos utilitários SP/SP2 existentes.

**Step 1:** Para cada contrato TRAD (1507, 2056, 2057, 2627, 3575):
```python
# contracts/cXXXX/engine/scanner_XXXX.py
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

ORDEM_PASTAS = ["- Área externa", "- Área interna", "- Segundo piso"]

def folder_sort_key(name: str):
    name_lower = name.lower()
    if "vista ampla" in name_lower: return (0, name_lower)
    match = re.match(r'^(\d+)(.*)', name)
    if match: return (1, int(match.group(1)), match.group(2))
    if "detalhes" in name_lower: return (3, name_lower)
    return (2, name_lower)

def build_content_from_root(pasta_raiz, log_errors_path, logger=lambda _: None):
    # ... mesmo código de scanner_2626.py
```
```python
# contracts/cXXXX/engine/word_builder_XXXX.py
from word_utils import inserir_conteudo as _inserir_conteudo

def inserir_conteudo(modelo_path, conteudo, output_path, meta=None):
    _inserir_conteudo(modelo_path=modelo_path, conteudo=conteudo, output_path=output_path, meta=meta)
    return output_path
```

**Step 2:** Para c0908 (SP) e c1565 (SP2), criar wrappers apontando para `word_utils_sp` / `word_utils_sp2`.

**Step 3:** Verificar que `registry.py` não quebra:
```bash
cd backend && python -c "from core.registry import list_contracts; print(len(list_contracts()))"
# Esperado: 9
```

#### Task A2: Corrigir imports e caminhos do backend
**Objective:** Garantir que `python -m uvicorn core.server:app --port 5000` sobe sem erros.

**Files:** `backend/core/server.py`, `backend/core/registry.py`, `backend/core/word_utils.py`

**Step 1:** Verificar se `sys.path` manipulation nos wrappers está correto
**Step 2:** Testar health endpoint:
```bash
curl http://localhost:5000/health
# Esperado: {"status": "ok", "version": "5.0.0"}
```

---

### 🔧 FASE B — NOVO ENDPOINT DE GERAÇÃO COM MEDIDAS

#### Task B1: Novo modelo Pydantic `GenerateV2Request`
**Objective:** Criar o payload que recebe blocos com medidas do frontend.

**File:** Modificar `backend/core/server.py`

```python
from pydantic import BaseModel
from typing import Optional, List

class BlocoMedida(BaseModel):
    nome: str                          # "01 - 3,50 x 2,80"
    pasta: str                         # "Área externa / 1 - Pintura"
    item_codigo: str                   # "17.6"
    item_descricao: str                # "Pintura acrílica..."
    unidade: str                       # "m²"
    medidas: dict                      # {"largura": 3.5, "altura": 2.8, "faces": 2, "desconto": 0}
    total: float                       # 19.6
    # imagem será enviada como multipart file separado

class GenerateV2Request(BaseModel):
    contrato_id: str
    nr_os: str
    ag_cod: str
    ag_nome: str
    dt_atend: str
    endereco: Optional[str] = ""
    responsavel: Optional[str] = ""
    desc_index: Optional[str] = "1"
    modo: Optional[str] = "sp2"
    blocos: List[BlocoMedida]          # NOVO: array de blocos com medidas
```

#### Task B2: Implementar `POST /generate-v2` (multipart)
**Objective:** Receber JSON + imagens binárias, salvar em temp, montar `conteudo[]` enriquecido, gerar DOCX.

**File:** Modificar `backend/core/server.py`

```python
from fastapi import File, UploadFile, Form
import json, tempfile, shutil

@app.post("/generate-v2")
async def generate_v2(
    meta_json: str = Form(...),        # JSON string do GenerateV2Request
    imagens: List[UploadFile] = File(...),  # arquivos binários
):
    import os, pathlib, datetime
    
    meta = json.loads(meta_json)
    engine = get_engine(meta["contrato_id"])
    
    # Salva imagens em diretório temporário
    tmpdir = tempfile.mkdtemp(prefix="autorelatorio_")
    saved_paths = []
    for img in imagens:
        path = os.path.join(tmpdir, img.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(img.file, f)
        saved_paths.append(path)
    
    # Monta conteudo[] enriquecido COM MEDIDAS
    conteudo = _montar_conteudo_com_medidas(meta["blocos"], saved_paths)
    
    # Template
    tpl = pathlib.Path(__file__).parent.parent / "contracts" / f"c{meta['contrato_id']}" / "template" / engine.template_file
    
    # Gera
    output_path = str(pathlib.Path(__file__).parent.parent / "output" / f"Relatorio-OS{meta['nr_os']}-{meta['ag_cod']}.docx")
    output = engine.build_word_v2(str(tpl), conteudo, output_path, meta)
    
    # Limpa temp
    shutil.rmtree(tmpdir, ignore_errors=True)
    
    return FileResponse(output, filename=os.path.basename(output))
```

#### Task B3: Função `_montar_conteudo_com_medidas()`
**Objective:** Transformar `BlocoMedida[]` + caminhos de imagem no `conteudo[]` enriquecido.

**File:** Criar `backend/core/conteudo_builder.py`

```python
def montar_conteudo_com_medidas(blocos: list[dict], image_paths: list[str]) -> list:
    """
    Transforma BlocoMedida[] + image_paths em conteudo[] compatível
    com o word builder, MAS com campo 'medidas' em cada imagem.
    
    Estrutura de pastas inferida dos nomes:
      "Área externa / 1 - Pintura / 01 - desc.jpg"
      → seções: "Área externa" > "»1 - Pintura"
    """
    conteudo = []
    ultima_secao = None
    
    for bloco, img_path in zip(blocos, image_paths):
        partes = bloco["pasta"].split(" / ")
        
        # Insere títulos de seção quando mudam
        for i, sec in enumerate(partes):
            prefixo = "»" * i
            secao_key = f"{prefixo}{sec}"
            if secao_key != ultima_secao:
                conteudo.append(secao_key)
                ultima_secao = secao_key
        
        # Insere imagem COM medidas
        conteudo.append({
            "imagem": img_path,
            "medidas": bloco["medidas"],
            "item": {
                "codigo": bloco["item_codigo"],
                "descricao": bloco["item_descricao"],
                "unidade": bloco["unidade"],
            },
            "total": bloco["total"],
            "nome_arquivo": bloco["nome"],
        })
    
    return conteudo
```

---

### 🔧 FASE C — WORD BUILDER COM MEDIDAS (TEXTO ABAIXO DA IMAGEM)

#### Task C1: Nova função `inserir_conteudo_v2()` no `word_utils.py`
**Objective:** Modificar `inserir_conteudo()` para detectar `{"imagem": ..., "medidas": {...}}` e adicionar parágrafo de medidas abaixo da imagem.

**File:** Modificar `backend/core/word_utils.py` (adicionar após linha ~520)

```python
def _inserir_paragrafo_medidas(doc, paragrafo_ref, medidas: dict, item: dict, total: float, nome: str):
    """
    Insere um parágrafo formatado abaixo da imagem com as medidas.
    
    OPÇÃO A — Texto puro:
      "3,50 × 2,80 m — Faces: 2 — Total: 19,60 m²"
    
    OPÇÃO B — Caixa de texto (tabela 1×1 com borda):
      ┌─────────────────────────────────┐
      │ 3,50 × 2,80 m | Faces: 2       │
      │ Total: 19,60 m²                 │
      └─────────────────────────────────┘
    """
    from docx.shared import Cm, Pt, RGBColor
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    
    unidade = item.get("unidade", "m²")
    codigo = item.get("codigo", "")
    desc = item.get("descricao", "")
    
    # Monta texto da medida
    partes = []
    if "largura" in medidas and "altura" in medidas:
        partes.append(f"{medidas['largura']:.2f} × {medidas['altura']:.2f} m")
    if "comp" in medidas and medidas["comp"] > 0:
        partes.append(f"{medidas['comp']:.2f} m")
    if "quantidade" in medidas and medidas["quantidade"] > 0:
        partes.append(f"Qtd: {medidas['quantidade']:.0f}")
    if medidas.get("faces", 1) > 1:
        partes.append(f"Faces: {medidas['faces']}")
    if medidas.get("desconto", 0) > 0:
        partes.append(f"Desc: {medidas['desconto']:.2f} m²")
    partes.append(f"Total: {total:.2f} {unidade}")
    
    texto_medida = " | ".join(partes)
    
    # --- OPÇÃO A: Texto puro (mais simples) ---
    p = paragrafo_ref.insert_paragraph_before(texto_medida)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    for run in p.runs:
        run.font.size = Pt(9)
        run.font.name = 'Arial'
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)  # cinza escuro
    
    # --- OPÇÃO B: Caixa de texto (tabela 1×1) ---
    # (ativar conforme preferência do usuário)
    # tbl = doc.add_table(rows=1, cols=1)
    # tbl.style = 'Table Grid'
    # cell = tbl.cell(0, 0)
    # cell.text = f"{codigo} — {desc}\n{texto_medida}"
    # paragrafo_ref._p.addnext(tbl._tbl)
```

#### Task C2: Modificar `inserir_conteudo()` para chamar `_inserir_paragrafo_medidas()`
**Objective:** No loop principal do `inserir_conteudo()`, após inserir cada imagem, verificar se há `medidas` e adicionar o parágrafo.

**File:** Modificar `backend/core/word_utils.py` (linhas ~493-520)

No trecho onde imagens são inseridas:
```python
# Antes (linha ~518):
p.add_run().add_picture(grupo[sub_i], width=Cm(tw))
contador_imagens += 1

# Depois:
p.add_run().add_picture(grupo[sub_i], width=Cm(tw))
contador_imagens += 1

# NOVO: Se o item original tinha medidas, insere parágrafo abaixo
item_original = conteudo[idx_original]  # precisa rastrear índice
if isinstance(item_original, dict) and "medidas" in item_original:
    _inserir_paragrafo_medidas(
        doc, p,
        medidas=item_original["medidas"],
        item=item_original.get("item", {}),
        total=item_original.get("total", 0),
        nome=item_original.get("nome_arquivo", "")
    )
```

#### Task C3: Versão SP2 — `inserir_conteudo_sp2_v2()`
**Objective:** Mesma lógica para o modo SP2 (contrato 1565), que já tem suporte a legendas.

**File:** Modificar `backend/core/word_utils_sp2.py`

No trecho `elif isinstance(item, dict) and "imagem" in item:` (~linha 365):
```python
elif isinstance(item, dict) and "imagem" in item:
    if _inserir_imagem(doc, p_ref, item["imagem"]):
        contador_imagens += 1
    # NOVO: Se tem medidas, insere legenda de medidas
    if "medidas" in item:
        _inserir_legenda_medidas_sp2(doc, p_ref, item)
```

---

### 🔧 FASE D — FRONTEND: ENVIO DAS MEDIDAS AO BACKEND

#### Task D1: Novo método `generateReportV2()` em `lib/api.ts`
**Objective:** Enviar FormData com JSON de metadados + arquivos de imagem.

**File:** Modificar `frontend/lib/api.ts`

```typescript
export async function generateReportV2(
  meta: GenerateV2Payload,
  blocos: Bloco[]
): Promise<void> {
  const formData = new FormData();
  
  // Meta como JSON string
  const metaJson = {
    contrato_id: meta.contrato_id,
    nr_os: meta.nr_os,
    ag_cod: meta.ag_cod,
    ag_nome: meta.ag_nome,
    dt_atend: meta.dt_atend,
    endereco: meta.endereco,
    responsavel: meta.responsavel,
    desc_index: meta.desc_index,
    modo: meta.modo,
    blocos: blocos.map(b => ({
      nome: b.nome,
      pasta: b.pasta,
      item_codigo: b.item?.codigo ?? '',
      item_descricao: b.item?.descricao ?? '',
      unidade: b.item?.unidade ?? '',
      medidas: { ...b.medidas },
      total: b.total,
    })),
  };
  
  formData.append('meta_json', JSON.stringify(metaJson));
  
  // Adiciona cada imagem como arquivo binário
  for (const bloco of blocos) {
    formData.append('imagens', bloco.arquivo, bloco.arquivo.name);
  }
  
  const response = await fetch(`${BASE_URL}/generate-v2`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Erro ao gerar relatório');
  }
  
  // Download do blob
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Relatorio-OS${meta.nr_os}-${meta.ag_cod}.docx`;
  a.click();
  URL.revokeObjectURL(url);
}
```

#### Task D2: Conectar `page.tsx` ao novo endpoint
**Objective:** No `handleGenerate()` do Step 3, chamar `generateReportV2()` em vez de `generateReport()`.

**File:** Modificar `frontend/app/page.tsx`

```typescript
// Antes:
const handleGenerate = async () => {
  await generateReport({ contrato_id, nr_os, ... });
};

// Depois:
const handleGenerate = async () => {
  await generateReportV2(
    { contrato_id, nr_os, ag_cod, ag_nome, dt_atend, endereco, responsavel, desc_index, modo },
    blocos  // do useBlocks()
  );
};
```

---

### 🔧 FASE E — UI DE APROVAÇÃO DE MEDIDAS (PREVIEW)

#### Task E1: Exibir medidas no PreviewPanel durante Step 2
**Objective:** O painel direito deve mostrar cada foto com suas medidas calculadas ANTES de gerar, para aprovação visual.

**File:** Modificar `frontend/components/PreviewPanel.tsx`

Adicionar seção no preview que itera sobre `consolidado` e mostra:
```tsx
{consolidado.map(grupo => (
  <div key={`${grupo.pasta}-${grupo.item.codigo}`} className="preview-consolidado">
    <h4>{grupo.item.codigo} — {grupo.item.descricao}</h4>
    <p className="preview-pasta">{grupo.pasta}</p>
    <table className="preview-tabela-medidas">
      <thead>
        <tr>
          <th>Foto</th>
          <th>Medidas</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        {grupo.blocos.map(b => (
          <tr key={b.id}>
            <td>
              <img src={b.previewUrl} alt={b.nome} className="preview-thumb" />
              <span>{b.nome}</span>
            </td>
            <td>{formatarMedidas(b.medidas, b.item?.unidade)}</td>
            <td className="preview-total">{b.total.toFixed(2)} {b.item?.unidade}</td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr>
          <td colSpan={2}>Total do grupo</td>
          <td className="preview-total">{grupo.total.toFixed(2)} {grupo.item.unidade}</td>
        </tr>
      </tfoot>
    </table>
  </div>
))}
```

---

### 🔧 FASE F — TESTES COM PLAYWRIGHT

#### Task F1: Instalar e configurar Playwright
```bash
cd frontend
npm install -D @playwright/test
npx playwright install chromium
```

#### Task F2: Criar teste E2E do fluxo completo

**File:** Criar `frontend/e2e/fluxo-medidas.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Fluxo de Medidas → Aprovação → Geração DOCX', () => {
  
  test('Step 1: Preenche cabeçalho e vê preview atualizar', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Seleciona contrato
    await page.click('text=2626');
    await expect(page.locator('.topbar-contract-name')).toContainText('Salinas');
    
    // Preenche formulário Step 1
    await page.fill('input[name="nr_os"]', '1753');
    await page.fill('input[name="ag_cod"]', '1234-5');
    await page.fill('input[name="ag_nome"]', 'Agência Centro');
    await page.fill('input[name="dt_atend"]', '2026-06-26');
    
    // Preview deve mostrar valores
    await expect(page.locator('.preview-doc')).toContainText('1753');
    await expect(page.locator('.preview-doc')).toContainText('1234-5');
  });
  
  test('Step 2: Seleciona fotos, preenche medidas, vê totais', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=2626');
    
    // Avança para Step 2
    await page.click('button:has-text("Próximo")');
    
    // Seleciona pasta de fotos (mock com fixtures)
    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.click('button:has-text("Selecionar Pasta")');
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles([
      './e2e/fixtures/foto-01.jpg',
      './e2e/fixtures/foto-02.jpg',
    ]);
    
    // Verifica que os blocos apareceram
    await expect(page.locator('.block-card')).toHaveCount(2);
    
    // Seleciona item no primeiro bloco
    await page.locator('.block-card').first().locator('select').selectOption('17.6');
    
    // Preenche medidas
    await page.locator('.block-card').first().locator('input[placeholder="0"]').first().fill('3.50');
    await page.locator('.block-card').first().locator('input[placeholder="0"]').nth(1).fill('2.80');
    
    // Verifica total calculado (3.50 × 2.80 = 9.80)
    await expect(page.locator('.block-total-pill').first()).toContainText('9,80');
  });
  
  test('Step 3: Preview de aprovação mostra medidas antes de gerar', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.click('text=2626');
    
    // Setup completo...
    // ... (preenche Step 1 e 2 como acima)
    
    // Avança para Step 3
    await page.click('button:has-text("Próximo")');
    
    // Preview deve mostrar tabela de medidas para aprovação
    await expect(page.locator('.preview-consolidado')).toBeVisible();
    await expect(page.locator('.preview-tabela-medidas')).toBeVisible();
    await expect(page.locator('.preview-total')).toContainText('9,80');
  });
  
  test('Geração: clica Gerar e recebe download', async ({ page }) => {
    // Mock da API para evitar dependência do backend
    await page.route('**/generate-v2', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        body: Buffer.from('mock-docx-content'),
      });
    });
    
    await page.goto('http://localhost:3000');
    // ... setup completo ...
    
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('button:has-text("Gerar .docx")'),
    ]);
    
    expect(download.suggestedFilename()).toContain('Relatorio-OS1753-1234-5.docx');
  });
  
  test('Validação: não gera sem medidas preenchidas', async ({ page }) => {
    await page.goto('http://localhost:3000');
    // ... vai direto para Step 3 sem preencher ...
    
    await expect(page.locator('button:has-text("Gerar .docx")')).toBeDisabled();
    await expect(page.locator('.toast-error')).toContainText('Preencha as medidas');
  });
});
```

#### Task F3: Criar fixtures de teste

**File:** Criar `frontend/e2e/fixtures/` com 2 imagens JPEG de teste (geradas programaticamente ou placeholder)

---

### 🔧 FASE G — REPARO FINAL DO APP

#### Task G1: Verificar e corrigir `frontend/package.json`
```bash
cd frontend
npm install       # reinstalar dependências
npm run dev       # deve subir em :3000
```

#### Task G2: Criar script `INICIAR.bat` funcional
**File:** Modificar `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5 (desenvolvimento)\INICIAR.bat`

Garantir que:
1. Ativa o Python correto (python 3.11+)
2. `pip install -r backend/requirements.txt` (se necessário)
3. Inicia backend em porta 5000
4. Inicia frontend em porta 3000
5. Abre navegador em http://localhost:3000

---

## 3. COMPARAÇÃO: OPÇÃO A (TEXTO PURO) vs OPÇÃO B (CAIXA DE TEXTO)

| Aspecto | Texto Puro (Recomendado) | Caixa de Texto (Tabela) |
|---------|--------------------------|-------------------------|
| Complexidade | Baixa | Média |
| Aparência no Word | Discrição profissional | Destaque visual |
| Edição pós-geração | Fácil (parágrafo normal) | Média (célula de tabela) |
| Alinhamento com foto | Sempre centralizado | Pode desalinhar |
| Compatibilidade | 100% | 100% |
| Uso nos templates BB | Padrão | Não usado atualmente |
| **Recomendação** | ✅ Adotar como padrão | Feature toggle (preferência do usuário) |

---

## 4. RISCOS E MITIGAÇÕES

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| 7 contratos sem módulo engine | **CRÍTICO** | Task A1 — scaffold completo |
| Imagens grandes causam timeout no upload | **ALTO** | Comprimir no frontend (canvas resize) antes do envio |
| Medidas inconsistentes (ex: largura sem altura em m²) | **MÉDIO** | Validação no backend antes de gerar |
| Template Word sem `{{start_here}}` | **BAIXO** | Fallback: insere no final do documento |
| Playwright não acessa `webkitdirectory` nativamente | **MÉDIO** | Usar `page.setInputFiles()` com override |

---

## 5. VERIFICAÇÃO FINAL

```bash
# 1. Backend sobe?
curl http://localhost:5000/health
# → {"status": "ok", "version": "5.0.0"}

# 2. Lista contratos?
curl http://localhost:5000/api/contracts
# → 9 contratos

# 3. Geração com medidas?
curl -X POST http://localhost:5000/generate-v2 \
  -F 'meta_json={"contrato_id":"2626","nr_os":"1753",...}' \
  -F 'imagens=@foto01.jpg' \
  -F 'imagens=@foto02.jpg' \
  -o teste.docx
# → Arquivo .docx com imagens + texto de medidas abaixo

# 4. Frontend?
# Abrir http://localhost:3000 → UI carrega sem erros no console

# 5. Playwright?
cd frontend && npx playwright test e2e/fluxo-medidas.spec.ts
# → 5 testes passam
```

---

## 6. ORDEM DE EXECUÇÃO (DEPENDÊNCIAS)

```
A1 (scaffold contratos)
  └─ A2 (backend sobe)
       └─ B1, B2, B3 (novo endpoint)
            └─ C1, C2, C3 (word builder com medidas)
                 └─ D1, D2 (frontend envia medidas)
                      └─ E1 (preview de aprovação)
                           └─ F1, F2, F3 (testes Playwright)
                                └─ G1, G2 (reparo final)

Tarefas independentes (paralelizáveis):
  - C1/C2/C3 podem começar junto com B1/B2/B3
  - E1 pode começar junto com D1/D2
  - F1 pode começar a qualquer momento
```

---

*Plano completo. Pronto para execução com subagent-driven-development.*
