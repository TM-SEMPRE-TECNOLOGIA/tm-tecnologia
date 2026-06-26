# AutoRelatório V5 — PLANNING (PREVC)

**Data:** 2026-05-22  
**Analista:** Claude Code (PREVC - AI Coders Academy)  
**Status:** Planejamento Executivo

---

## 1. ESCOPO & REQUISITOS

### 1.1 Objetivo
Criar interface frontend (HTML5 + JS) para gerar relatórios fotográficos preventivos automaticamente,
substituindo fluxo manual de edição em Word/Excel.

### 1.2 Contratos em Escopo
- **1565** (São Paulo / Rio Preto): Modo SP2 ✓ (RAT estruturado)
- **0908** (São Paulo): Modo SP (Tradicional)
- **2056** (Divinópolis): Modo Tradicional
- **2057** (Varginha): Modo Tradicional
- **6122** (Mato Grosso do Sul): Modo Tradicional
- **2626** (Salinas): Modo Tradicional
- **2627** (Valadares): Modo Tradicional
- **3575** (Tangará da Serra): Modo Tradicional
- **1507** (Cuiabá): Modo Tradicional

**Total: 9 contratos | 2 modos: SP2, Tradicional**

### 1.3 Modos de Operação

| Modo | Contrato | Modelo | Estrutura | Status |
|------|----------|--------|-----------|--------|
| **SP2** | 1565 | RAT (Modelo padronizado) | Planilha estruturada | ✓ Pronto |
| **Tradicional** | 0908, 2056, 2057, 6122, 2626, 2627, 3575, 1507 | Memorial do Thiago | Planilha manual | ⚠ Análise necessária |

---

## 2. ANÁLISE TÉCNICA DOS ARTEFATOS

### 2.1 Estrutura de Relatórios (DOCX)
Todos os 9 relatórios seguem padrão similar:
- **Componentes fixos:**
  - Cabeçalho com logo BB + logo MAFFENG
  - Tabela de dados da OS
  - Tabela "Dados da Dependência"
  - Descrição do serviço
  - Blocos de conteúdo (fotos, croquis, memoriais)
  - Rodapé com numeração de página

- **Variação:** Contrato 1565 tem RAT estruturado; outros têm estrutura livre

### 2.2 Planilhas de Memorial

#### SP 1565 (RAT - Modelo Estruturado)
```
Abas: RAT | Conformidade | Valores Unitários | Prefixos | BDI
Estrutura:
  - RAT: 17 colunas × 68 linhas (dados do atendimento)
  - Valores Unitários: 39 colunas × 550 linhas (tabela de itens)
Características:
  - Altamente estruturada
  - Referências cruzadas (VLOOKUP)
  - Pronta para extração automatizada
```

#### Apoio Thiago (Memorial Manual)
```
Abas: Esmalte em porta | Planilha cálculo UNIDADE | Planilha cálculo MEDIDAS | itens | Valores
Estrutura:
  - Planilha cálculo MEDIDAS: 6 colunas × 80 linhas (REFERÊNCIA, LARGURA, ALTURA, etc)
  - itens: Tabela de códigos de itens (39 colunas)
Características:
  - Menos estruturada
  - Preenchimento manual de fotos e dimensões
  - Requer parsing inteligente
```

### 2.3 Análise de Fidelidade: Wireframe V5 vs Realidade

#### ✓ FIDELIDADE ALTA (70-85%)
- **Cabeçalho de dados:** wireframe captura estrutura correta (OS, agência, data)
- **Tabelas de itens:** estrutura de 4 colunas (código, descrição, qtd, unidade) está correta
- **Blocos visuais:** padrão de título/subtítulo/fotos/memorial é válido

#### ⚠ GAPS IDENTIFICADOS (15-30%)

| Gap | Impacto | Prioridade | Ação |
|-----|---------|-----------|------|
| **1. Modo Tradicional não está modelado** | 8 contratos sem suporte | ALTA | Criar parser para planilha Thiago |
| **2. RAT (1565) é mais complexo** | Campos específicos do BB | ALTA | Adicionar campos SP2 ao form |
| **3. Memoriais não têm interface** | Dados não são extraídos | ALTA | Implementar importador de Excel |
| **4. Croquis não têm preview** | Falta validação visual | MÉDIA | Adicionar preview de imagens |
| **5. Validações de unidade de medida** | Pode haver inconsistências | MÉDIA | Implementar validação de unidades |
| **6. Referências de fotos** | Sequência pode variar | BAIXA | Permitir renumeração manual |

---

## 3. DECISÕES ARQUITETURAIS (DEFINIÇÕES PREVC)

### 3.1 Frontend (HTML5 + Vanilla JS)
**Decisão:** Manter abordagem SPA (Single Page Application) sem framework externo.
- ✓ Wireframe V5 já implementa estrutura correta
- ✓ Redimensionador de painéis adicionado (flexibilidade)
- ⚠ Precisa: parser de Excel, validação de fotos, importador de planilhas

### 3.2 Estrutura de Dados (JS)
```javascript
// Objeto global de contrato
const relatorio = {
  contrato: "1565",
  modo: "SP2",  // "SP2" ou "Tradicional"
  cabecalho: {
    nr_os, dt_atend, ag_cod, ag_nome, endereco, responsavel, descricao
  },
  blocos: [
    {
      tipo: "titulo",     // titulo|subtitulo|imagem|croqui|tabela_calc|tabela_itens
      conteudo: "...",
      metadados: {}
    }
  ],
  memoriais: {
    tabelas_calc: [],    // Dados extraídos da planilha
    itens: []            // Tabela final de itens
  }
}
```

### 3.3 Importação de Dados (Excel)
**Decisão:** Suportar dois fluxos:
1. **SP2 (1565):** Parser estruturado da aba "Valores Unitários" do RAT
2. **Tradicional (outros):** Parser flexível da planilha Thiago (MEDIDAS + UNIDADE)

Biblioteca: `xlsx` (JavaScript) — lightweight, sem dependências

### 3.4 Template DOCX
**Decisão:** Usar `python-docx` (backend) para geração, não `docxgen` (JS).
- ✓ Mais controle sobre formatação
- ✓ Suporta imagens, tabelas complexas, estilos
- ✗ Requer servidor Python (escopo futuro v1.1)
- **Para V5 MVP:** Manter preview HTML apenas

---

## 4. ROADMAP TÉCNICO (Próximas Fases)

### FASE 1: MVP Validação (Atual) — PREVC Planning + Review
- [x] Wireframe V5 com redimensionador
- [ ] **Parser Excel (SP2)** — extrair "Valores Unitários" do RAT 1565
- [ ] **Parser Excel (Tradicional)** — extrair planilha Thiago
- [ ] **Validação de fotos** — confirmar sequência, dimensões
- [ ] **Preview DOCX melhorado** — refletir estrutura real

### FASE 2: Geração de DOCX (v1.1)
- [ ] Backend Python com `python-docx`
- [ ] Endpoint `/generate` — recebe estrutura JS, gera DOCX
- [ ] Suporte a imagens, tabelas, estilos conforme modelo real

### FASE 3: Sincronização Multi-Contrato
- [ ] Salvar templates por contrato
- [ ] Versionamento de estruturas
- [ ] Histórico de relatórios gerados

---

## 5. RISCOS & MITIGAÇÃO

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|--------|-----------|
| Estrutura planilhas variar entre contratos | ALTA | MÉDIO | Criar parsers genéricos, testar 3 modelos |
| Imagens com caminhos quebrados | MÉDIA | MÉDIO | Validar existência de arquivos local/rede |
| Referências de foto fora de ordem | MÉDIA | BAIXO | Permitir renumeração no editor |
| Performance com muitas imagens | BAIXA | ALTO | Limpar cache, lazy-load preview |

---

## 6. CRITÉRIOS DE ACEITAÇÃO (Definition of Done)

### V5 MVP Completo
- [ ] Editor de cabeçalho + forma de estrutura com redimensionador ✓
- [ ] Importador Excel (SP2 + Tradicional)
- [ ] Parser validado em 3+ relatórios reais
- [ ] Preview DOCX reflete 85%+ da estrutura real
- [ ] Fidelidade comprovada em teste com documento base

### Entrega de Qualidade
- [ ] Testes manuais com contratos 1565, 0908, 2056
- [ ] Documentação técnica (PREVC Review)
- [ ] Registro em `diario_de_dev.md`

---

## 7. MÉTRICAS & KPIs

| Métrica | Target | Atual | Status |
|---------|--------|-------|--------|
| Cobertura de contratos | 9/9 (100%) | 1/9 (SP2 pronto) | ⏳ Em progresso |
| Fidelidade vs modelo real | 85%+ | 70% (gaps identificados) | ⏳ Melhorando |
| Tempo geração relatório | <10s | TBD | ⏳ A medir |
| Taxa de sucesso parsers Excel | 95%+ | TBD | ⏳ A testar |

---

**Próxima etapa:** PREVC Review → Validação técnica dos parsers Excel

---

## 8. REFERÊNCIAS

- **Padrão de Tabela de Valores:** `.context/TABELA_VALORES_PADRAO.md` — Especificação completa de importação Excel
- **Scripts de análise:** `AutoRelatorio_V5/analise_*.py` — Parsers experimentais

