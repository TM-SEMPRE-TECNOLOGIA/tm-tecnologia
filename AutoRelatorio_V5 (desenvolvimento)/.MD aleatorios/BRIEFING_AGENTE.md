# Briefing para Agente "Add collapse arrow..." — AutoRelatório V5

**Data:** 2026-05-23  
**Status:** Aguardando início de desenvolvimento  
**Sincronização:** Chat paralelo com Claude Code

---

## 🎯 OBJETIVO

Implementar o **AutoRelatório V5** — plataforma de 3 passos para gerar relatórios fotográficos preventivos automaticamente.

---

## 📍 LOCALIZAÇÃO DO PROJETO

```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
├── .context/ .......................... DOCUMENTAÇÃO ARQUITETURAL
│   ├── INDEX.md ....................... Guia de navegação
│   ├── planning.md .................... Escopo + decisões + roadmap
│   ├── TABELA_VALORES_PADRAO.md ....... Parsers Excel (2 tipos)
│   ├── INTEGRACAO_RELATORIO_PREVENTIVO.md ... JSON + skill
│   ├── ARQUITETURA_FINAL_V5.md ........ Blueprint 360°
│   └── BLOCOS_DINAMICOS.md ............ UI/UX: seleção dinâmica
│
├── .docs/
│   └── wireframe_v5_overleaf(inspiração).html  FRONTEND ATUAL
│
└── scripts/ ........................... (A CRIAR) Scripts auxiliares
```

---

## 🏗️ ARQUITETURA (Resumo Executivo)

### 3 Passos do App

```
Passo 1: Cabeçalho (OS, agência, endereço)
         ↓
Passo 2: Estrutura (importar Excel + blocos dinâmicos)
         ↓
Passo 3: Gerar (JSON → skill /relatorio-preventivo → DOCX)
```

### Tecnologia
- **Frontend:** HTML5 + Vanilla JavaScript (sem frameworks)
- **Importação Excel:** `SheetJS` (xlsx library)
- **Backend:** Python (skill `/relatorio-preventivo`)
- **Saída:** Word (.docx) formatado

---

## 🔧 TAREFAS EM ORDEM DE PRIORIDADE

### FASE 1: UI Dinâmica (Passo 2) — **PRIORIDADE ALTA**

**Requisito do usuário:** Quando seleciona uma foto, aparece:
1. Dropdown com itens disponíveis (do Excel importado)
2. Formulário **adaptativo** conforme unidade:
   - `un` (unidades) → Campo: QUANTIDADE
   - `m²` (área) → Campos: LARGURA × ALTURA × DESCONTO
   - `m³` (volume) → Campos: COMP × ALTURA × PROF
   - `m` (linear) → Campo: COMPRIMENTO
3. **Cálculo automático** do total
4. **Tabela renderizada** no preview DOCX

**Documentação:** `BLOCOS_DINAMICOS.md`

**Arquivo a editar:** `.docs/wireframe_v5_overleaf(inspiração).html`

---

### FASE 2: Parser de Excel — **PRIORIDADE ALTA**

**O que fazer:** Implementar função JavaScript que lê `.xlsx` e extrai:

**Tipo SP2 (1565, 0908):**
- Aba: "Valores Unitários" ou "Valores"
- Estrutura: Código | Descrição | Quantidade | Unidade | Valores

**Tipo Tradicional (outros 7 contratos):**
- Aba 1: "Planilha de cálculo MEDIDAS" (REFERÊNCIA | LARGURA | ALTURA | TOTAL)
- Aba 2: "Planilha de cálculo UNIDADE" (REFERÊNCIA | QUANTIDADE)

**Documentação:** `TABELA_VALORES_PADRAO.md`

**Biblioteca:** `SheetJS` (https://sheetjs.com/) — adicionar ao HTML

---

### FASE 3: Gerador de JSON — **PRIORIDADE MÉDIA**

**O que fazer:** No passo 3 (Gerar), criar função que consolida:
- Dados do formulário (cabeçalho)
- Blocos dinâmicos (fotos + itens + medidas)
- Memoriais (estrutura conforme contrato)

**Saída:** `relatorio.json` (estrutura em `INTEGRACAO_RELATORIO_PREVENTIVO.md`)

---

### FASE 4: Invocar Skill — **PRIORIDADE MÉDIA**

**O que fazer:** Enviar JSON para skill `/relatorio-preventivo`

**Resultado:** DOCX final pronto para download

**Documentação:** `INTEGRACAO_RELATORIO_PREVENTIVO.md`

---

## 📚 DOCUMENTAÇÃO TÉCNICA

### Para entender tudo:
1. Comece com: `INDEX.md` (mapa de navegação)
2. Depois: `planning.md` (escopo + decisões)
3. Específico para sua tarefa: `BLOCOS_DINAMICOS.md` (UI)

### Para implementação:
- **Parser:** `TABELA_VALORES_PADRAO.md` (estrutura dados + pseudo-código)
- **JSON:** `INTEGRACAO_RELATORIO_PREVENTIVO.md` (formato esperado)
- **UI:** `BLOCOS_DINAMICOS.md` (fluxo + validações)

---

## 🗂️ ESTADO ATUAL DO CÓDIGO

### Frontend (HTML)
```
wireframe_v5_overleaf(inspiração).html
✅ Layout básico 3 passos
✅ Editor de cabeçalho (passo 1)
✅ Redimensionador de painéis
✅ Preview DOCX em tempo real
⏳ FALTAM:
   • Importador de Excel (passo 2)
   • Blocos dinâmicos (passo 2)
   • Gerador de JSON (passo 3)
```

### Contrato Padrão
```
Contrato 1565 (São Paulo / Rio Preto)
Modo: SP2
Tipo Memorial: SP
Status: Referência (use para testes)
```

---

## 🔄 FLUXO DE SINCRONIZAÇÃO

```
[Claude Code]                    [Agente "Add collapse arrow..."]
(Arquitetura + Spec)    ←→     (Implementação)

1. Claude Code cria briefing (este arquivo)
2. Agente lê documentação
3. Agente edita HTML/JS
4. Agente atualiza progresso em PROGRESS.md
5. Claude Code revisa + integra com skill
```

---

## 📝 COMO REPORTAR PROGRESSO

Atualize este arquivo conforme avança:

```markdown
## ✅ CONCLUÍDO
- [x] Tarefa 1
- [x] Tarefa 2

## ⏳ EM ANDAMENTO
- [ ] Tarefa 3 — 60% pronto

## ❌ BLOQUEADO
- [ ] Tarefa 4 — Aguardando X
```

Crie arquivo: `PROGRESS.md` na raiz do projeto

---

## 🎬 COMEÇAR AGORA

### Passo 1: Leitura (10 min)
1. Leia `INDEX.md` (mapa de navegação)
2. Leia `planning.md` seção "Escopo"
3. Leia `BLOCOS_DINAMICOS.md` completo

### Passo 2: Setup (5 min)
1. Abra `.docs/wireframe_v5_overleaf(inspiração).html` no editor
2. Instale `SheetJS` via CDN (link no HTML `<head>`)
3. Crie arquivo `scripts/` se precisar de helpers

### Passo 3: Codificar
1. **Primeiro:** Implementar seletor de itens (UI)
2. **Depois:** Parser de Excel
3. **Depois:** Formulários dinâmicos
4. **Depois:** Gerador JSON

---

## 🚨 PONTOS CRÍTICOS

⚠️ **Sem frameworks** — Use Vanilla JS apenas  
⚠️ **Compatibilidade** — Suportar todos os 9 contratos  
⚠️ **Sincronização** — Converse com Claude Code antes de mudanças maiores  
⚠️ **Testes** — Use contrato 1565 como referência (SP2)  
⚠️ **Limpeza** — Scripts auxiliares em `scripts/`, não na raiz  

---

## 📞 CONTATO / DÚVIDAS

Qualquer dúvida:
1. Verifique a documentação em `.context/`
2. Converse com Claude Code (chat paralelo)
3. Atualize `PROGRESS.md` com bloqueios

---

## 📊 MÉTRICAS DE SUCESSO

| Fase | Meta | Critério |
|------|------|----------|
| UI Dinâmica | 100% | Todos os 4 tipos de formulário funcionando |
| Parser Excel | 100% | Lê SP2 + Tradicional, 9 contratos |
| JSON Generator | 100% | Estrutura conforme spec |
| Integração Skill | 100% | DOCX gerado com formatação correta |

---

**Status:** Pronto para começar 🚀  
**Última atualização:** 2026-05-23  
**Próximo checkpoint:** Após implementar Parser Excel

