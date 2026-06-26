# 🗺️ MAPA GERAL DO ECOSSISTEMA TM
> TM Sempre Tecnologia — Thiago Nascimento
> Atualizado: 2026-05-27 | Gerado por varredura real das 3 pastas

Este arquivo é a **bússola** do ecossistema. Antes de criar qualquer coisa, consulte aqui.
Antes de buscar qualquer coisa, consulte aqui primeiro.

---

## 📐 A Lei das 3 Pastas

```
Desktop\
├── tm-tecnologia\          → LABORATÓRIO  — onde o código nasce e evolui
├── TM-MEUS-APPS\           → BIBLIOTECA   — apps prontos, skills, design, legado
└── 000 - Minha Demanda\    → CAMPO        — demandas reais com cliente e prazo
```

**Regra de ouro:** Cada coisa tem um lugar. Se não sabe onde criar, leia a seção "Onde cada coisa vive" no final.

---

## 🔬 PASTA 1 — `tm-tecnologia\` (Laboratório)

**Propósito:** Desenvolvimento ativo. Tudo que está sendo construído agora.

```
tm-tecnologia\
├── _workspace\                     ← CENTRO DE CONTROLE (este arquivo está aqui)
├── AutoRelatorio_V5\               ← 🔶 APP PRINCIPAL — em desenvolvimento ativo
│   ├── backend\
│   │   ├── core\                   ← Módulos compartilhados (engine, registry, word_utils)
│   │   └── contracts\              ← 9 módulos isolados: c0908 c1507 c1565 c2056 c2057 c2626 c2627 c3575 c6122
│   ├── frontend\                   ← Next.js App Router (app/ components/ hooks/ lib/ store/)
│   ├── .context\                   ← Contexto técnico para IA
│   ├── .docs\                      ← Wireframes e documentação técnica
│   ├── INICIAR.bat / run.bat       ← Inicializar app (duplo-clique)
│   ├── PROXIMO_PASSO.md            ← ⭐ Leia antes de codar — estado atual do sprint
│   ├── PROGRESS.md                 ← Histórico de progresso
│   ├── ENGENHARIA_REVERSA_COMPLETA.md ← Mapa técnico completo do V4→V5
│   └── PENDENCIAS_V5.md            ← O que falta fazer
│
├── AutoRelatorio_V4\               ← ✅ REFERÊNCIA CANÔNICA — não alterar
│   └── APP\backend\                ← Código Python de referência para portagem
│
└── Documentos Preventivas\         ← 📋 Templates e planilhas reais por contrato
    ├── 1 - CONTRATO - DIVINÓPOLIS - 2056\
    ├── 2 - CONTRATO - VARGINHA - 2057\
    ├── 3 - CONTRATO - MATO GROSSO DO SUL - 6122\
    ├── 4 - CONTRATO - SÃO PAULO - 0908\
    ├── 5 - CONTRATO - CUIABA - 1507\
    ├── 6 - CONTRATO - SALINAS - 2626\
    ├── 7 - CONTRATO - VALADARES - 2627\
    ├── 8 - CONTRATO - TANGARA DA SERRA - 3575\
    ├── 9 - CONTRATO - SAO JOSE DO RIO PRETO - 1565\   ← SP2 EXCLUSIVO
    ├── Planilhas de memorial\
    ├── MEMORIAL DE ITENS - LOTE SP.xlsx
    └── PREVISÃO ORÇAMENTÁRIA *.xlsx  (por contrato)
```

### Estado atual do AutoRelatório V5 (2026-05-27)
| Componente | Status |
|-----------|--------|
| UI / Layout | ✅ 100% |
| Step 1 Formulário | ✅ 100% |
| Step 2 Blocos | ⚠️ 90% |
| Step 3 Resumo | ✅ 100% |
| Preview | ✅ 100% |
| Backend 9 contratos | ⚠️ 80% |
| Bridge API | ✅ 100% |
| Upload fotos → backend | ❌ 0% — **Sprint 3 pendente** |

**Como iniciar:** duplo-clique `run.bat` → http://localhost:3000 (app) + http://localhost:5000/docs (API)

---

## 📚 PASTA 2 — `TM-MEUS-APPS\` (Biblioteca)

**Propósito:** Tudo que já existe e pode ser reutilizado. Apps prontos, skills, design, legado.

```
TM-MEUS-APPS\
├── 01_Golden_Apps_meu_uso\         ← ✅ APPS EM USO ATIVO
│   ├── AutoRelatorio_V2\           ← Versão legacy (referência UI)
│   ├── AutoRelatorio_V3\           ← Primeira versão completa (Fabric.js, 20+ endpoints)
│   ├── AutoRelatorio_V3.2\         ← Placeholders {{campo}}, 70+ testes
│   ├── AutoRelatorio_V4\           ← SP2, Zustand, 4 views — referência de lógica SP
│   ├── squad-brainstorming\        ← Squad de ideação
│   ├── squad-docfactory\           ← Factory de documentos
│   └── Execuções em prompt\        ← Histórico de execuções
│
├── Meus Plugins e Skills\          ← 🔧 BIBLIOTECA DE SKILLS TM
│   ├── relatorio-preventivo.skill\ ← Skill principal: extrair itens, gerar memorial
│   ├── relatorio-preventivo-v2\    ← Versão 2 do skill preventivo
│   ├── tm-automatizando\           ← Completar relatórios SP2 pré-finalizados
│   ├── tm-testes\                  ← Automação E2E com Playwright
│   ├── tm-design-system-plugin\    ← Design system TM
│   ├── legenda-descricao-sp2\      ← Legendas e descrições SP2
│   ├── organizar-relatorio\        ← Organizar relatórios
│   ├── antigravity-awesome-skills\ ← Skills base: brainstorming, debug, code review
│   ├── impeccable-framework\       ← Framework de qualidade
│   └── opensquad\                  ← Framework multi-agente
│
├── TM Design System - NOVO Laranjado\ ← 🎨 IDENTIDADE VISUAL OFICIAL
│   └── (tokens, cores, tipografia — laranjado como primário)
│
├── scratch\                        ← 🧪 Scripts de análise e auditoria avulsos
│   ├── audit_barretos.py, audit_deep.py
│   ├── inspect_*.py, process_*.py, validate_*.py
│   └── (scripts one-off de análise de relatórios)
│
├── 03_Arquivo_Morto_Legado\        ← 🗄️ LEGADO — apenas referência, não alterar
│   ├── LEGADO - ANTIGOS\
│   │   ├── TM STUDIO RELATORIO\    ← Proto-V1 FastAPI (origem histórica)
│   │   ├── TM Gerenciador V-2\     ← CMMS completo (15 componentes: Dashboard, ImportOS…)
│   │   ├── TM-Design-System\       ← Design system antigo
│   │   └── Bot-chat-next.js\       ← Experimento de chat
│   │
│   ├── .NEXT APPS\                 ← Apps Next.js legacy
│   │   ├── TM Relatorio SP\        ← V0.9 — PONTO DE FUSÃO (UI NX + lógica SP)
│   │   ├── TM Gerenciador\         ← Gerenciador de OS (React/Vite, Drizzle, PRD.md)
│   │   ├── TM Levantamento\        ← App de levantamento de campo
│   │   ├── TM Ordens\              ← Gestão de ordens de serviço
│   │   ├── TM Extrator / 2.0\      ← Extrator de dados
│   │   ├── TM Comparador\          ← Comparador de versões
│   │   ├── TM Pastas\              ← Utilitário de pastas
│   │   ├── TM Gerador VBA\         ← Gerador VBA
│   │   ├── DEv HUB - PROJETO\      ← Hub de desenvolvimento
│   │   └── TURBO DEV\              ← Stack Turbo (antigravity, skills, opensquad)
│   │
│   └── .NEXT APPS 2\               ← Cópia/variante dos .NEXT APPS
│
├── output_claude\                  ← Outputs gerados por IA em sessões anteriores
├── diario_de_dev.md                ← 📓 Diário de desenvolvimento (última entrada: maio 2026)
├── MAPA_FORENSE_AUTORELATORIO.md   ← 🔬 Análise forense completa V1→V5
└── CHEAT_SHEET.md                  ← Referência rápida de comandos e fluxos
```

### Skills disponíveis via `/comando`
| Skill | Comando | Propósito |
|-------|---------|-----------|
| relatorio-preventivo | `/relatorio-preventivo` | 4 etapas: extrair → memorial → divergências → legendas |
| tm-testes | `/tm-testes` | E2E Playwright para apps locais |
| tm-automatizando | skill direto | Completar relatórios SP2 |
| legenda-descricao-sp2 | skill direto | Legendas e descrições SP2 |
| + 16 turbo workflows | `/turbo-*` | Ver `~/.claude/SKILLS_CATALOG.md` |

---

## 🏗️ PASTA 3 — `000 - Minha Demanda\` (Campo)

**Propósito:** Demandas reais com cliente, prazo e consequência. Operação pura.

```
000 - Minha Demanda\
├── 0 - Sala de controle\               ← 🎛️ CONTROLE GERAL
│   ├── MAFFENG - INTERATIVO\           ← App interativo de orçamentação (tem .git próprio)
│   │   ├── CONTROLADOR - PREVENTIVAS DO SEMESTRE.*
│   │   ├── JORNADA - RELATORIOS - AUTOMAÇÃO.*
│   │   ├── Meu Fluxo de trabalho.*
│   │   ├── MAFFENG - PINTURAS E AVISOS.html
│   │   └── checklist-levantamento preventivo.*
│   ├── BOTS de Descrição - Instruções\ ← Prompts usados para gerar descrições
│   │   ├── Instrução gerada pelo Claude.*
│   │   ├── Instruções qwen V2.md
│   │   └── V3.md
│   ├── Exemplos de relatórios - Modelo 3\ ← Modelos de referência do cliente
│   ├── MINHAS ATIVIDADES.png            ← Mapa visual das atividades
│   └── PRECIFICAÇÃO - ATUAL 23-01-2026.jpg
│
├── 1 - Preventivas 2026\               ← 📅 RELATÓRIOS PREVENTIVOS DO ANO
│   ├── 00 - Enviados\                  ← Já entregues ao cliente
│   ├── 01 - Apoio operacional\         ← Materiais de suporte
│   ├── 02 - Automações Ativas - Relatórios\ ← Automações em uso (desatualizado)
│   ├── 03 - Documentos Preventivas\    ← Docs por contrato
│   └── 04 - Assinaturas digitais\      ← Arquivos assinados
│
├── 2 - Em andamento\                   ← 🔶 DEMANDAS ATIVAS COM PRAZO
│   ├── IPUIUNA - 3986\                 ← Demanda ativa (contrato 3986)
│   ├── LAMBARI - 2245\                 ← Demanda ativa
│   └── PEDRALVA - 2424\                ← Demanda ativa
│
├── 3 - Aguardando correção\            ← ⏳ Retorno do cliente pendente
├── 4 - Pessoal\                        ← Assuntos pessoais
├── 5 - Arquivo morto\                  ← Demandas concluídas
└── Placas de sinalização - EXPLAN\     ← Material específico de placas
```

### Fluxo operacional das demandas
```
Levantamento (campo/Zap) → [2 - Em andamento] → Gerar relatório (AutoRelatório)
→ Enviar ao cliente → [1 - Preventivas 2026\00 - Enviados] → CONCLUÍDA → [5 - Arquivo morto]
```

---

## 🧠 ONDE CADA TIPO DE COISA VIVE

| O que você precisa criar/guardar | Onde vai |
|----------------------------------|----------|
| App novo em desenvolvimento | `tm-tecnologia\` |
| Código de produção ativo | `tm-tecnologia\AutoRelatorio_V5\` |
| Script de análise avulso / one-off | `TM-MEUS-APPS\scratch\` |
| Skill novo ou atualizado | `TM-MEUS-APPS\Meus Plugins e Skills\` |
| Template Word/Excel reutilizável | `tm-tecnologia\_workspace\templates\` |
| Automação documentada | `tm-tecnologia\_workspace\automacoes\` |
| Decisão arquitetural | `tm-tecnologia\_workspace\memoria\decisoes-arquiteturais\` |
| Descoberta técnica | `tm-tecnologia\_workspace\memoria\descobertas\` |
| Demanda com cliente e prazo | `000 - Minha Demanda\2 - Em andamento\` |
| Relatório preventivo entregue | `000 - Minha Demanda\1 - Preventivas 2026\00 - Enviados\` |
| Referência de código legado | `TM-MEUS-APPS\03_Arquivo_Morto_Legado\` (só leitura) |

---

## 🔗 CONEXÕES ENTRE AS 3 PASTAS

```
000 - Minha Demanda\2 - Em andamento\
         ↓ (fotos do levantamento)
tm-tecnologia\AutoRelatorio_V5\
         ↓ (gera .docx)
000 - Minha Demanda\1 - Preventivas 2026\00 - Enviados\

TM-MEUS-APPS\Meus Plugins e Skills\
         ↓ (skills chamados durante o trabalho)
Qualquer das 3 pastas

tm-tecnologia\_workspace\
         ↓ (centro de controle — referencia e documenta tudo)
As 3 pastas
```

---

## 📍 REFERÊNCIAS RÁPIDAS — "Onde está X?"

| O que você procura | Onde está |
|-------------------|-----------|
| Código fonte do AutoRelatório V5 | `tm-tecnologia\AutoRelatorio_V5\` |
| Templates .docx dos 9 contratos | `tm-tecnologia\AutoRelatorio_V5\backend\contracts\cXXXX\template\` |
| Planilhas de orçamento por contrato | `tm-tecnologia\Documentos Preventivas\` |
| Código de referência V4 (lógica SP) | `TM-MEUS-APPS\01_Golden_Apps_meu_uso\AutoRelatorio_V4\` |
| Análise forense completa V1→V5 | `TM-MEUS-APPS\MAPA_FORENSE_AUTORELATORIO.md` |
| Design System (cores, tokens) | `TM-MEUS-APPS\TM Design System - NOVO Laranjado\` |
| Skills de automação TM | `TM-MEUS-APPS\Meus Plugins e Skills\` |
| Bots de descrição (prompts de campo) | `000 - Minha Demanda\0 - Sala de controle\BOTS de Descrição - Instruções\` |
| Exemplos de relatórios do cliente | `000 - Minha Demanda\0 - Sala de controle\Exemplos de relatórios - Modelo 3\` |
| Demandas ativas agora | `000 - Minha Demanda\2 - Em andamento\` |
| Relatórios já entregues | `000 - Minha Demanda\1 - Preventivas 2026\00 - Enviados\` |
| MAFFENG (orçamentação interativa) | `000 - Minha Demanda\0 - Sala de controle\MAFFENG - INTERATIVO\` |
| Scripts de auditoria avulsos | `TM-MEUS-APPS\scratch\` |
| Diário de desenvolvimento | `TM-MEUS-APPS\diario_de_dev.md` |
| TM Gerenciador de OS (CMMS legado) | `TM-MEUS-APPS\03_Arquivo_Morto_Legado\LEGADO - ANTIGOS\TM Gerenciador V-2\` |
| Próximo passo do sprint atual | `tm-tecnologia\AutoRelatorio_V5\PROXIMO_PASSO.md` |
| Roadmap geral | `tm-tecnologia\_workspace\ROADMAP.md` |
| Guia operacional da skill relatorio-preventivo | `tm-tecnologia\_workspace\GUIA_RELATORIO_PREVENTIVO.html` |
| Este mapa | `tm-tecnologia\_workspace\MAPA_GERAL.md` |

---

## ⚠️ ALERTAS DE NAVEGAÇÃO

- **`03_Arquivo_Morto_Legado\`** = referência somente. Nunca alterar.
- **`TM Relatorio SP`** (legado) = V0.9, ponto de fusão — fonte de lógica SP ainda válida
- **`TM Gerenciador V-2`** (legado) = 15 componentes CMMS completos — fonte de referência UI
- **`scratch\`** = scripts de análise temporários — não são produção
- **`_workspace\`** = novo, estruturado, **vazio de conteúdo ainda** — alimentar gradualmente
- Não existe "TM Construtora" — sempre **TM Sempre Tecnologia**

---

*Mantido por: Thiago Nascimento + Claude Code — TM Sempre Tecnologia*
*Atualizar sempre que uma pasta nova for criada ou um app mudar de status*
