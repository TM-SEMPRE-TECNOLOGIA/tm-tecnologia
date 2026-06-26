# 🗺️ CONTEXTO DO PROJETO — TM Sempre Tecnologia
**Documento de onboarding para agentes IA e colaboradores novos**
**Atualizado em:** 2026-05-27

---

## 🏢 Empresa

**TM Sempre Tecnologia** — empresa de engenharia e automação que presta serviços de manutenção predial para o Banco do Brasil em 9 regiões do Brasil.

**Operador Principal:** Thiago Nascimento  
**Email:** thiagonascimento.barbosapro@gmail.com  
**Stack Principal:** Python · FastAPI · Next.js · TypeScript · python-docx · Playwright · Claude AI

### 🌐 Ecossistema Completo

Este projeto faz parte de um ecossistema de três pilares controlado a partir do `_workspace/`:

| Pilar | Pasta | Papel |
|-------|-------|-------|
| 🏭 Produto | `C:\Users\thiag\Desktop\tm-tecnologia\` | AutoRelatório V5 — sistema principal |
| 🔧 Ferramentas | `C:\Users\thiag\Desktop\TM-MEUS-APPS\` | Apps, Skills Claude Code, Design System TM |
| 📋 Operação | `C:\Users\thiag\Desktop\000 - Minha Demanda\` | Controle de demandas reais de campo (BB) |

> O `_workspace/` dentro de `tm-tecnologia` é o **hub central** — governando automações, prompts e memória técnica para os três pilares.  
> Mapa detalhado: [`_workspace/ECOSISTEMA_TM.md`](_workspace/ECOSISTEMA_TM.md)

---

## 🎯 Produto Principal: AutoRelatório V5

Sistema que **gera automaticamente relatórios fotográficos preventivos** (`.docx`) a partir de pastas de fotos organizadas. Substitui trabalho manual de ~4 horas por execução em segundos.

### Contexto de Negócio
- Os contratos são com o **Banco do Brasil** (BB)
- Cada contrato tem um **código**, uma **região** e um **modo de processamento**
- Os relatórios seguem templates `.docx` com placeholders como `{{nr_os}}`, `{{ag_cod}}` etc.
- Dois formatos visuais principais: **Tradicional** (2 colunas portrait) e **SP2** (croquis + faces)

### Os 9 Contratos

| Código | Região | Modo | Status V5 |
|--------|--------|------|-----------|
| 0908 | São Paulo / SJC | SP | 🔶 Engine criado |
| 1507 | Cuiabá | Tradicional | 🔶 Engine criado |
| 1565 | S.J.R.Preto / Ribeirão Preto | **SP2 ⭐ ÚNICO** | 🔶 Engine criado |
| 2056 | Divinópolis | Tradicional | 🔶 Engine criado |
| 2057 | Varginha | Tradicional | 🔶 Engine criado |
| 2626 | Salinas | Tradicional | 🔶 Engine criado |
| 2627 | Gov. Valadares | Tradicional | 🔶 Engine criado |
| 3575 | Tangará da Serra | Tradicional | 🔶 Engine criado |
| 6122 | Mato Grosso do Sul | Tradicional | 🔶 Engine criado |

---

## 📁 Estrutura de Repositório

```
c:\Users\thiag\Desktop\tm-tecnologia\
├── _workspace/                  ← ESTE WORKSPACE (automação + docs)
├── AutoRelatorio_V5/            ← Produto principal (em desenvolvimento)
│   ├── backend/
│   │   ├── core/                ← Módulos compartilhados
│   │   │   ├── contract_engine.py  ← ABC ContractEngine
│   │   │   ├── registry.py         ← 9 engines registrados
│   │   │   ├── word_utils*.py      ← Builders Word
│   │   │   └── utils_sp*.py        ← Parsers
│   │   └── contracts/
│   │       └── cXXXX/           ← Módulo isolado por contrato
│   │           ├── engine/      ← engine.py + scanner + word_builder
│   │           ├── items/       ← items.json
│   │           └── template/    ← MODELO-XXXX.docx
│   ├── frontend/                ← Next.js App Router
│   └── run.bat                  ← Inicializador
├── AutoRelatorio_V4/            ← Versão anterior (referência canônica)
│   └── APP/backend/             ← Código-fonte Python de referência
└── Documentos Preventivas/      ← Documentos reais por contrato
    ├── 1 - CONTRATO - DIVINÓPOLIS - 2056 - ATUALIZADO/
    ├── 2 - CONTRATO - VARGINHA - 2057 - ATUALIZADO/
    ├── ... (8 contratos)
    └── MEMORIAL DE ITENS - LOTE SP.xlsx
```

---

## 🧠 Arquitetura do AutoRelatório V5

### Contrato de Dados Central: `conteudo[]`

O array `conteudo[]` é o **único ponto de integração** entre scanner e word_builder:

```python
conteudo = [
    "» Título da Seção",           # str com prefixo »
    {"imagem": "/path/foto.jpg"},  # foto normal
    {"quebra_pagina": True},       # quebra de página
    {"memoria_calculo": {...}},    # tabela SP (c0908)
    {"tabela_itens_sp2": {...}},   # tabela SP2 (c1565)
    {"croqui": path, "legenda": str},  # croqui SP2
    {"enunciado_item": {...}},     # texto item SP2
]
```

### Regras de Negócio Críticas (NUNCA VIOLAR)

| ID | Regra |
|----|-------|
| RN-01 | Contrato 1565 é o ÚNICO que usa modo SP2 |
| RN-02 | Sort: "vista ampla" → numérico → alfabético → "detalhes" |
| RN-03 | Altura padrão de imagem = **10cm** (Tradicional e SP). **7cm exclusivo do c1565 (SP2)** |
| RN-04 | `conteudo[]` é o único contrato de dados entre scanner e builder |
| RN-05 | "Faces 2" no nome do arquivo = área × 2 (SP2) |
| RN-06 | Placeholders: `{{nr_os}}`, `{{dt_atend}}`, `{{ag_cod}}`, `{{ag_nome}}`, `{{endereco}}`, `{{responsavel_dependencia}}`, `{{dt_elab}}`, `{{start_here}}` |
| RN-07 | Arquitetura: 1 contrato = 1 módulo Python isolado |
| RN-08 | Nunca mudar core para acomodar contrato específico |

---

## 🔧 Stack Técnico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend | Python + FastAPI | 3.11+ |
| Geração DOCX | python-docx | latest |
| Frontend | Next.js + TypeScript | 14+ App Router |
| Estado | Zustand | latest |
| Testes E2E | Playwright | latest |
| IA | Claude API (Anthropic) | claude-sonnet-4-6 |
| Skills | Claude Code Skills | antigravity + TM custom |

---

## 📚 Biblioteca de Skills Existentes

**Localização:** `C:\Users\thiag\Desktop\TM-MEUS-APPS\Meus Plugins e Skills\`

| Skill | Propósito |
|-------|-----------|
| `relatorio-preventivo.skill` | Extrair itens, gerar memorial, verificar divergências |
| `relatorio-preventivo-v2.skill` | Versão 2 do skill preventivo |
| `tm-automatizando` | Completar relatórios pré-finalizados (SP2) |
| `tm-testes` | Automação E2E com Playwright |
| `tm-design-system-plugin` | Design system TM |
| `antigravity-awesome-skills` | Skills base: brainstorming, debugging, code review |
| `organizar-relatorio.skill` | Organização de relatórios |
| `legenda-descricao-sp2.skill` | Legendas e descrições SP2 |

---

## 🏃 Como Iniciar o Projeto

```bash
# AutoRelatório V5
cd c:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5
# Duplo-clique em run.bat  OU:
# Backend: cd backend && uvicorn core.server:app --port 5000
# Frontend: cd frontend && npm run dev

# URLs:
# App: http://localhost:3000
# API Docs: http://localhost:5000/docs
```

---

## 📊 Status Atual (2026-05-27)

| Componente | Status |
|-----------|--------|
| UI Layout | ✅ 100% |
| Step 1 Formulário | ✅ 100% |
| Step 2 Blocos | ⚠️ 90% |
| Step 3 Resumo | ✅ 100% |
| Preview (tabelas+thumbs) | ✅ 100% |
| Backend 9 contratos | ⚠️ 80% |
| Bridge API | ✅ 100% |
| Upload fotos → backend | ❌ 0% (Sprint 3) |

### Próximo Sprint Crítico
**Sprint 3:** POST `/api/contracts/{id}/generate-with-files` — browser envia files via FormData, backend salva em tmpdir → roda scanner → gera .docx.

---

*Para mais detalhes técnicos, consulte: `AutoRelatorio_V5/.context/` e `AutoRelatorio_V5/.docs/`*
