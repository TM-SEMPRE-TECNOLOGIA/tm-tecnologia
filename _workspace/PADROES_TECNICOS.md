# ⚙️ PADRÕES TÉCNICOS — TM Sempre Tecnologia
**Referência de padrões, convenções e regras de implementação**
**Atualizado em:** 2026-05-27

---

## 1. PADRÕES PYTHON (Backend AutoRelatório V5)

### 1.1 Cabeçalho Obrigatório em Todo Script

```python
"""
OBJETIVO: [O que este script faz em 1 linha]
ENTRADA:  [Tipo e descrição dos inputs]
SAÍDA:    [Tipo e descrição dos outputs]
DEPENDÊNCIAS: [Lista de imports externos]
RISCOS:   [Comportamentos inesperados conhecidos]
IMPACTO:  [O que quebra se este script falhar]
AUTOR:    TM Sempre Tecnologia
CRIADO:   YYYY-MM-DD
"""
```

### 1.2 Interface ContractEngine (ABC)

Todo novo contrato DEVE implementar:

```python
from abc import ABC, abstractmethod

class ContractEngine(ABC):
    @abstractmethod
    def scan(self, root_path: str) -> list:
        """Retorna conteudo[] a partir da pasta de fotos"""
        pass

    @abstractmethod
    def build_word(self, conteudo: list, meta: dict) -> bytes:
        """Gera .docx a partir de conteudo[] e metadados"""
        pass

    @abstractmethod
    def get_items(self) -> list:
        """Retorna lista de itens do items.json"""
        pass

    @abstractmethod
    def get_meta_fields(self) -> list:
        """Retorna lista de campos de metadados necessários"""
        pass

    @abstractmethod
    def validate_folder(self, root_path: str) -> dict:
        """Valida estrutura da pasta de fotos"""
        pass
```

### 1.3 Estrutura conteudo[] — Tipos Válidos

```python
# TIPO 1: Título de seção (str com prefixo »)
"» Nome da Seção"

# TIPO 2: Foto normal
{"imagem": "/caminho/absoluto/foto.jpg"}

# TIPO 3: Quebra de página
{"quebra_pagina": True}

# TIPO 4: Tabela SP — Memória de Cálculo (c0908)
{"memoria_calculo": {
    "item_cod": "17.01",
    "descricao": "Pintura automotiva",
    "largura": 10.0,
    "altura": 1.2,
    "faces": 1,
    "desconto": 5.6,
    "total": 6.4
}}

# TIPO 5: Tabela SP2 (c1565)
{"tabela_itens_sp2": {...}}

# TIPO 6: Croqui SP2
{"croqui": "/caminho/croqui.jpg", "legenda": "Vista frontal"}

# TIPO 7: Enunciado de item SP2
{"enunciado_item": {"codigo": "...", "descricao": "..."}}
```

### 1.4 Sort de Fotos (RN-02 — NUNCA ALTERAR)

```python
def sort_key(nome_pasta: str) -> tuple:
    """
    Ordem: Vista ampla → Numérico → Alfabético → Detalhes
    """
    nome_lower = nome_pasta.lower().strip()
    if "vista ampla" in nome_lower:
        return (0, 0, nome_lower)
    if nome_lower == "- detalhes" or nome_lower == "detalhes":
        return (3, 0, nome_lower)
    # Tenta extrair número inicial
    match = re.match(r'^-?\s*(\d+)', nome_lower)
    if match:
        return (1, int(match.group(1)), nome_lower)
    return (2, 0, nome_lower)
```

### 1.5 Imagens no Word

```python
# Altura padrão por modo (RN-03):
ALTURA_PADRAO_CM = 10.0  # Tradicional (c1507,2056,2057,2626,2627,3575,6122) e SP (c0908)
ALTURA_PADRAO_SP2_CM = 7.0  # SP2 — exclusivo do contrato c1565

# Portrait = 2 colunas
# Landscape = linha inteira (ocupa coluna dupla)
```

---

## 2. PADRÕES TYPESCRIPT/NEXT.JS (Frontend)

### 2.1 Store Zustand por Contrato

```typescript
// ✅ CORRETO — store isolado por contrato
const useContractStore = (contractId: string) => useAppStore(
  (state) => state.contracts[contractId]
)

// ❌ ERRADO — estado global misturado
const { currentContract, allData } = useAppStore()
```

### 2.2 Chamadas de API

```typescript
// lib/api.ts — padrão de uso
import { checkHealth, generateReport, requestFile } from '@/lib/api'

// Sempre usar try/catch com feedback ao usuário
try {
  const blob = await generateReport(contractId, formData)
  // processar blob
} catch (err) {
  console.error('[generateReport]', err)
  toast.error('Erro ao gerar relatório')
}
```

### 2.3 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/contracts` | Lista todos os contratos |
| GET | `/api/contracts/{id}/items` | Itens do contrato |
| POST | `/api/contracts/{id}/scan` | Escaneia pasta de fotos |
| POST | `/api/contracts/{id}/generate` | Gera .docx |
| POST | `/api/contracts/{id}/generate-with-files` | Upload + gera .docx (**Sprint 3**) |
| POST | `/api/contracts/{id}/validate` | Valida estrutura da pasta |

---

## 3. PADRÕES DE DOCUMENTAÇÃO

### 3.1 Spec de Automação (template obrigatório)

```markdown
# SPEC: [Nome da Automação]
**Data:** YYYY-MM-DD
**Versão:** 1.0.0
**Status:** Proposta | Em Desenvolvimento | Aprovada | Depreciada

## Objetivo
[O que esta automação faz]

## Entrada
- Tipo: [arquivo | pasta | API | manual]
- Formato: [xlsx | docx | json | ...]
- Exemplo: `./fixtures/exemplo_entrada/`

## Saída
- Tipo: [arquivo | relatório | API response]
- Formato: [docx | xlsx | json | log]
- Exemplo: `./fixtures/exemplo_saida/`

## Dependências
- Python: [lista de pip packages]
- Arquivos: [lista de arquivos necessários]
- APIs: [endpoints utilizados]

## Riscos
- [Risco 1]: [Como mitigar]
- [Risco 2]: [Como mitigar]

## Como Executar
```bash
python scripts/python/nome_script.py --input ./entrada --output ./saida
```

## Impacto Arquitetural
[O que muda no sistema se esta automação for integrada]

## Histórico
| Data | Versão | Mudança |
|------|--------|---------|
| YYYY-MM-DD | 1.0.0 | Criação |
```

### 3.2 Registro de Descoberta

```markdown
# DESCOBERTA: [Título]
**Data:** YYYY-MM-DD
**Contexto:** [Qual tarefa gerou esta descoberta]
**Impacto:** Alto | Médio | Baixo

## O Que Foi Encontrado
[Descrição técnica]

## Por Que Importa
[Implicações para o projeto]

## Como Aplicar
[Passo a passo de uso]

## Referências
- Arquivo: `caminho/do/arquivo.py:linha`
- Spec: `docs/specs/nome-spec.md`
```

---

## 4. PADRÕES DE TESTE

### 4.1 Estrutura de Fixture

```
testes/fixtures/
├── fixture_c0908_basico/        ← pasta de fotos mínima para teste
│   ├── - Área externa/
│   │   └── 1 - Pintura automotiva/
│   │       └── foto.jpg
│   └── - Área interna/
│       └── 1 - SAA (sala de autoatendimento)/
│           └── foto.jpg
└── fixture_c1565_sp2/           ← fixture SP2
    ├── Santa Adélia/
    └── croqui.jpg
```

### 4.2 Nomenclatura de Testes

```python
# Python pytest
def test_scan_c0908_retorna_conteudo_valido():
    """Test que o scanner do c0908 retorna conteudo[] com estrutura correta"""
    pass

def test_sort_vista_ampla_primeiro():
    """Test que 'vista ampla' sempre aparece antes de itens numerados"""
    pass
```

---

## 5. PADRÕES DE PLACEHOLDERS WORD

```
Placeholders válidos no template .docx:
{{nr_os}}                  → Número da OS
{{dt_atend}}               → Data de atendimento (DD/MM/YYYY)
{{ag_cod}}                 → Código da agência
{{ag_nome}}                → Nome da agência
{{endereco}}               → Endereço completo
{{responsavel_dependencia}} → Nome do responsável
{{dt_elab}}                → Data de elaboração (auto = hoje)
{{start_here}}             → Marcador de inserção (onde o conteúdo começa)
```

---

## 6. REGRAS DE INTEGRAÇÃO COM SKILLS

### 6.1 Quando Usar Cada Skill

| Situação | Skill a Usar |
|----------|-------------|
| Criar nova feature | `/brainstorming` |
| Relatório preventivo manual | `relatorio-preventivo` |
| Completar .docx pré-finalizado SP2 | `tm-automatizando` |
| Testar app com Playwright | `tm-testes` |
| Manipular DOCX programaticamente | `docx-manipulation` |
| Debug sistemático | `systematic-debugging` (antigravity) |

### 6.2 Localização das Skills

```
C:\Users\thiag\Desktop\TM-MEUS-APPS\Meus Plugins e Skills\
├── relatorio-preventivo.skill      → Skill principal de relatórios
├── relatorio-preventivo-v2.skill   → Versão 2
├── tm-automatizando\               → Skill de auto-completar SP2
├── tm-testes\                      → Playwright E2E
├── tm-design-system-plugin\        → Design system
└── antigravity-awesome-skills\     → Skills base (brainstorming, etc.)
    └── skills/
        ├── brainstorming/
        ├── systematic-debugging/
        ├── subagent-driven-development/
        └── dispatching-parallel-agents/
```

---

*Regras técnicas que não constam aqui devem ser adicionadas após validação. Ver: `FLUXO_DE_TRABALHO.md` §5.*
