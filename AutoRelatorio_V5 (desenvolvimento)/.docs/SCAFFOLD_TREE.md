# AutoRelatório V5 — Scaffold Completo

```
AutoRelatorio_V5/
│
├── .docs/
│   ├── PRD_MVP_V5.md              ← Product Requirements Document
│   └── SCAFFOLD_TREE.md           ← Este arquivo
│
├── backend/
│   │
│   ├── core/                      ← Infraestrutura compartilhada
│   │   ├── __init__.py
│   │   ├── contract_engine.py     ← ABC ContractEngine + MetaField + ValidationResult
│   │   ├── registry.py            ← ContractRegistry (get_engine, list_contracts)
│   │   └── server.py              ← FastAPI: /api/contracts/{id}/scan|generate|...
│   │
│   ├── contracts/                 ← 9 módulos isolados
│   │   │
│   │   ├── c0908/                 ← São José dos Campos
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py      ← Contract0908Engine (implements ContractEngine)
│   │   │   │   ├── scanner.py     ← build_content_from_root (migrado de generator.py)
│   │   │   │   └── word_builder.py← inserir_conteudo (migrado de word_utils.py)
│   │   │   ├── items/
│   │   │   │   └── items.json     ← banco de itens MAFFENG do contrato
│   │   │   ├── template/
│   │   │   │   └── MODELO-0908.docx
│   │   │   └── tests/
│   │   │       └── test_engine.py
│   │   │
│   │   ├── c1507/                 ← Cuiabá (mesma estrutura de c0908)
│   │   ├── c1565/                 ← São José do Rio Preto / Ribeirão Preto
│   │   │   ├── engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py      ← Contract1565Engine (motor SP2 completo)
│   │   │   │   ├── scanner_sp2.py ← build_content_sp2 (migrado de generator_sp2.py)
│   │   │   │   ├── word_builder_sp2.py ← inserir_conteudo_sp2 (migrado de word_utils_sp2.py)
│   │   │   │   ├── utils_sp2.py   ← parse_medidas_sp2, ITENS_CONTRATO_SP2 (migrado)
│   │   │   │   └── folder_rules.py← regras de validação de pasta SP2
│   │   │   ├── items/
│   │   │   │   └── items.json     ← ITENS_CONTRATO_SP2 exportado como JSON
│   │   │   ├── template/
│   │   │   │   └── MODELO-1565.docx
│   │   │   └── tests/
│   │   │       ├── test_engine.py
│   │   │       └── test_scanner_sp2.py
│   │   │
│   │   ├── c2056/                 ← Divinópolis
│   │   ├── c2057/                 ← Varginha
│   │   ├── c2626/                 ← Salinas
│   │   ├── c2627/                 ← Governador Valadares
│   │   ├── c3575/                 ← Tangará da Serra
│   │   └── c6122/                 ← Mato Grosso do Sul
│   │
│   ├── output/                    ← Relatórios gerados (gitignored)
│   └── requirements.txt
│
└── frontend/
    │
    ├── app/
    │   ├── layout.tsx
    │   └── page.tsx               ← Router: ContractSelector → Wizard → Report
    │
    ├── components/
    │   ├── shell/
    │   │   ├── AppShell.tsx       ← Layout fixo com sidebar
    │   │   ├── Topbar.tsx
    │   │   └── ConsoleWatcher.tsx
    │   │
    │   ├── views/
    │   │   ├── ContractSelectorView.tsx  ← NOVO: tela dos 9 cards de contrato
    │   │   ├── WizardView.tsx            ← NOVO: wizard 3 passos (OS → Pasta → Gerar)
    │   │   ├── OrganizarView.tsx         ← modo app (fotos drag & drop)
    │   │   └── RelatoriosView.tsx
    │   │
    │   └── contract/
    │       ├── ContractCard.tsx     ← Card de contrato na tela de seleção
    │       ├── MetaForm.tsx         ← Formulário dinâmico (campos do cabeçalho)
    │       ├── ContentPreview.tsx   ← Preview hierárquico do scan
    │       ├── ItemsPanel.tsx       ← (SP2) associar itens por pasta
    │       └── GenerateButton.tsx
    │
    ├── store/
    │   ├── useContractStore.ts     ← NOVO: store por contrato (factory pattern)
    │   └── useGlobalStore.ts       ← tema, navegação, estado global mínimo
    │
    ├── data/
    │   └── contracts-meta.ts       ← metadados estáticos dos 9 contratos para UI
    │
    └── lib/
        └── api.ts                  ← cliente HTTP para /api/contracts/{id}/...
```

---

## Regra de Ouro V5

> **Nada de código de contrato fora de `/contracts/cXXXX/`.**  
> O `core/` só conhece a interface `ContractEngine`.  
> O frontend só fala com a API — nunca importa lógica de contrato diretamente.

---

## Ciclo de Adição de Novo Contrato

1. Criar pasta `/backend/contracts/cNNNN/`
2. Implementar `engine.py` herdando `ContractEngine`
3. Criar `items/items.json` com o banco de itens
4. Colocar o `.docx` em `template/`
5. Registrar no `core/registry.py`
6. Adicionar o card em `frontend/data/contracts-meta.ts`

→ Zero mudanças no core, zero impacto nos outros contratos.
```
