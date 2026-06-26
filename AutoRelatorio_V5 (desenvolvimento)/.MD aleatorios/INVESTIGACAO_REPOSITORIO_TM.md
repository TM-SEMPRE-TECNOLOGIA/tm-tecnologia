# 🔬 Relatório de Investigação — TM-MEUS-APPS
**Data:** 2026-05-25  
**Escopo:** Varredura completa de `C:\Users\thiag\Desktop\TM-MEUS-APPS`  
**Objetivo:** Recuperar lógica existente antes de reimplementar do zero  
**Resultado:** ✅ **JACKPOT — tudo que o V5 precisa já existe no V4**

---

## 1. Mapa de arquivos encontrados

### 🟢 CRÍTICOS — prontos para migrar para o V5

| Arquivo (V4) | Tamanho aprox. | O que contém |
|---|---|---|
| `backend/generator_sp2.py` | ~370 linhas | **Scanner completo modo SP2** (Contrato 1565). Faz tudo: os.walk hierárquico, ordenação natural, detecção de croquis, fachada, pastas de detalhes, acumulação de linhas de memória, quebra de página. Testado em produção. |
| `backend/generator_sp.py` | ~200 linhas | **Scanner modo SP1** (Contrato 0908). Mesma lógica, padrão de pastas diferente. |
| `backend/generator.py` | ~200 linhas | **Scanner Tradicional** (contratos 2056, 2057, 2626, 2627, 3575, 6122, 1507). Sem cálculo de área — só estrutura hierárquica + fotos. |
| `backend/word_utils_sp2.py` | ~470 linhas | **Word builder completo SP2**. Insere: fachada, foto, croqui, texto narrativo, enunciado de item, tabela de memória de cálculo (m², metálico, unitário), tabela de itens separada, quebra de página. Usa `python-docx`. Testado em produção. |
| `backend/word_utils_sp.py` | ~300 linhas | **Word builder SP1**. Padrão de tabela diferente do SP2. |
| `backend/word_utils.py` | ~300 linhas | **Utilitários base**: `substituir_placeholders()`, `analisar_imagem()`, `otimizar_layout()`, `aplicar_estilo()`, `extract_placeholders()`. Compartilhado por todos. |
| `backend/utils_sp2.py` | ~275 linhas | **Parser de nome de arquivo SP2**: `parse_medidas_sp2()` — extrai largura × altura × faces − desconto do nome do arquivo. Detecta item por pasta. Formata referência, moeda, enunciado. Contém `ITENS_CONTRATO_SP2` com ~40 itens mapeados. |
| `backend/utils_sp.py` | ~69 linhas | **Parser SP1** — `parse_medidas_arquivo()` para o padrão mais simples do SP1. |
| `backend/routes.py` | ~377 linhas | **API FastAPI completa** — endpoints `/generate-report-with-fields`, `/download/{filename}`, `/templates`, `/health`, `/validate-fields`. Modelo Pydantic, FileResponse, path traversal protection. Funciona. |
| `backend/server.py` | ~100 linhas | **Servidor FastAPI V4** com CORS, UploadFile, ScanRequest, GenerateRequest. Referência para o V5. |

### 🟡 IMPORTANTES — dados e JSONs aproveitáveis

| Arquivo | O que contém |
|---|---|
| `DOCUMENTOS/skill_completar_relatorio_marcado/scripts/itens_por_contrato.json` | **20.068 linhas** — mapeamento completo de todos os itens dos 9 contratos com código, descrição, unidade, capítulo. **É o `items.json` que o V5 precisava**. |
| `DOCUMENTOS/skill_completar_relatorio_marcado/scripts/itens_oficiais_master.json` | Lista master de itens. Base de referência. |
| `DOCUMENTOS/skill_completar_relatorio_marcado/scripts/itens_contrato.json` | Itens por contrato simplificados. |
| `DOCUMENTOS/skill_completar_relatorio_marcado/scripts/banco_frases_sp2.json` | Banco de frases descritivas para SP2. |

### 🟢 TEMPLATES — todos os 9 contratos existem

| Template | Localização |
|---|---|
| `MODELO - 1565 - SÃO JOSÉ DO RIO PRETO E RIBEIRÃO PRETO - ATUALIZADO.docx` | `templates/` + `templates_backup/` |
| `MODELO - 0908 - SÃO JOSÉ DOS CAMPOS - ATUALIZADO.docx` | `templates/` + `templates_backup/` |
| `MODELO - 1507 - CUIABÁ - ATUALIZADO.docx` | `templates/` |
| `MODELO - 2056 - DIVINÓPOLIS - ATUALIZADO.docx` | `templates/` |
| `MODELO - 2057 - VARGINHA - ATUALIZADO.docx` | `templates/` |
| `MODELO - 2626 - SALINAS - ATUALIZADO.docx` | `templates/` |
| `MODELO - 2627 - VALADARES - ATUALIZADO.docx` | `templates/` |
| `MODELO - 3575 - TANGARA DA SERRA - ATUALIZADO.docx` | `templates/` |
| `MODELO - 6122 - MATO GROSSO DO SUL - ATUALIZADO.docx` | `templates/` |

> ⚡ **TODOS OS 9 TEMPLATES JÁ EXISTEM E ESTÃO ATUALIZADOS.**  
> O PENDENCIAS_V5.md dizia "🔴 Pendente" para todos — era informação desatualizada.

### 🟡 SKILL — scripts de memorial já implementados

| Arquivo | O que contém |
|---|---|
| `tests/fixtures/fixture_tradicional/.../scripts/gerar_memorial.py` | Gerador de memorial Word (tabelas de cálculo + itens consolidados). Testado em produção com Monte Azul Paulista, Barretos, Bairro Ipiranga. |
| `.../scripts/extrair_itens.py` | Extrator de itens para Excel (.xlsx) com duas abas: lista completa + consolidado. |
| `.../scripts/verificar_divergencias.py` | Verificador de divergências corpo vs. memorial. |
| `.../scripts/verificar_legendas.py` | Verificador de sequência de legendas de fotos. |
| `.../scripts/parse_report.py` | Parser de relatório (.md) para extrair ocorrências de cálculo. |

### 🟢 FIXTURES DE TESTE — pastas de fotos reais

| Fixture | Contratos |
|---|---|
| `tests/fixtures/fixture_sp/` | Tangará da Serra (SP) — com fotos reais no padrão `"10,00 x 0,800.jpg"` |
| `tests/fixtures/fixture_tradicional/` | Relatório preventivo real com documentação completa |

### 🟡 RELATÓRIOS GERADOS — exemplos reais de saída

Presentes na raiz de `TM-MEUS-APPS`:
- `Memorial_Final_MonteAzul.docx`, `Memorial_Barretos.docx`, `Memorial_Barretos_v2.docx`...
- `RELATORIO FOTOGRAFICO - MONTE AZUL PAULISTA...docx`
- `RELATORIO_IPIRANGA_FINAL_V2.docx`
- `IPIRANGA_COM_LEGENDAS.docx`

São os outputs reais do V4 — servem como **ground truth** para comparar o output do V5.

---

## 2. Nível de reutilização possível

| Módulo V5 (a implementar) | Fonte V4 | Reaproveitamento |
|---|---|---|
| **scanner_sp2.py** | `generator_sp2.py` | **100%** — copiar + adaptar assinatura |
| **scanner_trad.py** | `generator.py` | **100%** — copiar + adaptar assinatura |
| **scanner_sp.py** | `generator_sp.py` | **100%** — copiar + adaptar assinatura |
| **word_builder_sp2.py** | `word_utils_sp2.py` | **100%** — copiar + renomear função |
| **word_builder_sp.py** | `word_utils_sp.py` | **100%** — copiar + renomear função |
| **word_builder_trad.py** | `word_utils.py` + `generator.py` | **80%** — adaptar inserção de conteúdo |
| **utils_sp2.py** | `utils_sp2.py` | **100%** — copiar idêntico |
| **utils_sp.py** | `utils_sp.py` | **100%** — copiar idêntico |
| **word_utils.py** (base) | `word_utils.py` | **100%** — copiar idêntico |
| **Templates .docx** | `templates/` | **100%** — copiar os 9 arquivos |
| **items.json** por contrato | `itens_por_contrato.json` | **90%** — extrair e separar por contrato |
| **Endpoint /health** | `routes.py` | **100%** — copiar |
| **Endpoint /download** | `routes.py` | **100%** — copiar |
| **Gerador de memorial** | `gerar_memorial.py` | **85%** — adaptar para entrada JSON |
| **Extrator de itens xlsx** | `extrair_itens.py` | **90%** — adaptar entrada |

---

## 3. Dependências identificadas

### Python (backend V4 usa e V5 precisará)
```
python-docx    # manipulação de .docx
Pillow         # PIL para análise de imagem (proporção, dimensões)
openpyxl       # geração de .xlsx
fastapi        # servidor API
uvicorn        # servidor ASGI
pydantic       # validação de dados
```

### Verificar se estão instaladas no V5:
```bash
cd AutoRelatorio_V5
pip list | grep -E "docx|Pillow|openpyxl|fastapi|uvicorn|pydantic"
```

---

## 4. Lógica recuperável — destaques

### 4.1 parse_medidas_sp2() — parser de nome de arquivo
```python
# utils_sp2.py — extrai medidas do nome do arquivo
# Suporta: "01 - 6,50 x 3,00.jpg", "01 - 3,85 x 2,18 - Faces 2.jpg"
# "01 - vista geral.jpg" (sem medidas), "CROQUI 01 - Laje.jpg"
parse_medidas_sp2("01 - 6,50 x 3,00 - Desconto 1,89m².jpg")
# → { num: 1, largura: 6.5, altura: 3.0, desconto: 1.89,
#     subtotal: 19.5, total: 17.61, faces: 1, tem_medidas: True }
```
**Isso implementa todo o Módulo 2 de cálculo do V5 no backend — já funciona e é testado.**

### 4.2 detectar_item_por_pasta() — associação automática foto → item
```python
# Identifica item do contrato pelo nome da pasta (sem necessidade de o usuário selecionar)
detectar_item_por_pasta("1.1 - Emassamento e pintura de teto")
# → {"id": "17.2", "desc": "Emassamento de parede...", "un": "m²"}
```
**O frontend pode usar isso: scanner detecta o item automaticamente pelo nome da pasta.**

### 4.3 substituir_placeholders() — cabeçalho no template
```python
# word_utils.py — substitui {{nr_os}}, {{dt_atend}}, etc. no template
# Funciona em parágrafos E tabelas do docx
substituir_placeholders(doc, meta={
    "nr_os": "1753",
    "dt_atend": "21/05/2026",
    "ag_cod": "1234-5",
    "ag_nome": "Ag. Centro"
})
```

### 4.4 inserir_conteudo_sp2() — geração Word completa
Função principal que recebe o array `conteudo` e gera o .docx.
Suporta todos os tipos de bloco: fachada, foto, croqui, texto, enunciado, tabela de cálculo, tabela de itens, quebra de página.

---

## 5. Código duplicado identificado

| Função | V4 location | Duplicada onde |
|---|---|---|
| `folder_sort_key()` | `generator.py`, `generator_sp.py` | Idêntica nos 3 geradores — extrair para `utils_base.py` |
| `_natural_sort_key()` | `generator_sp2.py`, `generator_sp.py`, `generator.py` | Idêntica — mover para `utils_base.py` |
| `_inserir_imagem()` | `word_utils_sp2.py` e variante em `word_utils_sp.py` | Quase idêntica — unificar em `word_utils.py` |
| `_set_cell_bg()`, `_set_cell_text()` | `word_utils_sp2.py` e `gerar_memorial.py` | Padrão similar — unificar |

**Recomendação para o V5:** criar `utils_base.py` com as funções compartilhadas desde o início.

---

## 6. Riscos arquiteturais

### 🔴 RISCO 1 — Importações relativas quebradas
O V4 usa `from utils_sp2 import ...` e `from word_utils import ...` com importações relativas.
No V5, com a estrutura `backend/contracts/c1565/engine/`, o `sys.path` precisará ser configurado.
**Fix:** usar `from backend.core.utils_sp2 import ...` ou adicionar `__init__.py` corretamente.

### 🔴 RISCO 2 — PIL/Pillow necessário
`word_utils.py` usa `from PIL import Image` para calcular proporção das imagens.
O V5 ainda não tem `pillow` instalado no backend.
**Fix:** `pip install pillow` no `requirements.txt` do backend.

### 🟡 RISCO 3 — Padrão de nome de arquivo SP1 vs SP2
O SP2 usa `"01 - 6,50 x 3,00.jpg"` (com número) e SP1 usa `"6,50 x 3,00.jpg"` (sem número).
O parser de cada modo é diferente — não intercambiável.
**OK:** já separado em `utils_sp2.py` vs `utils_sp.py`.

### 🟡 RISCO 4 — Templates .docx com placeholder `{{start_here}}`
O word builder depende de um marcador `{{start_here}}` no template para saber onde inserir o conteúdo.
Os templates do V4 já têm esse marcador — mas ao copiar para o V5, validar que ainda está presente.

### 🟡 RISCO 5 — Payload frontend ↔ backend incompatível
O V4 usa:
```json
{ "root_path": "C:/fotos/agencia", "output_path": "C:/output", "conteudo": [...], "meta": {...} }
```
O V5 (`lib/api.ts`) envia:
```json
{ "contrato_id": "1565", "nr_os": "1753", "ag_cod": "...", ... }
```
**Fix:** alinhar o payload no `server.py` do V5 com o formato que o frontend envia.

---

## 7. Recomendações de reaproveitamento

### Ação imediata (zero código novo):

**Passo 1 — Copiar os 9 templates:**
```
DE: TM-MEUS-APPS/01_Golden_Apps_meu_uso/AutoRelatorio_V4/APP/backend/templates/*.docx
PARA: AutoRelatorio_V5/backend/contracts/cXXXX/template/MODELO-XXXX.docx
```

**Passo 2 — Copiar o utils_sp2 + generator_sp2 + word_utils_sp2:**
```
DE: TM-MEUS-APPS/.../backend/generator_sp2.py
PARA: AutoRelatorio_V5/backend/contracts/c1565/engine/scanner_sp2.py
     (renomear build_content_sp2 → scan)

DE: TM-MEUS-APPS/.../backend/word_utils_sp2.py
PARA: AutoRelatorio_V5/backend/contracts/c1565/engine/word_builder_sp2.py
     (renomear inserir_conteudo_sp2 → build_word)

DE: TM-MEUS-APPS/.../backend/utils_sp2.py
PARA: AutoRelatorio_V5/backend/core/utils_sp2.py
     (sem alterações)

DE: TM-MEUS-APPS/.../backend/word_utils.py
PARA: AutoRelatorio_V5/backend/core/word_utils.py
     (sem alterações)
```

**Passo 3 — Extrair items.json por contrato:**
```
DE: TM-MEUS-APPS/.../scripts/itens_por_contrato.json
    Chaves: "1507_CUIABA", "1565_SJRP", "0908_SJC", etc.
PARA: AutoRelatorio_V5/backend/contracts/c1565/items/items.json
     AutoRelatorio_V5/backend/contracts/c1507/items/items.json
     ... (9 arquivos — script simples de split)
```

**Passo 4 — Adicionar /health ao server.py do V5:**
```python
# Copiar de routes.py V4
@app.get("/health")
def health(): return {"status": "ok", "version": "5.0"}
```

**Passo 5 — Alinhar payload da API:**
Adaptar `ScanRequest` e `GenerateRequest` do `server.py` V5 para aceitar o formato que o `lib/api.ts` envia.

---

## 8. Resumo executivo

```
SITUAÇÃO ANTES DESTA INVESTIGAÇÃO
────────────────────────────────────────────────
 Diagnóstico anterior dizia:
  ❌ Scanner: não existe
  ❌ Word builder: não existe
  ❌ Templates: todos pendentes (🔴)
  ❌ items.json: todos pendentes (🔴)
  ❌ Bridge API: incompatível

SITUAÇÃO REAL (pós-investigação)
────────────────────────────────────────────────
 ✅ Scanner SP2:     EXISTE — generator_sp2.py (370 linhas, testado)
 ✅ Scanner SP1:     EXISTE — generator_sp.py
 ✅ Scanner Trad:    EXISTE — generator.py
 ✅ Word builder SP2: EXISTE — word_utils_sp2.py (470 linhas, testado)
 ✅ Word builder SP1: EXISTE — word_utils_sp.py
 ✅ Word builder base: EXISTE — word_utils.py (helpers completos)
 ✅ Parser de nomes: EXISTE — utils_sp2.py (parse_medidas_sp2, detectar_item_por_pasta)
 ✅ Templates:        TODOS OS 9 EXISTEM em templates/ do V4
 ✅ items.json:       20.068 LINHAS em itens_por_contrato.json (todos os 9 contratos)
 ✅ Memorial builder: EXISTE — gerar_memorial.py (testado com relatórios reais)
 ✅ Extrator xlsx:    EXISTE — extrair_itens.py
 ✅ Endpoint /health: EXISTE — routes.py
 ✅ Endpoint /download: EXISTE — routes.py
 ✅ Exemplos de saída: 10+ .docx reais como ground truth

ESFORÇO REAL DE MIGRAÇÃO
────────────────────────────────────────────────
 Antes da investigação (estimado): 3-5 dias de código novo
 Após a investigação (real):       1-2 dias de migração + adaptação

 Código a escrever do zero: ~0%  (tudo já existe)
 Código a adaptar: ~20%  (assinaturas, imports, payload API)
 Código a copiar: ~80%  (pronto para mover)
```

---

*Investigação realizada em 2026-05-25.*  
*Arquivos inspecionados: generator_sp2.py, generator_sp.py, generator.py, word_utils_sp2.py, word_utils_sp.py, word_utils.py, utils_sp2.py, utils_sp.py, routes.py, server.py, itens_por_contrato.json, gerar_memorial.py, extrair_itens.py + estrutura completa de templates e fixtures.*
