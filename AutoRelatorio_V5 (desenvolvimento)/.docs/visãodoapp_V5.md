# AutoRelatório V5 — PRD MVP
**Versão:** 5.0.0-alpha  
**Data:** 2026-05-20  
**Autor:** TM Sempre Tecnologia  
**Status:** 🟡 Planejamento

---

## 1. Contexto e Motivação

### Problema do V4
O AutoRelatório V4 nasceu como um motor único (`generator.py`) com bifurcações condicionais para cada contrato via flags `tipo_relatorio`. Com o crescimento para 9 contratos ativos, essa abordagem criou:

- **Acoplamento total:** mudar a lógica do contrato 1565 (SP2) quebra o fluxo do 0908
- **Impossibilidade de paralelismo:** não dá para evoluir dois contratos simultaneamente
- **Estado global compartilhado:** o Zustand store mistura metadados de contratos distintos
- **Templates estão "soltos":** 9 .docx no mesmo diretório sem isolamento de contexto
- **Dois motores já bifurcaram** (`generator.py` + `generator_sp.py` + `generator_sp2.py`) — a tendência é piorar

### Visão do V5
**Um contrato = um módulo completo e autônomo.**

Cada contrato possui seu próprio motor de scan, motor de Word, banco de itens, regras de cálculo, template `.docx` e configuração de interface. O core do sistema fornece apenas a infraestrutura compartilhada (servidor FastAPI, shell Next.js, componentes base).

---

## 2. Os 9 Contratos — Identidade e Modo

| # | Código | Região | Motor V4 Atual | Modo V5 |
|---|--------|--------|----------------|---------|
| 1 | **0908** | São José dos Campos | `generator.py` (tradicional) | `ContractEngine` padrão |
| 2 | **1507** | Cuiabá | `generator.py` (tradicional) | `ContractEngine` padrão |
| 3 | **1565** | São José do Rio Preto / Ribeirão Preto | `generator_sp2.py` (SP2) | `ContractEngine` com `MemoriaCalculo` |
| 4 | **2056** | Divinópolis | `generator.py` (tradicional) | `ContractEngine` padrão |
| 5 | **2057** | Varginha | `generator.py` (tradicional) | `ContractEngine` padrão |
| 6 | **2626** | Salinas | `generator.py` (tradicional) | `ContractEngine` padrão |
| 7 | **2627** | Governador Valadares | `generator.py` (tradicional) | `ContractEngine` padrão |
| 8 | **3575** | Tangará da Serra | `generator.py` (tradicional) | `ContractEngine` padrão |
| 9 | **6122** | Mato Grosso do Sul | `generator.py` (tradicional) | `ContractEngine` padrão |

> **Nota:** O contrato 1565 é o único com motor SP2 completo (memória de cálculo, croquis, faces). Os demais usam o motor tradicional, mas no V5 cada um tem seu próprio módulo isolado — mesmo que internamente deleguem para o engine base.

---

## 3. Arquitetura do V5 — Lógica Pura

### 3.1 Princípio Fundamental: Plugin de Contrato

```
┌─────────────────────────────────────────────────┐
│                 CORE V5                          │
│  FastAPI Shell + Next.js Shell + Componentes    │
└────────────────┬────────────────────────────────┘
                 │  ContractRegistry
    ┌────────────┼────────────────────────┐
    ▼            ▼                        ▼
┌────────┐  ┌────────┐  ...  ┌──────────┐
│ c0908  │  │ c1565  │       │  c6122   │
│ engine │  │ engine │       │  engine  │
│ items  │  │ items  │       │  items   │
│ rules  │  │ rules  │       │  rules   │
│ tpl    │  │ tpl    │       │  tpl     │
└────────┘  └────────┘       └──────────┘
```

### 3.2 Interface ContractEngine (Python ABC)

Todo contrato implementa esta interface:

```python
class ContractEngine(ABC):
    contract_id: str           # "1565"
    contract_name: str         # "São José do Rio Preto"
    template_file: str         # "MODELO-1565.docx"
    reading_modes: list[str]   # ["disco", "app"]
    
    @abstractmethod
    def scan(self, root_path: str, logger) -> list:
        """Varre a pasta e retorna array de conteudo"""
    
    @abstractmethod
    def build_word(self, modelo_path, conteudo, output_path, meta) -> str:
        """Gera o .docx final. Retorna path do arquivo gerado."""
    
    @abstractmethod
    def get_items(self) -> dict:
        """Retorna banco de itens do contrato (código → desc, unidade)"""
    
    @abstractmethod
    def get_meta_fields(self) -> list[MetaField]:
        """Retorna campos de cabeçalho que o formulário dinâmico deve exibir"""
    
    @abstractmethod
    def validate_folder(self, root_path: str) -> ValidationResult:
        """Valida se a estrutura de pastas atende as regras do contrato"""
```

### 3.3 ContractRegistry

```python
# core/registry.py
CONTRACTS = {
    "0908": Contract0908Engine(),
    "1507": Contract1507Engine(),
    "1565": Contract1565Engine(),
    "2056": Contract2056Engine(),
    "2057": Contract2057Engine(),
    "2626": Contract2626Engine(),
    "2627": Contract2627Engine(),
    "3575": Contract3575Engine(),
    "6122": Contract6122Engine(),
}

def get_engine(contract_id: str) -> ContractEngine:
    return CONTRACTS[contract_id]
```

### 3.4 API Routes V5 (simplificadas)

```
GET  /api/contracts              → lista todos os 9 contratos
GET  /api/contracts/{id}         → metadata + fields do contrato
POST /api/contracts/{id}/scan    → { root_path } → conteudo[]
POST /api/contracts/{id}/generate → { meta, conteudo } → .docx
POST /api/contracts/{id}/validate → { root_path } → ValidationResult
GET  /api/contracts/{id}/items   → banco de itens do contrato
```

---

## 4. Fluxo Principal V5

```
[1] Usuário abre o app
      ↓
[2] Tela de Seleção de Contrato (9 cards)
      ↓  clica em "1565 — São José do Rio Preto"
[3] Contexto carregado: engine 1565, itens 1565, formulário 1565
      ↓
[4] Wizard — Passo 1: Dados da OS
    Campos: nr_os, data_atendimento, agencia_codigo, agencia_nome, endereço, responsável
      ↓
[5] Wizard — Passo 2: Selecionar pasta de fotos
    Modo Disco: browse → scan automático
    Modo App: arrastar e classificar fotos manualmente
      ↓
[6] Preview do conteúdo escaneado
    Lista hierárquica de pastas/imagens + thumb grid
      ↓
[7] (Contrato 1565 apenas) Associar itens de contrato por pasta
    Dropdown com banco de itens → memória de cálculo automática
      ↓
[8] Gerar Relatório → POST /api/contracts/1565/generate
      ↓
[9] Download .docx / abrir no Word
```

---

## 5. Diferenças V4 → V5

| Aspecto | V4 | V5 |
|---------|----|----|
| Motores | 3 arquivos (`generator`, `generator_sp`, `generator_sp2`) | 9 módulos isolados com interface comum |
| Estado global | Zustand com flags `tipo_relatorio` | Store por contrato (`useContractStore(id)`) |
| Templates | Todos no mesmo `/templates/` | `/contracts/{id}/template/` |
| Itens de contrato | Hardcoded em `utils_sp2.py` | `items.json` por contrato |
| Configuração | `tipo_relatorio: str` passado na request | `contract_id` seleciona o engine completo |
| Interface | Modo único com sidebar | Tela de seleção + contexto isolado por contrato |
| Regras de validação | Nenhuma | `validate_folder()` por contrato |
| Evolução | Mudança no core afeta todos | Mudança em `c1565/` não toca `c0908/` |

---

## 6. MVP — Escopo da V5.0

### ✅ Incluído no MVP

- [ ] Core: `ContractEngine` ABC + `ContractRegistry`
- [ ] Scaffold dos 9 módulos de contrato (estrutura de pastas)
- [ ] Motor base migrado para `ContractEngine` (contratos tradicionais: 0908, 1507, 2056, 2057, 2626, 2627, 3575, 6122)
- [ ] Motor SP2 migrado e isolado para contrato 1565
- [ ] API V5: endpoints `/api/contracts/{id}/...`
- [ ] Frontend: tela de seleção de contrato (9 cards)
- [ ] Frontend: wizard de 3 passos por contrato
- [ ] Frontend: store por contrato (sem estado global compartilhado)
- [ ] Preview de conteúdo escaneado

### ❌ Fora do MVP (V5.1+)

- Motor de IA para auto-classificação de fotos
- Modo colaborativo (multi-usuário)
- Dashboard de métricas por contrato
- Exportação para formatos além de .docx
- Integração com portal de OS (auto-preenchimento de cabeçalho)
- Histórico de relatórios gerados

---

## 7. Stack Técnica (sem mudanças)

- **Backend:** Python 3.10+, FastAPI, python-docx, Pillow, Uvicorn
- **Frontend:** Next.js 14, React 18, Zustand, TypeScript, Tailwind CSS
- **Dev:** pytest para backend, sem testes E2E no MVP

---

## 8. Métricas de Sucesso do MVP

| Métrica | Meta |
|---------|------|
| Todos os 9 contratos funcionam independentemente | 100% |
| Tempo de geração de relatório | ≤ 30s para 100 fotos |
| Mudança em contrato X não afeta contrato Y | 0 regressões |
| Cobertura de testes backend | ≥ 70% por engine |

---

## 9. Riscos

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| Migração do motor SP2 quebra edge cases | Média | Manter `generator_sp2.py` original como fallback durante transição |
| Templates Word com placeholders inconsistentes | Alta | Auditar os 9 .docx antes da migração |
| Frontend com estado duplicado entre contratos | Média | Usar factory pattern no Zustand |

---

*AutoRelatório V5 — TM Sempre Tecnologia · 2026*
