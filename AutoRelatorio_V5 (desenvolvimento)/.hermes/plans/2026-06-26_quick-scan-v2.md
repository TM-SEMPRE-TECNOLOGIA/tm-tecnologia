# Plano V2: Quick-Scan Strip + Leitura Inteligente de Pastas + Configuração de Foto

> **Para o Hermes:** Use subagent-driven-development. NÃO escreva código ainda — planning only.
> **Gerado:** 2026-06-26 · **Referência real:** `SABINOPOLIS - 2557` (C:\Users\thiag\Desktop\Minha Demanda\2 - Em andamento\)
> **Código legado:** AutoRelatorioV1_Dev em `C:\Users\thiag\Desktop\Minha Demanda\1 - Preventivas 2026\01 - Apoio operacional\`
> **UI escolhida:** Variant 3 — Quick-Scan Strip (filmstrip horizontal + painel de detail)

**Goal:** App que recebe uma raiz de pasta (ex: `SABINOPOLIS - 2557`), extrai automaticamente a hierarquia (Área → Ambiente → Serviço → fotos), entende os nomes de arquivo (que já codificam medidas), permite configurar o TIPO de cada foto via dropdown, revisar rápida com filmstrip, e gerar DOCX com medidas abaixo de cada imagem.

---

## 0. O QUE APRENDEMOS COM AS PASTAS REAIS

### 0.1 Estrutura real — Sabinópolis 2557

```
SABINOPOLIS - 2557/
├── - ENVIO PORTAL/                  ← PDFs, ignorar
├── - Área externa/
│   └── 12 - Telhado/
│       └── - Vista ampla/
│           ├── IMG-20260623-WA0292.jpg
│           ├── IMG-20260623-WA0293.jpg
│           ├── IMG-20260623-WA0295.jpg
│           └── IMG-20260623-WA0297.jpg
└── - Área interna/
    ├── 1 - SAA/
    │   ├── - Vista ampla/
    │   │   ├── IMG-20260623-WA0079.jpg
    │   │   └── IMG-20260623-WA0080.jpg
    │   ├── 1.1 - Pintura acrílica/
    │   │   ├── - Detalhes/
    │   │   │   ├── IMG-20260623-WA0083.jpg
    │   │   │   ├── IMG-20260623-WA0084.jpg
    │   │   │   ├── IMG-20260623-WA0086.jpg
    │   │   │   └── IMG-20260623-WA0087.jpg
    │   │   ├── 1,85 x 0,20.jpg
    │   │   ├── 1,90 x 0,20.jpg
    │   │   └── 3,10 x 0,70.jpg
    │   ├── 1.2 - Pintura automotiva/
    │   │   ├── - Detalhes/
    │   │   │   ├── IMG-20260623-WA0105.jpg
    │   │   │   ├── IMG-20260623-WA0106.jpg
    │   │   │   └── IMG-20260623-WA0107.jpg
    │   │   └── 6,00 unidades.jpg
    │   ├── 1.3 - Piso tátil/
    │   │   ├── - Detalhes/  (8 fotos)
    │   │   └── 2 alertas e 12 direcionais.jpg
    │   └── 1.4 - Fita de piso/
    │       ├── - Detalhes/  (3 fotos)
    │       └── 12,00 m de fita amarela.jpg
    ├── 2 - Atendimento/
    │   ├── - Vista ampla/  (2 fotos)
    │   ├── 2.1 - Pintura acrílica/
    │   │   └── 12,00 x 2,90.jpg
    │   ├── 2.2 - Fita de piso/
    │   │   ├── - Detalhes/  (2 fotos)
    │   │   └── 12,00 metros fita amarela.jpg
    │   ├── 2.3 - Ponto elétrico/  (6 fotos)
    │   └── 2.4 - Ponto lógico/  (6 fotos)
    ├── 3 - CAIEX/ ...
    ├── 4 - Suporte/ ...
    ├── 5 - Acesso restrito/
    │   ├── 5.1 - Pintura acrílica/
    │   │   ├── 1,50 x 6,00.jpg
    │   │   ├── 6,00 x 5,40.jpg
    │   │   └── 6,00 x 5,40 (2).jpg     ← (2) = faces 2
    │   ├── 5.2 - Pintura esmalte em porta/
    │   │   ├── - Detalhes/  (4 fotos)
    │   │   ├── 2,10 x 0,90.jpg
    │   │   └── 2,10 x 1,20.jpg
    │   └── 5.3 - Pintura esmalte metal/
    │       ├── 5,40.jpg                ← medida linear
    │       └── 5,40 (2).jpg            ← linear com faces 2
    ├── 6 - Banheiro masculino/ ...
    ├── 7 - Banheiro feminino/ ...
    ├── 8 - Piso inferior/ ...
    ├── 9 - Cozinha/ ...
    ├── 10 - Sala de máquinas/ ...
    ├── 11 - Corredor de abastecimento/ ...
    ├── 12 - Tesouraria/ ...
    └── 13 - Sala online/ ...
```

### 0.2 Padrões de nomenclatura DESCOBERTOS

| Padrão no nome do arquivo | Exemplo | O que significa | Como o app deve interpretar |
|---|---|---|---|
| `X,XX x X,XX.jpg` | `3,50 x 2,80.jpg` | Área: largura × altura | `largura=3.50, altura=2.80, unidade=m²` |
| `X,XX x X,XX (2).jpg` | `6,00 x 5,40 (2).jpg` | Área com 2 faces | `largura=6.00, altura=5.40, faces=2, unidade=m²` |
| `X,XX.jpg` (só um número) | `5,40.jpg` | Medida linear | `comp=5.40, unidade=m` |
| `X,XX (2).jpg` | `5,40 (2).jpg` | Linear com 2 faces | `comp=5.40, faces=2, unidade=m` |
| `X,XX unidades.jpg` | `6,00 unidades.jpg` | Quantidade | `quantidade=6, unidade=un` |
| `X,XX m de fita.jpg` | `12,00 m de fita amarela.jpg` | Linear com unidade explícita | `comp=12.00, unidade=m` |
| `IMG-20260623-WAXXXX.jpg` | WhatsApp image | Foto sem medidas no nome | `medidas=pendentes` |
| `N alertas e M direcionais.jpg` | `2 alertas e 12 direcionais.jpg` | Contagem mista | `quantidade textual (não parseável)` |
| `X,XX x ,XXX.jpg` (vírgula dupla) | `2,05 x ,200.jpg` | Erro de digitação | Tentar parse com tolerância |

### 0.3 Hierarquia de pastas — 4 níveis

```
Nível 0: Pasta raiz               "SABINOPOLIS - 2557"
Nível 1: Área                     "- Área externa", "- Área interna"
Nível 2: Ambiente (numerado)      "1 - SAA", "5 - Acesso restrito"
Nível 3: Serviço (numerado)       "1.1 - Pintura acrílica", "5.2 - Pintura esmalte em porta"
Nível 4: Sub-pasta especial       "- Vista ampla", "- Detalhes"
```

**Regra de ouro:** O nome da pasta do serviço (nível 3) **já é a descrição do que está sendo feito**. Ex: `1.1 - Pintura acrílica` → isso JÁ é o texto que deve aparecer no relatório.

### 0.4 O que o V1 (legado) já faz

O `generator.py` do V1:
- ✅ Varre a pasta com `os.walk`
- ✅ Ordena pastas (Vista ampla primeiro, depois numéricas, Detalhes por último)
- ✅ Produz `conteudo[]` com títulos (`»`) e `{"imagem": path}`
- ✅ Insere imagens no DOCX com otimização de layout (agrupa verticais em tabelas 2-3 colunas)
- ❌ NÃO extrai medidas dos nomes de arquivo
- ❌ NÃO adiciona texto de medidas abaixo das fotos
- ❌ NÃO tem interface de aprovação/seleção

O `server.py` do V1:
- ✅ `POST /api/scan` → varre e retorna `conteudo[]`
- ✅ `POST /api/generate` → recebe `conteudo[]` editado + gera DOCX
- ✅ `GET /api/thumbnail` → gera thumbnail de qualquer imagem por path
- ❌ Sem suporte a medidas
- ❌ Sem multipart upload

---

## 1. ARQUITETURA PROPOSTA (VISÃO GERAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FLUXO COMPLETO — V2                              │
│                                                                     │
│  [Usuário abre o app]                                               │
│     │                                                               │
│     ├─1─ Cola ou seleciona o caminho da pasta raiz                  │
│     │     Ex: C:\Users\thiag\Desktop\...\SABINOPOLIS - 2557        │
│     │                                                               │
│  [Backend: POST /api/scan-v2]                                       │
│     │                                                               │
│     ├─ os.walk() na raiz                                            │
│     ├─ Extrai hierarquia (área → ambiente → serviço → subpasta)     │
│     ├─ Para cada .jpg/.png:                                         │
│     │   ├─ Parse do nome: tenta extrair largura, altura, faces,     │
│     │   │   unidade, quantidade                                     │
│     │   ├─ Classifica o TIPO automático:                            │
│     │   │   ├─ Pasta chamada "- Vista ampla" → tipo="vista_ampla"   │
│     │   │   ├─ Pasta chamada "- Detalhes"   → tipo="detalhe"        │
│     │   │   ├─ Nome contém "x"              → tipo="medida_area"    │
│     │   │   ├─ Nome contém "unidades"       → tipo="medida_un"      │
│     │   │   ├─ Nome contém "m de"           → tipo="medida_linear"  │
│     │   │   └─ Nome é IMG-*                 → tipo="registro"       │
│     │   └─ Gera thumbnail (200px) via Pillow                        │
│     │                                                               │
│     └─ Retorna JSON com:                                            │
│         {                                                            │
│           "raiz": "SABINOPOLIS - 2557",                              │
│           "arvore": [                                               │
│             {                                                        │
│               "tipo": "area",                                       │
│               "nome": "- Área interna",                             │
│               "ambientes": [                                        │
│                 {                                                    │
│                   "tipo": "ambiente",                               │
│                   "numero": "1",                                    │
│                   "nome": "1 - SAA",                                │
│                   "servicos": [                                     │
│                     {                                                │
│                       "tipo": "servico",                            │
│                       "numero": "1.1",                              │
│                       "nome": "1.1 - Pintura acrílica",             │
│                       "fotos": [                                    │
│                         {                                            │
│                           "path": "C:/.../1,85 x 0,20.jpg",        │
│                           "nome": "1,85 x 0,20.jpg",               │
│                           "thumbnail": "base64...",                 │
│                           "medidas_extraidas": {                    │
│                             "largura": 1.85, "altura": 0.20,        │
│                             "unidade": "m²", "faces": 1             │
│                           },                                        │
│                           "tipo_foto": "medida_area",               │
│                           "incluida": true                          │
│                         },                                          │
│                         ...                                          │
│                       ]                                              │
│                     },                                              │
│                     {                                                │
│                       "tipo": "subpasta",                           │
│                       "nome": "- Vista ampla",                      │
│                       "fotos": [...]                                │
│                     }                                                │
│                   ]                                                  │
│                 }                                                    │
│               ]                                                      │
│             }                                                        │
│           ],                                                         │
│           "total_fotos": 156,                                        │
│           "pastas_ignoradas": ["- ENVIO PORTAL"]                     │
│         }                                                            │
│                                                                     │
│  [Frontend: Quick-Scan Strip UI]                                    │
│     │                                                               │
│     ├─ Filmstrip horizontal com todas as fotos                      │
│     ├─ Painel de detail ao selecionar uma foto                      │
│     ├─ DOIS dropdowns por foto:                                     │
│     │   ├─ Dropdown 1: "Tipo da foto"  ← NOVO                      │
│     │   │   Opções: área, ambiente, serviço, vista ampla,           │
│     │   │           detalhe, registro, fachada                      │
│     │   └─ Dropdown 2: "Item do contrato" ← já existe              │
│     ├─ Toggle include/exclude (já existe no sketch 003)             │
│     ├─ Campos de medida (já existem no MeasureForm)                 │
│     ├─ Preview DOCX atualizado em tempo real                        │
│     └─ Botão "Gerar .docx" → envia JSON completo ao backend         │
│                                                                     │
│  [Backend: POST /api/generate-v2]                                   │
│     │                                                               │
│     ├─ Recebe: arvore[] (JSON) + template selecionado               │
│     ├─ Monta conteudo[] enriquecido:                                │
│     │   ├─ Títulos de seção (área, ambiente, serviço)               │
│     │   ├─ Fotos com medidas + tipo_foto no metadata                │
│     │   └─ Quebras de página                                        │
│     ├─ word_utils_v2.inserir_conteudo():                            │
│     │   ├─ Para cada foto com tipo="medida_area":                   │
│     │   │   ├─ Insere imagem (10cm altura padrão)                   │
│     │   │   └─ Insere parágrafo: "3,50 × 2,80 m | Faces: 2 |       │
│     │   │                        Total: 19,60 m²"                   │
│     │   ├─ Para tipo="vista_ampla":                                 │
│     │   │   └─ Legenda: "VISTA AMPLA — SAA"                         │
│     │   ├─ Para tipo="detalhe":                                     │
│     │   │   └─ Legenda: "Detalhe do serviço"                        │
│     │   └─ Para tipo="registro":                                    │
│     │       └─ Sem legenda de medida (só a foto)                    │
│     └─ Retorna FileResponse(.docx)                                  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. O NOVO DROPDOWN: "TIPO DA FOTO"

O usuário pediu: *"um seletor parecido com item do contrato, porém para definir a configuração da foto — por exemplo se é uma área, um ambiente, mas o que tiver serviço já é uma das configurações."*

### 2.1 Os tipos de foto

| Tipo | Valor | O que significa | Como aparece no DOCX | Detectado automaticamente? |
|------|-------|----------------|---------------------|---------------------------|
| **Área** | `area` | Foto que documenta uma área (espaço físico) | Título da seção de área, sem medidas | ❌ Não — sempre manual |
| **Ambiente** | `ambiente` | Foto que mostra um ambiente específico | Subtítulo, sem medidas | ❌ Não — sempre manual |
| **Serviço** | `servico` | Foto que documenta um serviço executado | Subtítulo do serviço, com medidas se houver | ✅ Sim — pastas nível 3 |
| **Vista ampla** | `vista_ampla` | Foto panorâmica do local | "VISTA AMPLA — [nome do ambiente]" | ✅ Sim — pasta "- Vista ampla" |
| **Detalhe** | `detalhe` | Close-up de um problema ou acabamento | "Detalhe — [nome do serviço]" | ✅ Sim — pasta "- Detalhes" |
| **Registro** | `registro` | Foto geral/documental (WhatsApp) | Apenas a imagem, sem legenda | ✅ Sim — nome IMG-* |
| **Fachada** | `fachada` | Foto da fachada do prédio | "FACHADA" centralizado, imagem maior (12cm) | ❌ Não — sempre manual |
| **Medida (área)** | `medida_area` | Foto com medidas de área (larg × alt) | Imagem + "3,50 × 2,80 m \| Faces: 2 \| Total: 19,60 m²" | ✅ Sim — nome contém "x" |
| **Medida (linear)** | `medida_linear` | Foto com medida linear | Imagem + "5,40 m \| Faces: 2 \| Total: 10,80 m" | ✅ Sim — nome com número só |
| **Medida (unidade)** | `medida_unidade` | Foto com quantidade | Imagem + "Qtd: 6 unidades" | ✅ Sim — nome "unidades" |

### 2.2 Comportamento do dropdown por tipo

Quando o usuário muda o tipo da foto, os campos de medida se ADAPTAM:

| Tipo selecionado | Campos de medida exibidos | Comportamento |
|-----------------|--------------------------|---------------|
| `area` | Nenhum | Apenas título da seção |
| `ambiente` | Nenhum | Apenas subtítulo |
| `servico` | Item do contrato + Medidas | Herda o nome da pasta como descrição |
| `vista_ampla` | Nenhum | Legenda automática |
| `detalhe` | Nenhum | Legenda automática |
| `registro` | Nenhum | Só a imagem |
| `fachada` | Nenhum | Imagem grande centralizada |
| `medida_area` | Largura + Altura + Faces + Desconto + Item | **Pré-preenchido do parse do nome** |
| `medida_linear` | Comprimento + Faces + Item | **Pré-preenchido do parse do nome** |
| `medida_unidade` | Quantidade + Item | **Pré-preenchido do parse do nome** |

---

## 3. PLANO DE IMPLEMENTAÇÃO (FASES)

### FASE 0 — PRÉ-REQUISITOS (DIAGNÓSTICO JÁ FEITO ✅)

- [x] Estrutura real de pastas mapeada (Sabinópolis 2557)
- [x] Padrões de nomenclatura catalogados (8 padrões)
- [x] Código V1 legado analisado
- [x] UI escolhida (Variant 3 — Quick-Scan Strip)
- [x] Tipos de foto definidos (10 tipos)

---

### 🔧 FASE A — BACKEND: NOVO SCANNER INTELIGENTE

**Objetivo:** Criar `POST /api/scan-v2` que varre a pasta raiz e retorna a árvore completa com parse de nomes, thumbnails e classificação automática de tipo.

**Arquivos:**
- Criar: `backend/core/scanner_v2.py` — função `scan_root_v2(pasta_raiz) -> dict`
- Modificar: `backend/core/server.py` — adicionar endpoint

#### Task A1: Função `parse_filename(nome: str) -> dict`

Extrai medidas do nome do arquivo.

```python
def parse_filename(nome: str) -> dict:
    """
    Exemplos:
      "3,50 x 2,80.jpg"        → {"largura": 3.5, "altura": 2.8, "unidade": "m²", "faces": 1}
      "6,00 x 5,40 (2).jpg"    → {"largura": 6.0, "altura": 5.4, "unidade": "m²", "faces": 2}
      "5,40.jpg"               → {"comp": 5.4, "unidade": "m", "faces": 1}
      "5,40 (2).jpg"           → {"comp": 5.4, "unidade": "m", "faces": 2}
      "6,00 unidades.jpg"      → {"quantidade": 6, "unidade": "un", "faces": 1}
      "12,00 m de fita.jpg"    → {"comp": 12.0, "unidade": "m", "faces": 1}
      "IMG-20260623-WA0292.jpg" → {}  # sem medidas
    """
```

**Algoritmo:**
1. Remove extensão
2. Substitui `,` por `.` nos números
3. Tenta regex `(\d+\.?\d*)\s*x\s*(\d+\.?\d*)` → área
4. Tenta regex `(\d+\.?\d*)\s*unidades?` → quantidade
5. Tenta regex `(\d+\.?\d*)\s*m\s` → linear
6. Tenta regex `(\d+\.?\d*)$` → linear simples
7. Verifica `(2)` ou `( 2 )` no nome → faces=2
8. Tenta tolerância para erros de digitação: `,200` → `0.200`

#### Task A2: Função `classificar_tipo_foto(path: str, nome: str, medidas: dict, pasta_pai: str) -> str`

```python
def classificar_tipo_foto(path, nome, medidas, pasta_pai):
    """
    Retorna um dos 10 tipos.
    Ordem de precedência:
    1. Pasta pai = "- Vista ampla"     → "vista_ampla"
    2. Pasta pai = "- Detalhes"        → "detalhe"
    3. Nome começa com "IMG-"          → "registro"
    4. Tem medidas de área             → "medida_area"
    5. Tem medida linear               → "medida_linear"
    6. Tem quantidade                  → "medida_unidade"
    7. Fallback                        → "registro"
    """
```

#### Task A3: Função `scan_root_v2(pasta_raiz: str) -> dict`

Varre com `os.walk()`, monta a árvore hierárquica, gera thumbnails.

```python
def scan_root_v2(pasta_raiz: str) -> dict:
    """
    Retorna:
    {
      "raiz": "SABINOPOLIS - 2557",
      "arvore": [
        {
          "tipo": "area",           # area | ambiente | servico | subpasta
          "nome": "- Área interna",
          "nivel": 1,
          "ordem": 1,
          "ambientes": [
            {
              "tipo": "ambiente",
              "numero": "1",
              "nome": "1 - SAA",
              "nivel": 2,
              "servicos": [
                {
                  "tipo": "servico",
                  "numero": "1.1",
                  "nome": "1.1 - Pintura acrílica",
                  "nivel": 3,
                  "fotos": [
                    {
                      "id": "uuid",
                      "path": "C:/.../1,85 x 0,20.jpg",
                      "nome": "1,85 x 0,20.jpg",
                      "thumbnail_base64": "...",
                      "medidas_extraidas": {...},
                      "tipo_foto": "medida_area",
                      "incluida": true,
                      "ordem": 1,
                    }
                  ]
                },
                {
                  "tipo": "subpasta",
                  "nome": "- Vista ampla",
                  "nivel": 4,
                  "fotos": [...]
                }
              ]
            }
          ]
        }
      ],
      "total_fotos": 156,
      "pastas_ignoradas": ["- ENVIO PORTAL"],
      "erros": []
    }
    """
```

**Regras de classificação de nível:**
- Nível 1: pastas que começam com `- ` (ex: `- Área interna`) → `tipo="area"`
- Nível 2: pastas com padrão `N - Nome` (ex: `1 - SAA`) → `tipo="ambiente"`
- Nível 3: pastas com padrão `N.N - Nome` (ex: `1.1 - Pintura acrílica`) → `tipo="servico"`
- Nível 4: pastas especiais (`- Vista ampla`, `- Detalhes`) → `tipo="subpasta"`

**Pastas ignoradas:**
- `- ENVIO PORTAL` (PDFs)
- Qualquer pasta sem imagens
- `Thumbs.db`, `desktop.ini`

**Ordenação:**
- Áreas: `- Área externa` antes de `- Área interna`
- Ambientes: numérico pelo prefixo
- Serviços: numérico pelo prefixo (1.1, 1.2, ...)
- Fotos: por `os.path.getctime` (ordem de captura)
- Subpastas: `- Vista ampla` antes de `- Detalhes`

#### Task A4: Endpoint `POST /api/scan-v2`

```python
class ScanV2Request(BaseModel):
    pasta_raiz: str

@app.post("/api/scan-v2")
async def scan_v2(body: ScanV2Request):
    if not os.path.isdir(body.pasta_raiz):
        raise HTTPException(400, "Pasta raiz inválida")
    resultado = scan_root_v2(body.pasta_raiz)
    return resultado
```

---

### 🔧 FASE B — FRONTEND: QUICK-SCAN STRIP COM DOIS DROPDOWNS

**Objetivo:** Adaptar o wireframe Variant 3 para consumir `/api/scan-v2` e adicionar o dropdown de "Tipo da foto".

**Arquivos:**
- Criar: `frontend/components/QuickScanStrip.tsx`
- Criar: `frontend/components/PhotoDetail.tsx`
- Modificar: `frontend/lib/api.ts` — adicionar `scanV2()`
- Modificar: `frontend/lib/types.ts` — tipos da árvore
- Modificar: `frontend/app/page.tsx` — integrar no Step 2

#### Task B1: Tipos TypeScript para a árvore

```typescript
// lib/types.ts (adicionar)
export type TipoFoto = 
  | 'area' | 'ambiente' | 'servico' 
  | 'vista_ampla' | 'detalhe' | 'registro' 
  | 'fachada' | 'medida_area' | 'medida_linear' | 'medida_unidade';

export interface FotoNode {
  id: string;
  path: string;
  nome: string;
  thumbnail_base64: string;
  medidas_extraidas: MedidasParseadas;
  tipo_foto: TipoFoto;
  incluida: boolean;
  ordem: number;
  // Campos editáveis pelo usuário:
  tipo_foto_override?: TipoFoto;
  item_contrato?: ItemContrato;
  medidas_usuario?: MedidasBloco;
}

export interface ServicoNode {
  tipo: 'servico' | 'subpasta';
  numero?: string;
  nome: string;
  nivel: number;
  fotos: FotoNode[];
}

export interface AmbienteNode {
  tipo: 'ambiente';
  numero: string;
  nome: string;
  nivel: number;
  servicos: ServicoNode[];
}

export interface AreaNode {
  tipo: 'area';
  nome: string;
  nivel: number;
  ambientes: AmbienteNode[];
}

export interface ScanV2Result {
  raiz: string;
  arvore: AreaNode[];
  total_fotos: number;
  pastas_ignoradas: string[];
}
```

#### Task B2: Componente `QuickScanStrip`

Baseado no wireframe `003-quick-scan-strip/index.html`:

```
┌──────────────────────────────────────────────────────────────────┐
│ 📷 Fotos  [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]  ← → Space │
│          ▲ filmstrip horizontal com scroll                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────┐  ┌──────────────────┐ │
│  │        [🖼️ imagem grande]           │  │ 📄 Preview DOCX  │ │
│  │                                      │  │                  │ │
│  │  01 - 1,85 x 0,20.jpg               │  │ Área interna     │ │
│  │  📁 1 - SAA / 1.1 - Pintura acrílica│  │ 1 - SAA          │ │
│  │                                      │  │   1.1 - Pintura  │ │
│  │  ┌──────────────────────────────┐   │  │   [🖼️] 1,85×0,20│ │
│  │  │ Tipo da foto: [medida_area ▾]│   │  │   1,85×0,20m     │ │
│  │  └──────────────────────────────┘   │  │   Total: 0,37m²  │ │
│  │  ┌──────────────────────────────┐   │  │                  │ │
│  │  │ Item do contrato: [17.6 ▾]   │   │  │                  │ │
│  │  └──────────────────────────────┘   │  └──────────────────┘ │
│  │                                      │                       │
│  │  Larg: [1,85]  Alt: [0,20]  Faces: [1▾]                     │
│  │  TOTAL: 0,37 m²                                              │
│  │                                                              │
│  │  [✓ Incluir no relatório]                                    │
│  │                                                              │
│  │  ← Anterior   3 de 156   Próxima →                           │
│  └──────────────────────────────────────┘                       │
│                                                                  │
│  [← Voltar]                    Incluídas: 142/156   [Gerar .docx]│
└──────────────────────────────────────────────────────────────────┘
```

#### Task B3: Comportamento do dropdown "Tipo da foto"

Quando o usuário troca o tipo:
1. Se for `area`, `ambiente`, `servico`, `fachada`, `vista_ampla`, `detalhe`, `registro`:
   - Esconde campos de medida
   - Esconde dropdown de item do contrato
   - A foto vira "ilustrativa" (sem medidas no DOCX)
2. Se for `medida_area`, `medida_linear`, `medida_unidade`:
   - Mostra campos de medida apropriados
   - Mostra dropdown de item do contrato
   - Pré-preenche com `medidas_extraidas` do parse

#### Task B4: API client

```typescript
// lib/api.ts
export async function scanV2(pastaRaiz: string): Promise<ScanV2Result> {
  const res = await fetch(`${BASE_URL}/api/scan-v2`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pasta_raiz: pastaRaiz }),
  });
  if (!res.ok) throw new Error('Erro ao escanear pasta');
  return res.json();
}
```

---

### 🔧 FASE C — BACKEND: GERAÇÃO COM MEDIDAS + TIPOS

**Objetivo:** `POST /api/generate-v2` que recebe a árvore editada e gera DOCX com medidas formatadas conforme o tipo da foto.

**Arquivos:**
- Criar: `backend/core/word_builder_v2.py`
- Modificar: `backend/core/server.py`

#### Task C1: Função `montar_conteudo_v2(arvore: list) -> list`

Transforma a árvore editada (do frontend) no array `conteudo[]`:

```python
def montar_conteudo_v2(arvore: list) -> list:
    conteudo = []
    
    for area in arvore:
        # Título da área (nível 1)
        conteudo.append(area["nome"])
        
        for ambiente in area.get("ambientes", []):
            # Título do ambiente (nível 2)
            conteudo.append(f"»{ambiente['nome']}")
            
            for servico in ambiente.get("servicos", []):
                if servico["tipo"] == "subpasta":
                    # Subpasta (- Vista ampla, - Detalhes)
                    for foto in servico["fotos"]:
                        if not foto.get("incluida", True): continue
                        item = _montar_item_foto(foto)
                        conteudo.append(item)
                else:
                    # Serviço (nível 3)
                    conteudo.append(f"»»{servico['nome']}")
                    for foto in servico["fotos"]:
                        if not foto.get("incluida", True): continue
                        item = _montar_item_foto(foto)
                        conteudo.append(item)
                
                conteudo.append({"quebra_pagina": True})
    
    return conteudo


def _montar_item_foto(foto: dict) -> dict:
    tipo = foto.get("tipo_foto_override") or foto.get("tipo_foto", "registro")
    
    item = {"imagem": foto["path"], "tipo_foto": tipo}
    
    if tipo == "vista_ampla":
        item["legenda"] = "VISTA AMPLA"
    elif tipo == "detalhe":
        item["legenda"] = "Detalhe"
    elif tipo == "fachada":
        item["altura_cm"] = 12.0
        item["legenda"] = "FACHADA"
    elif tipo in ("medida_area", "medida_linear", "medida_unidade"):
        medidas = foto.get("medidas_usuario") or foto.get("medidas_extraidas", {})
        item["medidas"] = medidas
        item["item_contrato"] = foto.get("item_contrato")
    
    return item
```

#### Task C2: Word Builder V2 — `inserir_conteudo_v2()`

```python
def inserir_conteudo_v2(modelo_path, conteudo, output_path, meta):
    """
    Para cada item em conteudo[]:
    - string → título (Heading 1/2/3 conforme prefixo »)
    - {"imagem": path, "tipo_foto": "medida_area", "medidas": {...}}
      → Insere imagem + parágrafo de medidas:
        "1,85 × 0,20 m | Total: 0,37 m²"
    - {"imagem": path, "tipo_foto": "vista_ampla", "legenda": "VISTA AMPLA"}
      → Insere imagem + legenda "VISTA AMPLA — [ambiente]"
    - {"imagem": path, "tipo_foto": "registro"}
      → Insere apenas a imagem, sem texto
    - {"quebra_pagina": True}
      → Page break
    """
```

**Formatação das medidas por tipo:**

| Tipo | Formato no DOCX |
|------|----------------|
| `medida_area` | `1,85 × 0,20 m \| Faces: 2 \| Total: 0,74 m²` |
| `medida_linear` | `5,40 m \| Faces: 2 \| Total: 10,80 m` |
| `medida_unidade` | `Qtd: 6 unidades` |
| `vista_ampla` | `VISTA AMPLA — SAA` |
| `detalhe` | `Detalhe — Pintura acrílica` |
| `fachada` | `FACHADA` (imagem 12cm altura) |
| `registro` | *(sem texto)* |

---

### 🔧 FASE D — INTEGRAÇÃO E TESTES

#### Task D1: Conectar fluxo completo no `page.tsx`

```
Usuário cola path → scan-v2 → QuickScanStrip carrega →
  → Usuário revisa (inclui/exclui, ajusta tipo, preenche medidas) →
    → Clica Gerar → POST generate-v2 → download .docx
```

#### Task D2: Playwright — Testes E2E

5 testes:
1. **Scan de pasta real**: `POST /api/scan-v2` com Sabinópolis → retorna árvore com 156 fotos, tipos corretos
2. **Parse de nomes**: verifica que `1,85 x 0,20.jpg` → `largura=1.85, altura=0.20, tipo=medida_area`
3. **Quick-Scan Strip**: filmstrip renderiza, ← → navega, Space toggle include/exclude
4. **Troca de tipo**: dropdown muda campos de medida dinamicamente
5. **Geração DOCX**: mock do backend, verifica download

---

## 4. ORDEM DE EXECUÇÃO

```
FASE A (Backend scanner)
  A1 → A2 → A3 → A4
    └── FASE B (Frontend QuickScan)
          B1 → B2 → B3 → B4
            └── FASE C (Backend word builder)
                  C1 → C2
                    └── FASE D (Integração + Testes)
                          D1 → D2
```

**Paralelizável:** A1+A2 podem ser feitos em paralelo com B1 (tipos TypeScript).

---

## 5. ESTIMATIVA DE ESFORÇO

| Fase | Tasks | Tempo |
|------|-------|-------|
| A — Scanner V2 | 4 | 1h30 |
| B — Frontend QuickScan | 4 | 2h00 |
| C — Word Builder V2 | 2 | 1h00 |
| D — Integração + Testes | 2 | 1h00 |
| **Total** | **12** | **~5h30** |

---

## 6. ARQUIVOS AFETADOS

| Arquivo | Ação | Fase |
|---------|------|------|
| `backend/core/scanner_v2.py` | **CRIAR** | A |
| `backend/core/word_builder_v2.py` | **CRIAR** | C |
| `backend/core/server.py` | MODIFICAR | A, C |
| `frontend/components/QuickScanStrip.tsx` | **CRIAR** | B |
| `frontend/components/PhotoDetail.tsx` | **CRIAR** | B |
| `frontend/lib/types.ts` | MODIFICAR | B |
| `frontend/lib/api.ts` | MODIFICAR | B |
| `frontend/app/page.tsx` | MODIFICAR | D |
| `frontend/e2e/scan-v2.spec.ts` | **CRIAR** | D |

---

*Plano V2 completo. Fundamentado em dados reais da pasta Sabinópolis 2557 e código V1 legado.*
