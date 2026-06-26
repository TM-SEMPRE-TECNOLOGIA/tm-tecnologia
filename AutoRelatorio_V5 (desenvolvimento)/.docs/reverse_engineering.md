# AutoRelatório V5 — Engenharia Reversa dos Blocos do Relatório
**Versão:** 5.0.0-alpha  
**Data:** 2026-05-21  
**Status:** 🟡 Planejamento Wireframe  

---

## Objetivo

Mapear cada tipo de "dado" que entra no relatório `.docx` como uma **etapa/bloco visual**
dentro do wizard do AutoRelatório V5, permitindo que a interface mostre exatamente
o que será gerado antes da geração.

---

## Os Dois Modos e seus Blocos

## Placeholders Reais dos Templates (confirmados via extração python-docx)

| Campo no Formulário | Placeholder no .docx | Tipo | Obrigatório |
|--------------------|----------------------|------|:-----------:|
| Nº da OS | `{{nr_os}}` | text | ✅ |
| Data do Atendimento | `{{dt_atend}}` | date | ✅ |
| Código da Agência | `{{ag_cod}}` | text | ✅ |
| Nome da Agência | `{{ag_nome}}` | text | ✅ |
| Endereço | `{{endereco}}` | text | — |
| Responsável | `{{responsavel_dependencia}}` | text | — |
| Data de Elaboração | `{{dt_elab}}` | date | auto |
| Descrição do Serviço | `{Desc_here}` (chave interna) | select | — |
| Início do conteúdo | `{{start_here}}` (interno) | marcador | — |

> **Atenção contrato 2056:** template está faltando `{{ag_cod}}` — campo ausente, precisa ser inserido manualmente no Word.

---

## Os 3 Modos de Geração (confirmados no server.py do V4)

| Modo | Scanner | Word Builder | Uso |
|------|---------|-------------|-----|
| **Tradicional** | `generator.py` → `build_content_from_root()` | `word_utils.py` → `inserir_conteudo()` | 7 contratos: 1507, 2056, 2057, 2626, 2627, 3575, 6122 |
| **SP** | `generator_sp.py` → `build_content_sp()` | `word_utils_sp.py` → `inserir_conteudo_sp()` | 1 contrato: **0908** (São José dos Campos) |
| **SP2** | `generator_sp2.py` → `build_content_sp2()` | `word_utils_sp2.py` → `inserir_conteudo_sp2()` | 1 contrato: **1565** (SJRP / Ribeirão Preto) |

**Modo App** (leitura): `generator_app.py` → pasta plana, pode combinar com qualquer modo Word.

---

### MODO SP (contrato: 0908 — São José dos Campos)

> Motor SP: `generator_sp.py` → `build_content_sp()` / `word_utils_sp.py` → `inserir_conteudo_sp()`

Os blocos do modo SP são intermediários — inclui fachada, `texto_padrao` e tabela simples. A estrutura de pastas e os placeholders de cabeçalho são os mesmos do Tradicional.

---

### MODO TRADICIONAL (contratos: 1507, 2056, 2057, 2626, 2627, 3575, 6122)

#### Passo 1 — Cabeçalho (formulário dinâmico)

| Campo | Tipo | Obrigatório | Placeholder Word |
|-------|------|:-----------:|-----------------|
| Nº da OS | text | ✅ | `{{nr_os}}` |
| Data do Atendimento | date | ✅ | `{{dt_atend}}` |
| Código da Agência | text | ✅ | `{{ag_cod}}` |
| Nome da Agência | text | ✅ | `{{ag_nome}}` |
| Endereço | text | — | `{{endereco}}` |
| Responsável | text | — | `{{responsavel_dependencia}}` |
| Data de Elaboração | date | auto | `{{dt_elab}}` |
| Descrição do Serviço | select (4 opções) | — | `{Desc_here}` |

#### Passo 2 — Blocos do Corpo (scan de pasta → array `conteudo`)

```
PASTA ROOT/
├── PASTA NÍVEL 1 (ex: - Área externa)
│   ├── PASTA NÍVEL 2 (ex: 01 - Fachada)
│   │   ├── foto_01.jpg
│   │   └── foto_02.jpg
│   └── PASTA NÍVEL 2 (ex: 02 - Lateral)
│       └── foto_01.jpg
```

| Tipo de Bloco | Representação no `conteudo` | Resultado no Word |
|---------------|----------------------------|-------------------|
| **TÍTULO** | `str` sem prefixo `»` | Heading 1 — nome da pasta nível 1 |
| **SUBTÍTULO** | `str` com `»` | Heading 2 — nome da pasta nível 2 |
| **SUB-SUBTÍTULO** | `str` com `»»` | Heading 3 — pasta nível 3 |
| **IMAGEM** | `{"imagem": path}` | Foto centralizada (paisagem=10cm, retrato=2×7cm) |
| **QUEBRA DE PÁGINA** | `{"quebra_pagina": True}` | `<page-break>` — sempre após bloco |

**Regra de layout de imagens:**
- 2 fotos retrato lado a lado → tabela 2 colunas (7cm cada)
- 1 foto paisagem → centralizada 10cm
- Ordenação: por `ctime` (ordem de criação)

---

### MODO SP2 (contrato: 1565 — São José do Rio Preto / Ribeirão Preto)

#### Passo 1 — Cabeçalho (mesmos 7 placeholders dos outros contratos)

O contrato 1565 usa os MESMOS placeholders `{{ag_cod}}`, `{{ag_nome}}`, `{{dt_atend}}`, `{{dt_elab}}`, `{{nr_os}}`, `{{endereco}}`, `{{responsavel_dependencia}}`.

Campos extras do SP2 (como contrato, elaborador, empresa) são **fixos no template** — já impressos no .docx, não são placeholders dinâmicos. Apenas os 7 campos acima precisam ser preenchidos pelo usuário.

#### Passo 2 — Blocos do Corpo SP2 (scan hierárquico)

```
PASTA ROOT/ (ex: AGÊNCIA CENTRO — 1234-5)
├── Fachada.jpg                          → imagem_fachada
├── 1 - 1º Andar – Espaço Desativado/   → título nível 1
│   ├── 1.1 - Emassamento de teto/      → título nível 2 (pasta de serviço)
│   │   ├── 01 - 16,20 x 4,63.jpg      → imagem + linha de memória de cálculo
│   │   ├── 02 - vista.jpg             → imagem (sem medidas)
│   │   ├── CROQUI 01 - Laje.jpg       → croqui + legenda
│   │   └── - Detalhes 1/              → texto_padrao + imagens de detalhe
│   └── 1.2 - Pintura acrílica/        → título nível 2
│       └── 01 - 8,40 x 3,00.jpg      → imagem + linha de memória
```

| # | Tipo de Bloco | Representação no `conteudo` | Etapa Visual no Wizard | Resultado no Word |
|---|---------------|----------------------------|------------------------|-------------------|
| 1 | **TÍTULO** | `str` (sem `»`) | Cabeçalho de Seção | Heading 1 |
| 2 | **SUBTÍTULO** | `str` com `»` | Título de Serviço | Heading 2 |
| 3 | **IMAGEM FACHADA** | `{"imagem_fachada": path}` | Foto de Capa | Foto centralizada grande |
| 4 | **IMAGEM** | `{"imagem": path}` | Foto do Serviço | Foto com medidas no nome |
| 5 | **CROQUI** | `{"croqui": path, "legenda": str}` | Croqui Técnico | Imagem + legenda abaixo |
| 6 | **DETALHE** | `{"texto_padrao": str}` + imagens | Subitem de Detalhe | Label + fotos de detalhe |
| 7 | **DESCRIÇÃO** | `{"enunciado_item": {"codigo": str, "descricao": str}}` | Bloco de Descrição | Texto: "Item 17.6 – Pintura em látex..." |
| 8 | **TABELA MEMÓRIA** | `{"memoria_calculo": {...}}` | Tabela de Cálculo | Tabela: FOTO \| COMP. \| ALT. \| DESCONTO \| TOTAL |
| 9 | **TABELA ITENS** | `{"tabela_itens_sp2": {...}}` | Tabela de Itens | Tabela: CÓDIGO \| DESCRIÇÃO \| QTD \| UN |
| 10 | **QUEBRA** | `{"quebra_pagina": True}` | — | `<page-break>` |

---

## Memorial de Cálculo — Integração com Planilha (todos os contratos)

> **Descoberta 2026-05-22:** A planilha `MEMORIAL DE CÁLCULO - SÃO PAULO.xlsx` (contrato 0908) tem **2 abas**:
> - **Itens**: 529 itens do contrato com código, descrição, QTDE (calculada) e UN
> - **Memorial de cálculo**: 5 seções de cálculo, cada uma preenchida com medidas das fotos

### As 5 Seções de Cálculo (colunas da aba "Memorial de cálculo")

| Seção | Colunas | Campos | Quando usar |
|-------|---------|--------|-------------|
| **M² COM DESCONTO** | A–J | Foto \| Comp. \| Altura \| Desconto \| Subtotal \| Total | Pintura de parede/fachada com deduções de abertura |
| **M² SEM DESCONTO** | K–R | Foto \| Comp. \| Altura \| Total | Piso, teto, revestimento sem deduções |
| **ENTULHO, ETC** | S–Z | Foto \| Comp. \| Altura \| Total | Remoção de entulho, demolição |
| **ESMALTE EM PORTA** | AA–AH | Foto \| Comp. \| Altura/Comp. \| Total | Pintura esmalte em esquadrias |
| **UNITÁRIOS** | AH+ | Foto \| Quantitativo \| UN | Itens em un, m, km (não m²) |

### Integração no App (fluxo)

```
Usuário adiciona item "17.6 — Pintura acrílica" → app lê tipo_calculo: "sem_desconto"
  ↓
Fotos do serviço têm medidas no nome: "01 - 8,40 x 3,00.jpg" → comp=8.40, alt=3.00
  ↓
App preenche seção SEM_DESCONTO do Memorial: linha 01 | 8,40 | 3,00 | 25,20
  ↓
Total = 25,20 m² → atualiza QTDE do item 17.6 na aba Itens
  ↓
Word gerado com foto + tabela de memória de cálculo
Excel Memorial de Cálculo gerado/atualizado com os valores calculados
```

### Campo `tipo_calculo` no items.json

```json
"17.6": { "cod": "17.6", "desc": "Pintura acrílica", "un": "m2", "tipo_calculo": "sem_desconto" }
"29.2": { "cod": "29.2", "desc": "Adesivos padrão BB", "un": "m2", "tipo_calculo": "com_desconto" }
"29.24": { "cod": "29.24", "desc": "Remoção de adesivos", "un": "m2", "tipo_calculo": "entulho" }
"28.28": { "cod": "28.28", "desc": "Torneira lavatório", "un": "un", "tipo_calculo": "unitario" }
```

O items.json do c0908 já tem 529 itens extraídos. Os `com_desconto` precisam validação manual (a maioria dos m² foi classificada como `sem_desconto` por padrão).

---

## Regras de Extração de Medidas (SP2)

Nome do arquivo → medidas automáticas:

```
"01 - 16,20 x 4,63.jpg"        → largura=16.20, altura=4.63, faces=1
"01 - 3,85 x 2,18 - Faces 2.jpg" → largura=3.85, altura=2.18, faces=2
"02 - 5,38 x 4,07 - Desconto 8,39m².jpg" → desconto=8.39
"02 - vista.jpg"                → sem medidas, só imagem
"CROQUI 01 - Laje.jpg"          → croqui, legenda="Laje"
```

**Cálculo por linha:**
- `subtotal = largura × altura × faces`
- `total = subtotal − desconto`
- `total_geral = Σ total de todas as linhas da pasta`

---

## Tipos de Tabela de Memória (por `tipo_item`)

### `area` (pintura, emassamento):
| FOTO | COMPRIMENTO (m) | ALTURA (m) | DESCONTO (m²) | TOTAL (m²) |
|------|-----------------|-----------|---------------|-----------|
| 01   | 16,20           | 4,63      | —             | 75,01     |
| 02   | 8,40            | 3,00      | —             | 25,20     |
| **TOTAL** | | | | **100,21** |

### `metalico` (faces > 1):
| FOTO | COMPRIMENTO (m) | ALTURA (m) | FACES | TOTAL (m²) |
|------|-----------------|-----------|-------|-----------|
| 01   | 3,85            | 2,18      | 2     | 16,79     |

### `unitario`:
| FOTO | QUANTIDADE | TOTAL |
|------|-----------|-------|
| 01   | 1         | 1     |

---

## Mapa Visual — Etapas por Modo

### MODO TRADICIONAL — 3 Etapas

```
ETAPA 1: CABEÇALHO
  [nr_os] [data_atendimento] [agencia_codigo] [agencia_nome]
  [endereco] [responsavel] [data_elaboracao*] [descricao_select]
  
ETAPA 2: ESTRUTURA DE PASTAS
  ├─ [TÍTULO] Nome da pasta nível 1
  │   ├─ [SUBTÍTULO] Nome pasta nível 2
  │   │   ├─ [IMAGEM] foto_01.jpg
  │   │   ├─ [IMAGEM] foto_02.jpg
  │   │   └─ [QUEBRA]
  │   └─ [SUBTÍTULO] Nome pasta nível 2b
  │       └─ [IMAGEM] foto_01.jpg
  
ETAPA 3: CONFIRMAR + GERAR
  Resumo: contrato | agência | OS | serviços | fotos | motor
```

### MODO SP2 — 3 Etapas + Painel de Itens

```
ETAPA 1: CABEÇALHO (expandido)
  [nr_os] [data_atendimento] [agencia_codigo] [agencia_nome]
  [endereco] [responsavel] [data_elaboracao*] [descricao_select]
  [contrato] [elaborador] [tipo_vistoria] [empresa]

ETAPA 2: ESTRUTURA + ITENS
  ├─ [IMAGEM FACHADA] Fachada.jpg (capa)
  ├─ [TÍTULO] "1 - 1º Andar – Espaço Desativado"
  │   ├─ [SUBTÍTULO] "1.1 - Emassamento e pintura de teto"
  │   │   ├─ [IMAGEM] 01 - 16,20 x 4,63.jpg
  │   │   ├─ [IMAGEM] 02 - vista.jpg
  │   │   ├─ [CROQUI] CROQUI 01 - Laje.jpg  [legenda: Laje]
  │   │   ├─ [DESCRIÇÃO] Item 17.2 — Emassamento PVA (m²)  ← dropdown associação
  │   │   ├─ [TABELA MEMÓRIA] 16,20×4,63=75,01 / 8,40×3,00=25,20 / Total=100,21
  │   │   └─ [TABELA ITENS] 17.2 | Emassamento PVA | 100,21 | m²
  │   └─ ...
  
  PAINEL LATERAL: Associação de Itens
    [pasta de serviço] → [dropdown: código + descrição] → [total calculado]

ETAPA 3: CONFIRMAR + GERAR
  Resumo com Memória de Cálculo total
```

---

## Estrutura de Pastas por Contrato (descoberta na pasta de docs)

| Contrato | Região | Modo | Documentos Disponíveis |
|----------|--------|------|------------------------|
| 0908 | São José dos Campos | **SP** | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 1507 | Cuiabá | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 1565 | São José do Rio Preto | SP2 | Modelo RAT + Relatório fotográfico |
| 2056 | Divinópolis | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 2057 | Varginha | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 2626 | Salinas | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 2627 | Governador Valadares | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 3575 | Tangará da Serra | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |
| 6122 | Mato Grosso do Sul | Tradicional | PREVISÃO ORÇAMENTÁRIA + RELATÓRIO FOTOGRÁFICO |

---

## Próximos Passos (Wireframe)

1. **Wireframe novo** → mostrar cada tipo de bloco como card visual no passo 2
2. **Painel SP2** → cada pasta de serviço detectada + dropdown de item + total calculado
3. **Preview por bloco** → antes de gerar, mostrar lista de blocos com tipo + thumbnail
4. **Tabela de itens** → dentro do wizard, exibir os itens selecionados e totais

*AutoRelatório V5 — TM Sempre Tecnologia · 2026*
