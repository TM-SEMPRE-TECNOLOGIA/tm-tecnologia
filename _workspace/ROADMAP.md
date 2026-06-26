# 🛣️ ROADMAP — TM Sempre Tecnologia
**Estado atual, sprints em andamento e visão de futuro**
**Atualizado em:** 2026-05-27

---

## 📊 STATUS GERAL DO PROJETO

| Componente | Versão | Status |
|-----------|--------|--------|
| AutoRelatório | V5 | 🔶 80% — Sprint 3 pendente |
| Workspace de Automação | V1 | ✅ Criado (2026-05-27) |
| Skills TM | Múltiplas | ✅ Ativas |
| Documentação | V1 | ✅ Este workspace |

---

## ✅ CONCLUÍDO

### AutoRelatório V5 — Fundação (2026-05-20 a 2026-05-26)
- [x] PRD MVP definido
- [x] Scaffold de pastas criado
- [x] ContractEngine ABC implementado
- [x] Registry com os 9 contratos
- [x] Engines individuais para todos os 9 contratos
- [x] Templates .docx vinculados
- [x] UI Next.js — Layout, Step 1, Step 2 (90%), Step 3, Preview
- [x] Bridge API (checkHealth, generateReport, requestFile)
- [x] Engenharia reversa completa do V4 documentada
- [x] Wireframes HTML (blocos visuais + Overleaf 3 painéis)

### Workspace de Automação (2026-05-27)
- [x] Estrutura de 35 pastas criada
- [x] README_OPERACIONAL.md
- [x] CONTEXTO_PROJETO.md
- [x] FLUXO_DE_TRABALHO.md
- [x] PADROES_TECNICOS.md
- [x] MAPA_AUTOMACOES.md
- [x] MEMORIA_OPERACIONAL.md
- [x] ROADMAP.md
- [x] GUIA_AGENTES_IA.md
- [x] Templates base nas subpastas

---

## 🔶 EM ANDAMENTO

### Sprint 3 — Upload de Fotos via Browser
**Objetivo:** Permitir que o usuário selecione pasta de fotos no browser e o backend processe  
**Bloqueio atual:** Browser não pode fornecer `root_path` diretamente  
**Solução planejada:** FormData com `UploadFile[]` → tmpdir no backend → scanner → .docx

**Tarefas:**
- [ ] Criar endpoint `POST /api/contracts/{id}/generate-with-files`
- [ ] Frontend: componente de seleção de pasta (`webkitdirectory`)
- [ ] Backend: salvar files em tmpdir, montar estrutura de pastas
- [ ] Backend: executar scanner no tmpdir
- [ ] Retornar .docx como download
- [ ] Criar spec: `docs/specs/2026-05-27-upload-fotos.md`
- [ ] Criar fixture de teste para c0908

---

## 📋 BACKLOG

### Sprint 4 — Materiais dos Contratos
**Objetivo:** Completar items.json de todos os contratos  
**Bloqueio:** Aguardando Thiago enviar materiais dos 9 contratos  

| Contrato | Planilha Itens | Planilha Padrão | Exemplo .docx |
|----------|:--------------:|:---------------:|:-------------:|
| 0908 | ⏳ | ⏳ | ⏳ |
| 1507 | ⏳ | ⏳ | ⏳ |
| 1565 | ⏳ | ⏳ | ⏳ |
| 2056 | ⏳ | ⏳ | ⏳ |
| 2057 | ⏳ | ⏳ | ⏳ |
| 2626 | ⏳ | ⏳ | ⏳ |
| 2627 | ⏳ | ⏳ | ⏳ |
| 3575 | ⏳ | ⏳ | ⏳ |
| 6122 | ⏳ | ⏳ | ⏳ |

### Sprint 5 — QA e Testes
- [ ] Fixtures de teste para todos os contratos
- [ ] Testes de regressão V5 vs V4
- [ ] Playwright E2E do frontend
- [ ] Relatório de cobertura

### Sprint 6 — Automação de Workspace
- [ ] A09: QA Visual Playwright
- [ ] A10: Scanner de duplicações
- [ ] A11: Validador de pasta CLI
- [ ] A12: Exportador items.json de XLSX
- [ ] A13: Gerador de relatório de regressão

### Sprint 7 — Produção e Entrega
- [ ] Documentação de usuário final
- [ ] Empacotamento para uso sem Claude Code
- [ ] Pipeline de entrega de .docx por contrato
- [ ] A14: Geração em lote

---

## 🔮 VISÃO DE FUTURO (Pós-V5)

### AutoRelatório V6 — Idéias
- Geração automática de memorial de cálculo a partir das fotos (Vision AI)
- Integração direta com portal BB (envio automático)
- App mobile para captura de fotos já organizadas em campo
- Análise preditiva de itens por histórico de contratos

### Workspace de Automação — Evoluções
- Agentes autônomos por contrato (cada contrato tem seu agente especializado)
- Dashboard de status de todos os contratos em tempo real
- Sistema de alertas para pendências e prazos
- Integração com Obsidian para memória profunda

---

## 📅 HISTÓRICO DE SPRINTS

| Sprint | Período | Objetivo | Status |
|--------|---------|----------|--------|
| Sprint 1 | 2026-05-20/21 | Fundação V5 + Wireframes | ✅ Concluído |
| Sprint 2 | 2026-05-21/26 | Engenharia reversa + Engines | ✅ Concluído |
| Sprint 3 | 2026-05-27+ | Upload fotos via browser | 🔶 Em andamento |
| Sprint 4 | TBD | Materiais dos contratos | 📋 Pendente materiais |
| Sprint 5 | TBD | QA e testes | 📋 Planejado |
| Sprint 6 | TBD | Automação workspace | 📋 Planejado |
| Sprint 7 | TBD | Produção | 📋 Planejado |

---

*Atualizar este arquivo ao início e fim de cada sprint.*
