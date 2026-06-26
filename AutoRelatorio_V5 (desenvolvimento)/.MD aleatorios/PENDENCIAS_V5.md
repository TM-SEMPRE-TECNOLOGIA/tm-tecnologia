# AutoRelatório V5 — Pendências e Acompanhamento
**Abra este arquivo sempre que retomar o projeto.**
Última atualização: 2026-05-21

---

## Status Geral

| Fase | Status |
|------|--------|
| PRD MVP | ✅ Concluído |
| Scaffold de pastas | ✅ Concluído |
| Wireframe Blocos (visual por tipo) | ✅ Concluído |
| Wireframe Overleaf (3 painéis, live preview) | ✅ Concluído |
| Core: ContractEngine ABC | ✅ Criado |
| Migração dos motores | 🔴 Aguardando materiais |
| Templates Word | 🔴 Aguardando materiais |
| Frontend V5 | 🔴 Não iniciado |
| Testes | 🔴 Não iniciado |

---

## Materiais que Thiago precisa enviar

Para cada um dos 9 contratos, são necessários **3 itens**:

| # | Contrato | Planilha de Itens | Planilha Padrão | Exemplo de Relatório Pronto |
|---|----------|:-----------------:|:---------------:|:---------------------------:|
| 1 | **0908** — São José dos Campos | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 2 | **1507** — Cuiabá | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 3 | **1565** — São José do Rio Preto / Ribeirão Preto | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 4 | **2056** — Divinópolis | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 5 | **2057** — Varginha | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 6 | **2626** — Salinas | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 7 | **2627** — Governador Valadares | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 8 | **3575** — Tangará da Serra | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |
| 9 | **6122** — Mato Grosso do Sul | 🔴 Pendente | 🔴 Pendente | 🔴 Pendente |

> **Como enviar:** Pode mandar um contrato de cada vez. Assim que receber, já começo a mapear os itens e migrar o motor daquele contrato.

---

## O que cada material vai alimentar no V5

**Planilha de Itens** (ex: planilha Excel com códigos, descrições, unidades)
→ Vira o `items/items.json` de cada contrato
→ Alimenta o painel de associação de itens na interface
→ Garante que a memória de cálculo use os códigos certos

**Planilha Padrão** (template de planilha que acompanha o relatório)
→ Define o formato de saída da memória de cálculo
→ Serve de referência para o motor de Word gerar tabelas corretas

**Exemplo de Relatório Pronto** (.docx real de uma OS já finalizada)
→ É o espelho do que o V5 precisa reproduzir
→ Revela formatação, placeholders, ordem de seções e estilo de foto
→ Base para os testes de regressão ("o V5 gera igual ao exemplo?")

---

## Próximos Passos (após receber materiais)

1. **Por contrato recebido:**
   - Extrair itens da planilha → `contracts/cXXXX/items/items.json`
   - Analisar relatório de exemplo → documentar regras de formatação
   - Migrar scanner + word_builder do V4 para o módulo isolado
   - Criar testes comparando output V5 vs relatório de exemplo

2. **Quando todos os 9 contratos estiverem com materiais:**
   - Fechar o `ContractRegistry` com os 9 engines registrados
   - Iniciar o frontend Next.js do V5 (tela de seleção + wizard)
   - Testes de integração end-to-end

---

## Notas e Decisões Tomadas

- **Arquitetura:** 1 contrato = 1 módulo Python isolado. Mudança em c1565 não toca c0908.
- **Interface ContractEngine:** ABC com `scan()`, `build_word()`, `get_items()`, `get_meta_fields()`, `validate_folder()`.
- **API:** `/api/contracts/{id}/scan|generate|validate|items` — sem mais flags `tipo_relatorio`.
- **Logo:** LOGO.png da TM embutido em base64, com glow laranja pulsante. Quadrado laranja aposentado.
- **Frontend Store:** `useContractStore(id)` por contrato — sem estado global misturado.

---

## Registro de Sessões

| Data | O que foi feito |
|------|----------------|
| 2026-05-20 | Análise macro V4 · PRD MVP · Scaffold · Wireframe HTML · Core Engine ABC · Logo skill atualizada |
| 2026-05-21 | Engenharia reversa completa do V4 · Mapeamento dos 10 tipos de bloco · `reverse_engineering.md` · `wireframe_v5_blocks.html` (blocos visuais + painel SP2) · Confirmação real dos placeholders via python-docx (nomes curtos: `{{ag_cod}}`, `{{dt_atend}}`, etc.) · Criação dos engines para todos os 9 contratos · `wireframe_v5_overleaf.html` — layout Overleaf 3 painéis: nav contratos + editor + live preview Word simulado, dark theme #111110, sem seletor de motor |
