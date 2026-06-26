# PROJECT_MEMORY.md — AutoRelatório V5
> Engenharia Reversa Completa + Memória Técnica Permanente  
> Gerado por: Claude Code (claude-sonnet-4-6)  
> Data: 29/05/2026  
> Metodologia: Análise Forense Profunda — PREVC

---

# 1. VISÃO GERAL DO PROJETO

## 1.1 Nome e Objetivo

**AutoRelatório V5** — Plataforma full-stack de geração automática de relatórios fotográficos preventivos para contratos do **Banco do Brasil**.

Objetivo central: eliminar o trabalho manual de montagem de relatórios `.docx` de manutenção predial. O operador de campo acessa o app, preenche os dados da OS, associa fotos a itens do contrato, informa as medidas — e o sistema gera automaticamente o relatório Word formatado conforme o template oficial de cada contrato bancário.

**Empresa responsável:** TM Sempre Tecnologia  
**Domínio:** Engenharia e manutenção predial — contratos bancários institucionais  
**Versão:** 5.0.0 (MVP em desenvolvimento)

## 1.2 Stack Tecnológica

| Camada | Tecnologia | Versão | Propósito |
|--------|-----------|--------|-----------|
| **Frontend** | Next.js | 16.1.6 | Framework React com SSR/App Router |
| | React | 19.2.3 | UI declarativa |
| | TypeScript | 5.x | Type safety |
| | Zustand | 5.0.13 | State management global |
| | Tailwind CSS | 4.2.2 | Estilização utilitária |
| | Framer Motion | 12.34.4 | Animações (importado, uso parcial) |
| | Fabric.js | 7.3.1 | Canvas (importado, não usado ainda) |
| **Backend** | FastAPI | 0.111.0 | Web framework Python ASGI |
| | Uvicorn | 0.29.0 | ASGI server |
| | python-docx | 1.1.0 | Geração e manipulação de DOCX |
| | Pillow | 10.0.0 | Processamento de imagens |
| | Pydantic | 2.0 | Validação e serialização de dados |

## 1.3 Arquitetura Identificada

**Plugin/Registry Pattern + Factory Pattern + Abstract Engine Pattern**

- 9 contratos, cada um com seu próprio módulo Python isolado
- Registry centralizado que mapeia `contrato_id → engine`
- Interface abstrata `ContractEngine` (ABC) que todos os contratos implementam
- Frontend 3-passos orquestrado por `page.tsx` com estado via hooks + Zustand

## 1.4 Padrões Utilizados

- **Plugin Pattern:** Cada contrato é um plugin independente e substituível
- **Factory Pattern:** `registry.py` instancia o engine correto por ID
- **Strategy Pattern:** Cada engine implementa a mesma interface com comportamentos distintos
- **PREVC:** Planning → Review → Execution → Validation → Confirmation (metodologia de documentação)
- **GSD:** Get-Shit-Done — velocidade de execução com qualidade pragmática

---

# 2. ESTRUTURA COMPLETA DE PASTAS

```
AutoRelatorio_V5/
│
├── backend/                            [Python + FastAPI — porta 5000]
│   ├── core/                           [Núcleo compartilhado por todos os contratos]
│   │   ├── server.py                  [FastAPI app + rotas principais]
│   │   ├── contract_engine.py         [Interface abstrata ContractEngine (ABC)]
│   │   ├── registry.py                [Registro centralizado dos 9 engines]
│   │   ├── word_utils.py              [Utilitários Word genéricos]
│   │   ├── word_utils_sp.py           [Utilitários Word modo SP]
│   │   ├── word_utils_sp2.py          [Utilitários Word modo SP2]
│   │   ├── utils_sp.py                [Formatações específicas SP]
│   │   └── utils_sp2.py               [Formatações específicas SP2]
│   │
│   ├── contracts/                      [1 pasta por contrato — módulos isolados]
│   │   ├── c0908/                     [São José dos Campos — SP]
│   │   │   ├── engine/
│   │   │   │   ├── engine.py          [Implementação ContractEngine]
│   │   │   │   ├── generator_0908.py  [Scanner — extrai conteúdo da pasta]
│   │   │   │   ├── scanner_0908.py    [Wrapper V5 do generator]
│   │   │   │   └── word_builder_0908.py [Wrapper V5 da geração DOCX]
│   │   │   ├── items/
│   │   │   │   └── items.json         [Banco de itens do contrato]
│   │   │   └── template/
│   │   │       └── MODELO-0908.docx   [Template Word com placeholders {{campo}}]
│   │   │
│   │   ├── c1507/                     [Cuiabá — MT — Tradicional]
│   │   ├── c1565/                     [SJRP/Ribeirão Preto — SP — SP2 EXCLUSIVO]
│   │   ├── c2056/                     [Divinópolis — MG — Tradicional]
│   │   ├── c2057/                     [Varginha — MG — Tradicional]
│   │   ├── c2626/                     [Salinas — MG — Tradicional]
│   │   ├── c2627/                     [Gov. Valadares — MG — Tradicional]
│   │   ├── c3575/                     [Tangará da Serra — MT — Tradicional]
│   │   └── c6122/                     [Mato Grosso do Sul — MS — Tradicional]
│   │       └── [mesma estrutura de c0908]
│   │
│   ├── output/                         [Pasta de saída — .docx gerados]
│   └── requirements.txt               [Dependências Python]
│
├── frontend/                           [Next.js 16 + React 19 + TypeScript — porta 3000]
│   ├── app/
│   │   ├── layout.tsx                 [Layout raiz — hydration guard + metadata]
│   │   ├── page.tsx                   [Orquestrador central da aplicação]
│   │   └── globals.css               [Estilos globais + Tailwind base]
│   │
│   ├── components/
│   │   ├── TopBar.tsx                 [Barra superior — contrato info + action buttons]
│   │   ├── Sidebar.tsx                [Menu lateral — seletor de contratos]
│   │   ├── EditorPanel.tsx            [Painel esquerdo — 3 passos de edição]
│   │   ├── PreviewPanel.tsx           [Painel direito — preview DOCX live]
│   │   ├── ResizableDivider.tsx       [Divisor redimensionável entre painéis]
│   │   ├── Toast.tsx                  [Sistema de notificações]
│   │   ├── blocks/
│   │   │   ├── BlockList.tsx          [Lista de fotos — drop zone + progress]
│   │   │   ├── BlockCard.tsx          [Card de foto — item dropdown + medidas]
│   │   │   └── MeasureForm.tsx        [Formulário dinâmico de medidas]
│   │   └── ui/
│   │       ├── EmptyState.tsx         [UI de estado vazio]
│   │       ├── ErrorMessage.tsx       [Exibição de erros]
│   │       └── LoadingSpinner.tsx     [Spinner de carregamento]
│   │
│   ├── hooks/
│   │   ├── useContracts.ts            [Wrapper do Zustand store]
│   │   ├── useSteps.ts                [Navegação entre os 3 passos]
│   │   ├── useFormData.ts             [State do formulário de cabeçalho]
│   │   ├── useBlocks.ts               [State central de blocos — cálculos + consolidação]
│   │   ├── useItems.ts                [Fetch de itens do backend]
│   │   ├── useApiState.ts             [State genérico para chamadas assíncronas]
│   │   └── useTheme.ts                [Dark/light mode com localStorage]
│   │
│   ├── lib/
│   │   ├── api.ts                     [Cliente HTTP — endpoints + error handling]
│   │   ├── contracts.ts               [Dados estáticos dos 9 contratos]
│   │   ├── descriptions.ts            [4 descrições predefinidas de serviço]
│   │   └── types.ts                   [Tipos TypeScript globais]
│   │
│   ├── store/
│   │   └── contractStore.ts           [Zustand store — contrato selecionado]
│   │
│   ├── data/                          [Dados estáticos adicionais]
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   └── .env.local                     [NEXT_PUBLIC_API_URL=http://localhost:5000]
│
├── .context/                           [DOCUMENTAÇÃO ARQUITETURAL (PREVC)]
│   ├── INDEX.md                       [Índice — leia primeiro]
│   ├── planning.md                    [Escopo, análise, riscos, roadmap]
│   ├── RESUMO_ANALISE.md              [Sumário executivo — padrão unificado]
│   ├── ARQUITETURA_FINAL_V5.md        [Blueprint completo — 4 fases, métricas]
│   ├── TABELA_VALORES_PADRAO.md       [Especificação parsers Excel — 2 tipos]
│   ├── INTEGRACAO_RELATORIO_PREVENTIVO.md [Fluxo JSON → skill memorial]
│   ├── BLOCOS_DINAMICOS.md            [UI/UX de blocos — interações]
│   └── FERRAMENTA_LEGENDAS_FOTOS.md   [Scripts de legendação]
│
├── .docs/                              [DOCUMENTAÇÃO TÉCNICA COMPLEMENTAR]
│   ├── wireframe_v5_overleaf.html     [Wireframe de inspiração — Overleaf style]
│   ├── reverse_engineering.md         [Engenharia reversa do V4]
│   ├── SCAFFOLD_TREE.md               [Árvore de scaffold inicial]
│   └── visaoDoApp_V5.md               [Visão de produto do V5]
│
├── .MD aleatorios/                    [Notas e logs de desenvolvimento]
│   ├── PROGRESS.md                    [Progresso por sprint]
│   ├── PENDENCIAS_V5.md               [Lista de pendências]
│   ├── PLANO_AJUSTES_CRITICOS.md      [Ajustes críticos identificados]
│   ├── VALIDACAO_FINAL_V5.md          [Checklist de validação final]
│   ├── TAREFA_NEXTJS_FRONTEND.md      [Tarefas de frontend]
│   ├── INSTRUCOES_MIGRACAO.md         [Instruções de migração do V4]
│   └── [outros ~10 arquivos de notas]
│
├── run.py                             [Launcher Python — start Next.js + open browser]
├── run.bat                            [Atalho Windows — executa run.py]
├── INICIAR.bat                        [Inicia backend + frontend em janelas separadas]
├── app.js                             [Wireframe/demonstração JavaScript (modo preview HTML)]
├── CLONE_REPORT.txt                   [Relatório de migração HTML → Next.js]
└── design_report.html                 [Validação visual de design — screenshots]
```

---

# 3. FUNCIONALIDADES IDENTIFICADAS

## 3.1 Funcionalidades Implementadas (✅)

### Geração de Relatório DOCX
- Preenche formulário com dados da OS (número, data, agência, endereço, responsável)
- Seleciona contrato bancário (9 contratos disponíveis)
- Clica "Gerar .docx" → backend substitui placeholders no template Word
- Download automático do arquivo gerado

### Interface 3-Passos
- **Step 1:** Cabeçalho (OS, agência, datas, endereço, responsável, tipo de descrição)
- **Step 2:** Blocos de fotos (seleção de pasta, associação de itens, preenchimento de medidas)
- **Step 3:** Pronto para gerar (preview final)

### Sistema de Blocos Dinâmicos
- Upload de pasta via `webkitdirectory` (sem upload real — lê FileList do browser)
- Cada foto vira um `Bloco` com: `id`, `arquivo`, `nome`, `pasta`, `numero`, `item?`, `medidas`, `total`
- Cálculo automático de área/volume/comprimento conforme unidade do item selecionado
- Consolidação automática: agrupa por pasta + item, soma totais

### Preview DOCX em Tempo Real
- Renderiza o relatório em HTML no painel direito
- Atualiza conforme o usuário preenche o formulário (flash animation)
- Zoom ajustável (40% a 150%)
- Header com logos (BB + MAFFENG), dados da OS, tabelas de itens

### Gestão de Contratos
- Sidebar lista os 9 contratos
- Seleção muda o engine ativo (SP2/SP/TRAD)
- TopBar mostra pill de modo (TRADICIONAL / SP / SP2)

### Dark Mode
- Toggle ☀️/🌙 na sidebar
- Persistido em localStorage
- Hydration guard em layout.tsx evita flicker SSR

### Suporte a 9 Contratos BB
- Cada contrato tem template próprio, banco de itens, lógica de scan e geração
- Modos: SP2 (c1565), SP (c0908), Tradicional (7 contratos)

## 3.2 Funcionalidades Em Desenvolvimento (⏳)

- Importador de Excel (parsers para planilhas SP2 e Tradicional)
- Processamento de imagens no backend (envio das fotos + inserção no DOCX)
- Cálculos avançados de memorial (faces, descontos, unidades especiais)
- Validação de legendas de fotos
- Geração de relatórios consolidados por contrato

## 3.3 Integrações Externas

| Integração | Status | Detalhe |
|-----------|--------|---------|
| Banco do Brasil (templates) | ✅ | Templates DOCX oficiais em cada `c{id}/template/` |
| python-docx | ✅ | Geração e substituição de placeholders |
| Pillow | ✅ (importado) | Processamento de imagens (uso pendente) |
| Skill `/relatorio-preventivo` | ⏳ | Integração via JSON → fluxo de memorial |

---

# 4. ANÁLISE TÉCNICA

## 4.1 Padrões Arquiteturais

### Plugin/Registry Pattern (Backend)
Cada contrato é um plugin independente registrado no `registry.py`:

```python
# core/registry.py
_ENGINES: dict[str, ContractEngine] = {
    "0908": Contract0908Engine(),
    "1565": Contract1565Engine(),
    # ... 9 contratos
}

def get_engine(contrato_id: str) -> ContractEngine:
    return _ENGINES[contrato_id]
```

### Abstract Engine (Interface)
Todos os contratos implementam a mesma interface:

```python
# core/contract_engine.py
class ContractEngine(ABC):
    contract_id: str
    contract_name: str
    template_file: str
    generation_mode: str  # "tradicional" | "sp" | "sp2"
    
    @abstractmethod
    def scan(self, root_path: str) -> list: ...
    
    @abstractmethod
    def build_word(self, modelo_path, conteudo, output_path, meta) -> str: ...
    
    @abstractmethod
    def get_items(self) -> dict: ...
    
    @abstractmethod
    def validate_folder(self, root_path: str) -> ValidationResult: ...
```

### Wrapper Compatibility Pattern
O V5 reutiliza código do V4 via sys.path injection:

```python
# contracts/c1565/scanner_1565.py
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from .generator_sp2 import build_content_sp2 as _build_content_sp2
```

### Custom Hooks State Management (Frontend)
Estado separado em camadas:

```
useContracts()    → contrato selecionado (Zustand)
useFormData()     → dados do formulário cabeçalho
useBlocks()       → blocos de fotos + cálculos + consolidação
useSteps()        → navegação entre os 3 passos
useItems()        → fetch de itens do backend
useApiState()     → estado genérico de chamadas async
useTheme()        → dark/light mode + localStorage
```

## 4.2 Organização do Código

**Separação de responsabilidades clara:**
- `core/` → compartilhado por todos
- `contracts/cXXXX/` → isolado por contrato
- `components/` → UI pura (presentational)
- `hooks/` → lógica de estado (stateful)
- `lib/` → utilitários sem estado (pure functions)
- `store/` → estado global (Zustand)

**Regra de negócio central:** `conteudo[]` é o único contrato de dados entre scanner e builder. O scanner produz um array, o builder consome esse mesmo array — independente do contrato.

## 4.3 Estratégias Técnicas Identificadas

### Hydration Guard (Next.js)
```typescript
// app/layout.tsx
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return null;
```
Evita SSR mismatch com localStorage (dark mode).

### Blob Download (DOCX)
```typescript
// lib/api.ts
const blob = await response.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = filename;
a.click();
URL.revokeObjectURL(url);
```
Download automático sem abrir nova aba.

### CORS Permissivo (Desenvolvimento)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```
Permite localhost:3000 → localhost:5000 sem bloqueio.

### webkitdirectory (Upload de Pasta)
```tsx
<input type="file" webkitdirectory directory multiple />
```
Permite selecionar uma pasta inteira (não faz upload real — retorna FileList no browser).

---

# 5. HISTÓRICO RECONSTRUÍDO

## 5.1 Sequência Provável de Desenvolvimento

**Fase 0 — V4 (baseline):** Sistema funcional com Tkinter ou app simples. Tinha `generator_sp2.py`, `word_builder_*.py`, `utils_sp2.py` que processavam fotos e geravam DOCX. Era provavelmente um script Python direto, sem frontend web.

**Fase 1 — Decisão de V5:** Escolha de migrar para web (Next.js + FastAPI) por usabilidade e escalabilidade. Criação do wireframe HTML (`app.js`, `wireframe_v5_overleaf.html`).

**Fase 2 — Scaffold do Backend:** Criação do `core/` (contract_engine.py, registry.py, server.py). Definição da interface abstrata. Reutilização dos generators/builders do V4 via wrapper pattern.

**Fase 3 — Portagem dos Contratos:** Criação das 9 pastas `contracts/cXXXX/`. Para cada contrato: engine.py + scanner wrapper + word_builder wrapper. Mantendo compatibilidade com V4.

**Fase 4 — Frontend Next.js:** Migração do wireframe HTML → React. Criação dos componentes (TopBar, Sidebar, EditorPanel, PreviewPanel). Implementação dos hooks. Integração com backend via `lib/api.ts`.

**Fase 5 — Sistema de Blocos:** Implementação do `useBlocks.ts` — lógica mais complexa do frontend. Criação de BlockList, BlockCard, MeasureForm. Cálculos de área/volume.

**Fase 6 — Documentação PREVC:** Criação dos 8 documentos em `.context/`. Planejamento formal das próximas fases (Excel, imagens, memoriais).

**Status atual (29/05/2026):** MVP funcional — gera DOCX com dados de cabeçalho. Blocos de fotos: UI pronta, lógica de cálculo implementada, mas envio das fotos ao backend ainda pendente.

## 5.2 Evidências de Evolução

- `CLONE_REPORT.txt` → registra a migração HTML → Next.js
- `INSTRUCOES_MIGRACAO.md` → instruções de migração do V4
- `ENGENHARIA_REVERSA_COMPLETA.md` → análise do V4 para base do V5
- Múltiplos `VALIDACAO_*.md` → sprints de validação iterativa
- `PROGRESS.md` → log de progresso por sprint
- `RELATORIO_EXECUCAO_SPRINTS.md` → histórico de execução

---

# 6. ARQUIVOS IMPORTANTES

## 6.1 Backend — Críticos

| Arquivo | Função | Importância |
|---------|--------|------------|
| `core/server.py` | FastAPI app + todos os endpoints | **CRÍTICO** — ponto de entrada do backend |
| `core/contract_engine.py` | Interface abstrata ABC | **CRÍTICO** — contrato de todos os engines |
| `core/registry.py` | Mapa de contratos → engines | **CRÍTICO** — factory central |
| `core/word_utils_sp2.py` | Utilitários Word para SP2 | **ALTO** — c1565 depende disso |
| `contracts/c1565/engine/engine.py` | Engine do contrato principal | **ALTO** — contrato mais complexo |
| `contracts/c1565/items/items.json` | 81 itens do contrato 1565 | **ALTO** — banco de dados de itens |
| `backend/requirements.txt` | Dependências Python | **ALTO** — reprodução do ambiente |

## 6.2 Frontend — Críticos

| Arquivo | Função | Importância |
|---------|--------|------------|
| `app/page.tsx` | Orquestrador da aplicação | **CRÍTICO** — tudo passa por aqui |
| `hooks/useBlocks.ts` | State + cálculos dos blocos | **CRÍTICO** — lógica mais complexa |
| `lib/api.ts` | Comunicação com backend | **CRÍTICO** — todas as chamadas HTTP |
| `store/contractStore.ts` | Estado global do contrato | **ALTO** — compartilhado por tudo |
| `lib/types.ts` | Interfaces TypeScript | **ALTO** — contrato de dados |
| `lib/contracts.ts` | Dados dos 9 contratos | **ALTO** — config estática |
| `frontend/package.json` | Dependências npm | **ALTO** — reprodução do ambiente |

## 6.3 Documentação — Referência

| Arquivo | Função | Quando Usar |
|---------|--------|------------|
| `.context/INDEX.md` | Índice de documentação | Antes de qualquer sessão |
| `.context/planning.md` | Escopo e riscos | Antes de mudanças de arquitetura |
| `.context/ARQUITETURA_FINAL_V5.md` | Blueprint completo | Para entender decisões |
| `.context/BLOCOS_DINAMICOS.md` | UI/UX de blocos | Para modificar BlockCard/BlockList |
| `.context/TABELA_VALORES_PADRAO.md` | Parsers Excel | Para implementar importação |

## 6.4 Scripts de Inicialização

| Arquivo | Função |
|---------|--------|
| `INICIAR.bat` | Inicia backend (porta 5000) + frontend (porta 3000) |
| `run.bat` | Inicia só o frontend via run.py |
| `run.py` | Launcher Python — `npm run dev` + abre browser |

---

# 7. DEPENDÊNCIAS

## 7.1 Backend (requirements.txt)

```
fastapi>=0.111.0        → Web framework ASGI — roteamento, validação, docs automáticas
uvicorn[standard]>=0.29.0 → ASGI server — hot reload, performance
python-docx>=1.1.0      → Manipulação de arquivos .docx — inserção de texto/imagens
Pillow>=10.0.0          → Processamento de imagens — resize, conversão (uso futuro)
pydantic>=2.0.0         → Validação de payloads HTTP + dataclasses com type safety
```

**Por que não Django/Flask?** FastAPI foi escolhido por: tipagem nativa, geração automática de docs `/docs`, performance async, Pydantic integrado.

## 7.2 Frontend (package.json)

```json
{
  "next": "16.1.6",           // Framework — App Router, SSR, build otimizado
  "react": "19.2.3",          // UI library — concurrent features, transitions
  "react-dom": "19.2.3",      // DOM renderer
  "zustand": "5.0.13",        // State management — simples, sem boilerplate
  "tailwindcss": "4.2.2",     // CSS utilitário — sem CSS files separados
  "@tailwindcss/postcss": "4",// PostCSS plugin para Tailwind 4
  "framer-motion": "12.34.4", // Animações declarativas (uso parcial)
  "fabric": "7.3.1"           // Canvas 2D (anotações em fotos — uso futuro)
}
```

**Por que Zustand e não Redux?** Minimalismo — menos boilerplate, API simples, sem actions/reducers.  
**Por que Tailwind 4?** Mais rápido que v3, menos configuração, PostCSS simples.

---

# 8. PROMPTS, AUTOMAÇÕES E IA

## 8.1 Metodologia PREVC (documentação em .context/)

O projeto segue a metodologia PREVC para cada feature/sprint:
- **P**lanning → Escopo, riscos, decisões técnicas
- **R**eview → Análise do estado atual
- **E**xecution → Implementação
- **V**alidation → Testes e verificação
- **C**onfirmation → Aprovação final

## 8.2 Integração com Skill /relatorio-preventivo

Documentada em `.context/INTEGRACAO_RELATORIO_PREVENTIVO.md`:
- O AutoRelatório V5 gera um JSON estruturado
- Esse JSON alimenta o skill `/relatorio-preventivo` da Caixa Econômica Federal
- Fluxo: V5 escaneia pasta → gera `conteudo[]` → serializa JSON → skill consome

## 8.3 Ferramenta de Legendas (scripts)

Documentada em `.context/FERRAMENTA_LEGENDAS_FOTOS.md`:
- Scripts Python prontos para legendação automática de fotos
- Verifica sequência numérica, consistência com tabelas, duplicatas

## 8.4 IA no Projeto

**Uso atual de IA:**
- Claude Code (este contexto) — desenvolvimento e documentação
- Anthropic SDK (planejado) — validação automática de legendas

**Skill integrados (TM Sempre Tecnologia):**
- `/relatorio-preventivo` — 4 etapas automáticas
- `/tm-testes` — E2E com Playwright
- `/turbo-checkpoint` — encerramento de sessão

---

# 9. MODELOS DE DADOS

## 9.1 Pydantic — Backend

```python
# Request de geração flat (endpoint principal)
class GenerateFlatRequest(BaseModel):
    contrato_id:   str
    nr_os:         str
    ag_cod:        str
    ag_nome:       str
    dt_atend:      str
    endereco:      Optional[str] = ""
    responsavel:   Optional[str] = ""
    desc_index:    Optional[str] = "1"
    modo:          Optional[str] = "sp2"
    root_path:     Optional[str] = ""

# Dataclasses do engine
@dataclass
class MetaField:
    key: str
    label: str
    type: str           # "text" | "date" | "select"
    required: bool = True
    auto_fill: bool = False
    example: str = ""
    options: list[str] = field(default_factory=list)

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
```

## 9.2 TypeScript — Frontend

```typescript
// Contrato
interface IContract {
  id: string;
  name: string;
  short: string;
  mode: 'sp2' | 'sp' | 'trad';
  uf: string;
}

// Formulário de cabeçalho
interface IFormData {
  nr_os: string;
  ag_cod: string;
  ag_nome: string;
  dt_atend: string;
  endereco: string;
  responsavel_dependencia: string;
  desc: '1' | '2' | '3' | '4';
}

// Bloco de foto
interface Bloco {
  id: string;
  arquivo: File;
  nome: string;
  previewUrl: string;
  pasta: string;
  numero: string;
  item?: ItemContrato;
  medidas: MedidasBloco;
  total: number;
}

// Item do contrato (banco de itens)
interface ItemContrato {
  codigo: string;
  descricao: string;
  unidade: 'm²' | 'm³' | 'm' | 'un' | 'kg' | 'l';
}

// Consolidado por pasta + item
interface BlocoConsolidado {
  pasta: string;
  item: ItemContrato;
  totalBlocos: number;
  totalMedida: number;
}
```

---

# 10. ENDPOINTS DA API

## 10.1 Backend FastAPI (localhost:5000)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check — retorna `{status: "ok"}` |
| POST | `/generate` | Geração flat — payload completo → FileResponse (.docx) |
| GET | `/api/contracts` | Lista os 9 contratos com metadados |
| GET | `/api/contracts/{id}` | Detalhes de um contrato específico |
| POST | `/api/contracts/{id}/scan` | Escaneia pasta do contrato |
| POST | `/api/contracts/{id}/generate` | Geração por contrato específico |
| GET | `/api/contracts/{id}/items` | Retorna banco de itens do contrato |

**Docs automáticas:** http://localhost:5000/docs (Swagger UI)

## 10.2 Frontend HTTP Client (lib/api.ts)

```typescript
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const checkHealth    = () => request<HealthResponse>('/health');
export const getContracts   = () => request<IContract[]>('/api/contracts');
export const getItems       = (id: string) => request<ItemsResponse>(`/api/contracts/${id}/items`);
export const generateReport = (payload: GeneratePayload) => requestFile('/generate', payload);
```

---

# 11. CONTRATOS SUPORTADOS

| ID | Localidade | UF | Modo | Itens | Obs |
|----|-----------|----|----|-------|-----|
| **0908** | São José dos Campos | SP | SP | items.json | |
| **1507** | Cuiabá | MT | TRAD | items.json | |
| **1565** | SJRP / Ribeirão Preto | SP | **SP2** | items.json (81 itens) | **EXCLUSIVO SP2 — nunca Tradicional** |
| **2056** | Divinópolis | MG | TRAD | items.json | |
| **2057** | Varginha | MG | TRAD | items.json | |
| **2626** | Salinas | MG | TRAD | items.json | |
| **2627** | Gov. Valadares | MG | TRAD | items.json | |
| **3575** | Tangará da Serra | MT | TRAD | items.json | |
| **6122** | Mato Grosso do Sul | MS | TRAD | items.json | |

---

# 12. REGRAS DE NEGÓCIO CRÍTICAS

| ID | Regra | Impacto se Violada |
|----|-------|-------------------|
| **RN-01** | Contrato 1565 = EXCLUSIVO SP2 — nunca Tradicional | Relatório incorreto, rejeição pelo BB |
| **RN-02** | Sort: "vista ampla" → numérico → alfabético → "detalhes" | Ordem errada nas fotos |
| **RN-03** | Altura padrão: 10cm (Trad/SP). 7cm = exclusivo SP2 (c1565) | Layout incorreto |
| **RN-04** | `conteudo[]` = único contrato de dados entre scanner e builder | Quebra de compatibilidade V4/V5 |
| **RN-05** | "Faces 2" no nome do arquivo = área × 2 (SP2) | Cálculo errado de área |
| **RN-06** | Placeholders: `{{nr_os}}`, `{{dt_atend}}`, `{{ag_cod}}`, `{{ag_nome}}`, `{{endereco}}`, `{{responsavel_dependencia}}`, `{{dt_elab}}`, `{{start_here}}` | Template não preenchido |
| **RN-07** | Arquitetura: 1 contrato = 1 módulo Python isolado | Acoplamento, difícil manutenção |
| **RN-08** | Nunca mudar core para acomodar contrato específico | Contamina todos os outros contratos |

---

# 13. FLUXO COMPLETO (WALKTHROUGH TÉCNICO)

```
1. INICIAR.bat → abre 2 janelas
   ├─ Backend: uvicorn core.server:app --port 5000 --reload
   └─ Frontend: npm run dev → http://localhost:3000

2. Usuário abre http://localhost:3000
   ├─ layout.tsx: hydration guard (mounted check)
   ├─ page.tsx: renderiza TopBar + Sidebar + EditorPanel + PreviewPanel
   └─ Sidebar: lista 9 contratos

3. Seleciona contrato (ex: "1565 - SJRP")
   ├─ contractStore.selectContract("1565")
   ├─ TopBar atualiza: nome + pill "SP2"
   ├─ useItems() faz GET /api/contracts/1565/items
   └─ BlockCard dropdowns populados com 81 itens

4. Passo 1 — Cabeçalho
   ├─ useFormData.updateField("nr_os", "1753")
   ├─ useFormData.updateField("ag_cod", "1234-5")
   ├─ [... mais campos]
   └─ PreviewPanel atualiza em tempo real (flash animation)

5. Passo 2 — Blocos de Fotos
   ├─ Clica "Selecionar Pasta" → input[webkitdirectory]
   ├─ FileList carregada → useBlocks.addFiles(files)
   ├─ Para cada arquivo:
   │   ├─ Cria Bloco {id, arquivo, nome, pasta, numero, previewUrl}
   │   └─ previewUrl = URL.createObjectURL(file)
   ├─ BlockCard renderizado para cada foto
   ├─ Usuário seleciona item no dropdown
   ├─ Usuário preenche medidas (largura, altura, etc.)
   ├─ calcularTotal() → m² = largura * altura (ou outra fórmula por unidade)
   └─ consolidar() → agrupa por [pasta][item] → soma totais

6. Passo 3 — Gerar
   ├─ Validação: nr_os ✓, ag_cod ✓, ag_nome ✓, dt_atend ✓
   ├─ handleGenerate() → lib/api.generateReport({...})
   ├─ POST http://localhost:5000/generate
   │   {
   │     contrato_id: "1565",
   │     nr_os: "1753",
   │     ag_cod: "1234-5",
   │     ag_nome: "Centro",
   │     dt_atend: "2026-05-21",
   │     endereco: "Rua X, 100",
   │     responsavel: "Mat. 12345 — João",
   │     desc_index: "1",
   │     modo: "sp2"
   │   }
   │
   └─ Backend processa:
       ├─ get_engine("1565") → Contract1565Engine
       ├─ meta = {nr_os, ag_cod, ag_nome, dt_atend, endereco, responsavel, dt_elab}
       ├─ conteudo = [] (sem root_path)
       ├─ tpl_path = "contracts/c1565/template/MODELO-1565.docx"
       ├─ engine.build_word(tpl_path, conteudo, output_path, meta)
       │   └─ Substitui {{nr_os}}, {{ag_cod}}, etc. no template
       └─ FileResponse("Relatorio-OS1753-1234-5.docx")

7. Frontend recebe blob DOCX
   ├─ URL.createObjectURL(blob)
   ├─ <a download> dispara download automático
   ├─ Toast: "✓ Relatório gerado com sucesso!"
   └─ Arquivo disponível na pasta Downloads/
```

---

# 14. MÉTRICAS DO PROJETO

## 14.1 Estimativa de Código

| Componente | Arquivos | LOC Estimado | Linguagem |
|-----------|----------|-------------|-----------|
| Backend — core/ | 8 | ~500 | Python |
| Backend — contratos/ | ~36 | ~2.000 | Python |
| Frontend — components/ | 12 | ~1.500 | TypeScript/React |
| Frontend — hooks/ | 7 | ~800 | TypeScript |
| Frontend — lib/ | 4 | ~250 | TypeScript |
| Documentação .context/ | 8 | ~8.000 | Markdown |
| **TOTAL** | **~75** | **~13.050** | |

## 14.2 Completude por Área

| Área | % Completo | Status |
|------|-----------|--------|
| Backend — estrutura e rotas | 90% | ✅ Sólido |
| Backend — parsers Excel | 0% | ❌ Não iniciado |
| Backend — processamento imagens | 20% | ⏳ Pillow importado |
| Frontend — UI/UX | 80% | ✅ Bom |
| Frontend — cálculos blocos | 70% | ⏳ Fórmulas básicas |
| Documentação PREVC | 95% | ✅ Excelente |
| Testes | 0% | ❌ Zero cobertura |
| Deploy/CI | 20% | ⏳ Scripts apenas |

---

# 15. ROADMAP E PRÓXIMAS ETAPAS

## Fase 1 — Importação Excel (Crítico)
1. Implementar `parseValoresExcel()` Python (2 tipos: SP2 + Tradicional)
2. Endpoint `POST /api/contracts/{id}/parse-excel`
3. UI: botão "Importar Planilha" no Step 2
4. Spec: `.context/TABELA_VALORES_PADRAO.md`

## Fase 2 — Fotos no DOCX
1. Envio real das fotos ao backend (multipart/form-data ou base64)
2. Inserção das imagens no template Word via python-docx
3. Redimensionamento Pillow (10cm × 14cm Trad/SP, 7cm × 10cm SP2)
4. Legendas automáticas por foto

## Fase 3 — Cálculos e Memoriais
1. Melhorar `calcularTotal()` — faces, descontos, unidades especiais
2. Gerar memorial de cálculo (PDF + DOCX)
3. Validação de legendas de fotos
4. Spec: `.context/BLOCOS_DINAMICOS.md`

## Fase 4 — QA e Deploy
1. Testes E2E com Playwright (`/tm-testes`)
2. Pytest para backend (contratos críticos)
3. Build otimizado (`next build`)
4. Deploy: Vercel (frontend) + Railway (backend)

---

# 16. COMO EXECUTAR

## Desenvolvimento Local

```bash
# Método 1: Script Windows (recomendado)
INICIAR.bat
# Abre 2 janelas CMD:
# - Backend: http://localhost:5000
# - Frontend: http://localhost:3000

# Método 2: Manual
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python -m uvicorn core.server:app --host 0.0.0.0 --port 5000 --reload

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

## URLs de Acesso

| URL | Descrição |
|-----|-----------|
| http://localhost:3000 | App principal |
| http://localhost:5000/docs | Swagger UI — documentação da API |
| http://localhost:5000/health | Health check do backend |

---

# 17. PONTOS FORTES E RISCOS

## Pontos Fortes

1. **Arquitetura escalável:** Adicionar novo contrato = copiar pasta `cXXXX/`, ajustar `engine.py`, registrar no `registry.py` — sem tocar no core
2. **Compatibilidade V4:** Wrappers inteligentes reutilizam código legado sem duplicação
3. **Documentação excelente:** 8 documentos PREVC cobrem todas as decisões técnicas
4. **Type safety em ambas as camadas:** TypeScript + Pydantic
5. **UI moderna:** Dark mode, preview live, drag-and-drop ready
6. **Isolamento de contratos:** Falha em c1565 não afeta c2056

## Riscos Identificados

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Parsers Excel não implementados | **ALTO** | Fase 1 prioritária |
| Zero testes | **ALTO** | Fase 4 obrigatória |
| Fotos não chegam ao backend | **ALTO** | Fase 2 crítica |
| Performance com 500+ fotos | **MÉDIO** | Virtualização da lista |
| sys.path injection (wrappers) | **BAIXO** | Funciona, mas é técnica improvisada |
| CORS permissivo em produção | **BAIXO** | Restringir allow_origins antes do deploy |

---

*Documento gerado por análise forense automatizada — Claude Code (claude-sonnet-4-6)*  
*Baseado na análise completa do workspace em 29/05/2026*  
*Para retomar o projeto: leia este arquivo + `.context/INDEX.md` + abra `INICIAR.bat`*
