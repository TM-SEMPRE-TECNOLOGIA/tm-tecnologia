# 🗺️ MAPA DE AUTOMAÇÕES — TM Sempre Tecnologia
**Inventário completo de automações existentes, em desenvolvimento e planejadas**
**Atualizado em:** 2026-05-27

---

## 🟢 AUTOMAÇÕES ATIVAS (Produção)

### A01 — Geração de Relatório Fotográfico (AutoRelatório V4)
| Campo | Valor |
|-------|-------|
| **Localização** | `AutoRelatorio_V4/APP/backend/` |
| **Módulo principal** | `generator.py`, `generator_sp.py`, `generator_sp2.py` |
| **Entrada** | Pasta de fotos organizada em hierarquia padrão |
| **Saída** | Arquivo `.docx` formatado com fotos e memorial de cálculo |
| **Contratos** | Todos os 9 (modos: Tradicional, SP, SP2) |
| **Status** | ✅ Estável — referência canônica |
| **Observação** | V5 deve replicar e superar este comportamento |

### A02 — Extração de Itens de Relatório (Skill)
| Campo | Valor |
|-------|-------|
| **Localização** | `Meus Plugins e Skills/relatorio-preventivo.skill` |
| **Script** | `scripts/extrair_itens.py` |
| **Entrada** | `.docx` de relatório preventivo |
| **Saída** | `.xlsx` com aba completa + aba consolidada |
| **Status** | ✅ Ativo via skill Claude Code |

### A03 — Geração de Memorial Final (Skill)
| Campo | Valor |
|-------|-------|
| **Localização** | `Meus Plugins e Skills/relatorio-preventivo.skill` |
| **Script** | `scripts/gerar_memorial.py` |
| **Entrada** | Dados extraídos do relatório |
| **Saída** | `.docx` com formatação padrão exata |
| **Status** | ✅ Ativo via skill Claude Code |

### A04 — Verificação de Divergências (Skill)
| Campo | Valor |
|-------|-------|
| **Localização** | `Meus Plugins e Skills/relatorio-preventivo.skill` |
| **Script** | `scripts/verificar_divergencias.py` |
| **Entrada** | Corpo do relatório vs memorial |
| **Saída** | Relatório de divergências |
| **Status** | ✅ Ativo via skill Claude Code |

### A05 — Verificação de Legendas de Fotos (Skill)
| Campo | Valor |
|-------|-------|
| **Localização** | `Meus Plugins e Skills/relatorio-preventivo.skill` |
| **Script** | `scripts/verificar_legendas.py` |
| **Entrada** | `.docx` do relatório |
| **Saída** | Relatório de inconsistências nas legendas |
| **Status** | ✅ Ativo via skill Claude Code |

### A06 — TM-Automatizando (Completar Relatório SP2)
| Campo | Valor |
|-------|-------|
| **Localização** | `Meus Plugins e Skills/tm-automatizando/` |
| **Entrada** | `.docx` pré-finalizado (fotos + medidas a punho) |
| **Saída** | `.docx` completo com narrativas, tabelas, memorial |
| **Contratos** | Todos os 9, foco em SP2 (1565) |
| **Status** | ✅ Ativo — padrão editorial Santa Adélia |

---

## 🔶 AUTOMAÇÕES EM DESENVOLVIMENTO

### A07 — AutoRelatório V5 (Backend)
| Campo | Valor |
|-------|-------|
| **Localização** | `AutoRelatorio_V5/backend/` |
| **Entrada** | Pasta de fotos + metadados via API |
| **Saída** | `.docx` via download |
| **Status** | ⚠️ 80% — 9 engines criados, aguarda Sprint 3 |
| **Bloqueio** | Upload de arquivos via browser não implementado |

### A08 — Upload de Fotos via FormData (Sprint 3)
| Campo | Valor |
|-------|-------|
| **Endpoint** | `POST /api/contracts/{id}/generate-with-files` |
| **Entrada** | `files: UploadFile[]` via FormData |
| **Saída** | `.docx` via response |
| **Status** | ❌ Não iniciado |
| **Spec** | A criar em `docs/specs/2026-05-27-upload-fotos.md` |

---

## 🔵 AUTOMAÇÕES PLANEJADAS (Backlog)

### A09 — QA Visual Automatizado (Playwright)
| Campo | Valor |
|-------|-------|
| **Objetivo** | Screenshot + comparação visual do frontend V5 |
| **Ferramenta** | Playwright + skill `tm-testes` |
| **Status** | 📋 Planejado — Sprint 4 |

### A10 — Scanner de Duplicações de Código
| Campo | Valor |
|-------|-------|
| **Objetivo** | Detectar funções duplicadas entre V4 e V5 |
| **Ferramenta** | Skill `finding-duplicate-functions` |
| **Status** | 📋 Planejado |

### A11 — Validador de Estrutura de Pasta (CLI)
| Campo | Valor |
|-------|-------|
| **Objetivo** | Verificar se pasta de fotos está correta antes de rodar |
| **Entrada** | Caminho da pasta |
| **Saída** | Relatório de validação com erros e avisos |
| **Status** | 📋 Planejado |

### A12 — Exportador de items.json a partir de XLSX
| Campo | Valor |
|-------|-------|
| **Objetivo** | Gerar `items.json` a partir da planilha de itens de cada contrato |
| **Entrada** | Planilha Excel por contrato |
| **Saída** | `contracts/cXXXX/items/items.json` |
| **Status** | 📋 Planejado — bloqueado por recebimento de materiais |

### A13 — Gerador de Relatório de Regressão
| Campo | Valor |
|-------|-------|
| **Objetivo** | Comparar output V5 vs relatório de exemplo por contrato |
| **Entrada** | .docx gerado pelo V5 + .docx de referência |
| **Saída** | Relatório HTML de diferenças (estrutura, fotos, formatação) |
| **Status** | 📋 Planejado — Sprint 5 |

### A14 — Pipeline de Geração em Lote
| Campo | Valor |
|-------|-------|
| **Objetivo** | Processar múltiplos contratos de uma vez |
| **Entrada** | Lista de pastas + metadados em CSV |
| **Saída** | .docx para cada contrato |
| **Status** | 📋 Planejado — pós-Sprint 3 |

### A15 — Monitor de Saúde do Backend
| Campo | Valor |
|-------|-------|
| **Objetivo** | Verificar se API V5 está respondendo corretamente |
| **Ferramenta** | Script Python + cron |
| **Status** | 📋 Planejado |

---

## 📋 LEGENDA DE STATUS

| Emoji | Status |
|-------|--------|
| ✅ | Ativo em produção |
| ⚠️ | Em desenvolvimento / parcialmente funcional |
| ❌ | Não iniciado |
| 📋 | Planejado / backlog |
| 🚫 | Depreciado |

---

## 🔗 INTEGRAÇÕES ENTRE AUTOMAÇÕES

```
A06 (TM-Automatizando)
    └── usa → A02, A03, A04, A05 (skills do relatorio-preventivo)

A07 (V5 Backend)
    ├── herda → A01 (lógica do V4)
    └── desbloqueia → A08 (Sprint 3)

A08 (Upload FormData)
    └── habilita → A09 (QA Visual), A13 (Regressão), A14 (Lote)

A12 (items.json)
    └── alimenta → A07 (9 contratos completos)
```

---

*Para adicionar nova automação, use o template em `templates/relatorio/TEMPLATE_SPEC_AUTOMACAO.md`*
