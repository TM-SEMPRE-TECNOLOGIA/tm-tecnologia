# CONTEXTO GERAL DE SESSÕES — TM Sempre Tecnologia
> Consolidado em: 29/05/2026  
> Gerado por: Claude Code (claude-sonnet-4-6)  
> Fonte: todas as memórias persistidas + PROJECT_MEMORY.md

---

## 1. QUEM É THIAGO E O QUE ELE CONSTRÓI

**Thiago Nascimento Barbosa** — fundador da **TM Sempre Tecnologia**, empresa de engenharia e manutenção predial com contratos bancários institucionais (Banco do Brasil).

Não é desenvolvedor acadêmico. É um **construtor pragmático** que usa tecnologia para resolver problemas operacionais reais de campo. Cada app que cria tem propósito direto: eliminar trabalho manual, acelerar entregas, manter qualidade institucional.

**Email:** thiagonascimento.barbosapro@gmail.com
**Site** thiagonascimentobarbosapro.com
---

## 2. AS 3 PASTAS — UNIVERSO DE TRABALHO

```
C:\Users\thiag\Desktop\
├── tm-tecnologia\          ← apps em desenvolvimento ativo
├── TM-MEUS-APPS\           ← apps prontos, skills, design system, legado
└── 000 - Minha Demanda\    ← demandas operacionais reais com prazo real
```

O `_workspace/` em `tm-tecnologia` é o **centro de controle** que conecta tudo:
`C:\Users\thiag\Desktop\tm-tecnologia\_workspace\`

---

## 3. PROJETO PRINCIPAL — AutoRelatório V5

### 3.1 O que é

Plataforma full-stack (Python FastAPI + Next.js) que **gera automaticamente relatórios fotográficos preventivos** em `.docx` para 9 contratos do Banco do Brasil.

O operador preenche dados da OS, seleciona o contrato, associa fotos a itens, informa medidas → sistema gera o Word formatado conforme template oficial.

**Path:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\`  
**Iniciar:** `INICIAR.bat` (duplo-clique)  
**URLs:** http://localhost:3000 (app) | http://localhost:5000/docs (API)

### 3.2 Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | Next.js 16 + React 19 + TypeScript + Tailwind 4 + Zustand 5 |
| Backend | FastAPI 0.111 + Python 3.11 + Pydantic 2 |
| Geração Word | python-docx 1.1 |
| Imagens | Pillow 10 (importado, uso pendente) |

### 3.3 Arquitetura — Plugin/Registry/ABC

```
ContractEngine (ABC)         ← contrato de interface
    ↓ implementado por
9 engines (1 por contrato)   ← módulos isolados em contracts/cXXXX/
    ↓ registrados em
registry.py                  ← factory central: get_engine("1565") → engine
    ↓ chamado por
core/server.py               ← FastAPI, 7 endpoints
```

**Regra de ouro:** 1 contrato = 1 módulo Python isolado. Nunca mudar `core/` para acomodar um contrato específico.

### 3.4 Estrutura de Arquivos Críticos

```
backend/core/server.py            ← CRÍTICO: FastAPI + todos os endpoints
backend/core/contract_engine.py   ← CRÍTICO: interface abstrata ABC
backend/core/registry.py          ← CRÍTICO: factory dos 9 engines
backend/contracts/cXXXX/
    engine/engine.py              ← implementação por contrato
    engine/scanner_*.py           ← scan(root_path) → conteudo[]
    engine/word_builder_*.py      ← build_word() → .docx
    items/items.json              ← banco de itens
    template/MODELO-XXXX.docx     ← template Word com {{placeholders}}

frontend/app/page.tsx             ← CRÍTICO: orquestrador da aplicação
frontend/hooks/useBlocks.ts       ← CRÍTICO: lógica de blocos + cálculos
frontend/lib/api.ts               ← CRÍTICO: todas as chamadas HTTP
frontend/store/contractStore.ts   ← estado global (Zustand)
frontend/lib/types.ts             ← interfaces TypeScript globais
```

### 3.5 Os 9 Contratos

| Código | Região | UF | Modo | items.json |
|--------|--------|----|----|-----------|
| **0908** | São José dos Campos | SP | **SP** | ✅ ok |
| **1507** | Cuiabá | MT | Tradicional | ✅ ok |
| **1565** | SJRP / Ribeirão Preto | SP | **SP2 ⭐ EXCLUSIVO** | ✅ ok (81 itens) |
| **2056** | Divinópolis | MG | Tradicional | ⚠️ vazio |
| **2057** | Varginha | MG | Tradicional | ⚠️ vazio |
| **2626** | Salinas | MG | Tradicional | ✅ ok |
| **2627** | Gov. Valadares | MG | Tradicional | ✅ ok |
| **3575** | Tangará da Serra | MT | Tradicional | ✅ ok |
| **6122** | Mato Grosso do Sul | MS | Tradicional | ⚠️ vazio |

### 3.6 conteudo[] — Contrato Único de Dados

O array `conteudo[]` é o único contrato de dados entre scanner e builder. Tipos possíveis:

```python
"» Título"                          # str com prefixo » = título de seção
{"imagem": path}                    # foto normal
{"quebra_pagina": True}             # quebra de página
{"memoria_calculo": {...}}          # tabela SP (c0908)
{"tabela_itens_sp2": {...}}         # tabela SP2 (c1565)
{"croqui": path, "legenda": str}    # croqui SP2 (c1565)
{"enunciado_item": {...}}           # texto item SP2 (c1565)
```

### 3.7 Placeholders Word

```
{{nr_os}}  {{dt_atend}}  {{ag_cod}}  {{ag_nome}}
{{endereco}}  {{responsavel_dependencia}}  {{dt_elab}}  {{start_here}}
```

### 3.8 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check |
| POST | `/generate` | Geração flat → FileResponse (.docx) |
| GET | `/api/contracts` | Lista os 9 contratos |
| GET | `/api/contracts/{id}` | Detalhes de um contrato |
| POST | `/api/contracts/{id}/scan` | Escaneia pasta |
| POST | `/api/contracts/{id}/generate` | Geração por contrato |
| GET | `/api/contracts/{id}/items` | Banco de itens |

### 3.9 Status por Área (29/05/2026)

| Área | % | Status |
|------|---|--------|
| UI / Layout | 100% | ✅ |
| Step 1 — Formulário | 100% | ✅ |
| Step 2 — Blocos | 90% | ✅ |
| Step 3 — Resumo | 100% | ✅ |
| Preview (tabelas + thumbs) | 100% | ✅ |
| Backend — 9 contratos | 80% | ⚠️ SP2 ok, trad/sp aguardam teste |
| Bridge API | 100% | ✅ |
| Upload fotos → backend | 0% | ❌ Sprint 3 |
| Parsers Excel | 0% | ❌ Não iniciado |
| Testes | 0% | ❌ Zero cobertura |

### 3.10 Roadmap — Próximas Sprints

**Sprint 3 — Upload de Fotos (Crítico)**
- Problema: browser não fornece `root_path` → .docx gerado só com cabeçalho
- Solução: `POST /api/contracts/{id}/generate-with-files` com `files: UploadFile[]`
- Frontend envia files via FormData; backend salva em tmpdir → roda scanner → gera .docx

**Sprint 4 — Parsers Excel**
- `parseValoresExcel()` Python — 2 tipos: SP2 + Tradicional
- Endpoint `POST /api/contracts/{id}/parse-excel`
- UI: botão "Importar Planilha" no Step 2

**Sprint 5 — QA + Deploy**
- Testes E2E Playwright (`/tm-testes`)
- pytest backend (contratos críticos)
- Deploy: Vercel (frontend) + Railway (backend)

---

## 4. REGRAS DE NEGÓCIO CRÍTICAS

| ID | Regra | Impacto se violada |
|----|-------|-------------------|
| **RN-01** | Contrato 1565 = **EXCLUSIVO SP2** — nunca Tradicional | Relatório incorreto, rejeição pelo BB |
| **RN-02** | Sort: "Vista ampla" → numérico → alfabético → "Detalhes" | Ordem errada nas fotos |
| **RN-03** | Altura imagem: 10cm (Trad/SP) / 7cm (SP2 c1565) | Layout incorreto |
| **RN-04** | `conteudo[]` = único contrato scanner ↔ builder | Quebra de compatibilidade |
| **RN-05** | "Faces 2" no nome do arquivo = área × 2 | Cálculo de área errado |
| **RN-06** | Placeholders exatos: `{{nr_os}}`, `{{dt_atend}}`, etc. | Template não preenchido |
| **RN-07** | 1 contrato = 1 módulo Python isolado | Acoplamento perigoso |
| **RN-08** | Nunca mudar core para acomodar contrato específico | Contamina todos |

---

## 5. HISTÓRIA DO ECOSSISTEMA — LINHA DO TEMPO

| Versão | Data | Destaque |
|--------|------|----------|
| Proto-V1 (TM Studio) | — | Primeira FastAPI, sem modo SP |
| V0.9/V0.99 (NX Relatorios) | — | **Ponto de fusão**: UI NX + lógica SP |
| V2 | 19/04/2026 | Scaffold Next.js, backend incompleto |
| V3 | — | Primeira versão completa (2 modos, 20+ endpoints) |
| V3.2 | 03/05/2026 | Placeholders `{{campo}}`, 70+ testes |
| V4 | 12/05/2026 | SP2, Zustand store, 4 views, modo app |
| **V5** | **Ativo** | Plugin pattern, 9 contratos, PREVC, Next.js 16 |

### Módulos canônicos (V4 como referência)
- `utils_sp.py` → `parse_medidas_arquivo`, `formatar_descricao_tecnica`
- `utils_sp2.py` → `parse_medidas_sp2`, `detectar_item_por_pasta`, `e_croqui`
- `generator_sp2.py` → Scanner SP2 completo
- `word_utils.py` → `extract_placeholders`, `substitute_placeholders`, `analisar_imagem`

### Perdas críticas (não portadas para V5)
1. `extrair_itens_docx.py` — extrai itens de .docx existente
2. `dump.json` — snapshot de `conteudo[]` para fixtures de teste
3. TM Gerenciador V-2 — 15 componentes CMMS completos

---

## 6. ECOSSISTEMA DE OS — FLUXO OPERACIONAL

A vida de uma OS segue 5 estágios no WhatsApp:

| Estágio | Nome do Grupo | O que acontece |
|---------|--------------|----------------|
| 1 | `1️⃣ LEV - [CIDADE] [CONTRATO] - [TÉCNICO]` | Levantamento: fotos + medidas |
| 2 | `2️⃣ ORÇ ENV` | Orçamento montado e enviado |
| 3 | `3️⃣ ORÇ APROV` | Orçamento aprovado |
| 4 | `4️⃣ EXECUTANDO` | Fotos dos serviços executados |
| 5 | `5️⃣ CONCLUÍDA` | OS encerrada, grupo arquivado |

### Formato do levantamento no Zap (estágio 1)
- Foto → medição `L/A` (ex: `16.00/7.00`)
- Descontos inline: `Descontar janelas 16.00/2.50`
- Fotos de detalhe sem texto = pertencem à medição anterior
- Separador de ambiente = texto puro (ex: `Auto ATENDIMENTO`)
- Multiplicador: `5.00/0.60x2 lados`
- Unidades: `Piso tátil 21 und`

### App Futuro: TM·Zap Inspeção
Substitui WhatsApp no estágio 1 com:
- Mesma UX do Zap (sem fricção)
- Fotos + medidas estruturadas (não só texto livre)
- Exportação direta para o AutoRelatório (modo APP)
- Gestão dos 5 estágios por OS

---

## 7. SKILL RELATÓRIO PREVENTIVO (CEF)

**Skill:** `/relatorio-preventivo` — para contratos Caixa Econômica Federal

**Guia completo:** `C:\Users\thiag\Desktop\tm-tecnologia\_workspace\GUIA_RELATORIO_PREVENTIVO.html`  
(HTML standalone, tema escuro laranjado, abrir no browser)

### 4 Etapas
1. **Extrair itens** → gera Excel com aba completa + aba consolidada
2. **Gerar memorial final** → Word (.docx) com formatação padrão
3. **Verificar divergências** → cruza totais das tabelas do relatório
4. **Verificar legendas** → sequência + consistência com tabelas

**Documentos reais:** `C:\Users\thiag\Desktop\tm-tecnologia\Documentos Preventivas\`  
**Demandas ativas:** `C:\Users\thiag\Desktop\000 - Minha Demanda\`

---

## 8. DOCUMENTAÇÃO DO WORKSPACE

### Documentos em `.context/` (AutoRelatório V5)

| Arquivo | Quando usar |
|---------|------------|
| `INDEX.md` | Antes de qualquer sessão — índice geral |
| `planning.md` | Antes de mudanças de arquitetura |
| `ARQUITETURA_FINAL_V5.md` | Para entender decisões de design |
| `BLOCOS_DINAMICOS.md` | Para modificar BlockCard/BlockList |
| `TABELA_VALORES_PADRAO.md` | Para implementar parsers Excel |
| `INTEGRACAO_RELATORIO_PREVENTIVO.md` | Para integrar V5 ↔ skill preventivo |

### Documentação forense gerada (26/05/2026)
- `ENGENHARIA_REVERSA_COMPLETA.html` — mapa visual interativo (9 abas)
- `PROXIMO_PASSO.md` — guia executivo Sprint 3 com código pronto
- `PROJECT_MEMORY.md` — engenharia reversa completa do V5

---

## 9. ALERTAS TÉCNICOS PARA FUTURAS SESSÕES

> Estes pontos foram identificados como riscos ou inconsistências nas sessões anteriores.

- `generator_app.py` (modo pasta plana) pode estar incompleto no V5
- Markup `<RED>` em `utils_sp.py` pode não estar sendo aplicado em `word_utils_sp.py`
- `gerar_ipuiuna.py` — script one-off no backend V4, sem documentação
- `FormularioDinamico_integration.tsx` vs `FormularioDinamico.tsx` — verificar diferença
- items.json de 2056, 2057 e 6122 estão **vazios** — precisam ser populados
- Sprint 3 (upload de fotos) é o bloqueio atual mais crítico para o V5 ser funcional de ponta a ponta

---

## 10. COMO RETOMAR O TRABALHO

```
1. Abrir VS Code em: C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
2. Ler: PROJECT_MEMORY.md (engenharia reversa completa)
3. Ler: .context/INDEX.md (documentação PREVC)
4. Iniciar app: duplo-clique INICIAR.bat
5. Verificar: http://localhost:3000 (frontend) | http://localhost:5000/docs (API)
6. Sprint atual: ver PROXIMO_PASSO.md ou .MD aleatorios/PENDENCIAS_V5.md
```

---

*Atualizado: 29/05/2026 — Claude Code (claude-sonnet-4-6)*  
*Fonte: PROJECT_MEMORY.md + todas as memórias em ~/.claude/projects/c--Users-thiag-Desktop-tm-tecnologia/memory/*
