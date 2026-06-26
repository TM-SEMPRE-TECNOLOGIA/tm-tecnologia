# 🌐 ECOSSISTEMA TM SEMPRE TECNOLOGIA
**Mapa completo do ambiente profissional de Thiago Nascimento**  
**Este workspace (`_workspace/`) é o hub central de controle de todo o ecossistema.**  
**Atualizado em:** 2026-05-27

---

## 🗺️ Os Três Pilares

| # | Pasta | Papel | Caminho |
|---|-------|-------|---------|
| 1 | **tm-tecnologia** | 🏭 Produto — AutoRelatório V5 | `C:\Users\thiag\Desktop\tm-tecnologia` |
| 2 | **TM-MEUS-APPS** | 🔧 Ferramentas — Apps, Skills, Design | `C:\Users\thiag\Desktop\TM-MEUS-APPS` |
| 3 | **000 - Minha Demanda** | 📋 Operação — Demandas reais de campo | `C:\Users\thiag\Desktop\000 - Minha Demanda` |

> **Este workspace (`_workspace/`) vive dentro de `tm-tecnologia` mas governa os três pilares.**  
> Automações, prompts, skills e memória técnica daqui servem ao ecossistema completo.

---

## 🏭 Pilar 1 — tm-tecnologia (Produto)

```
c:\Users\thiag\Desktop\tm-tecnologia\
├── _workspace/              ← HUB CENTRAL (este diretório)
├── AutoRelatorio_V5/        ← Produto principal (em desenvolvimento)
│   ├── backend/             ← FastAPI + Python (9 módulos de contrato)
│   ├── frontend/            ← Next.js + TypeScript + Zustand
│   └── run.bat              ← Inicializador geral
├── AutoRelatorio_V4/        ← Versão anterior (referência canônica)
│   └── APP/backend/         ← 41 arquivos Python — código de referência
└── Documentos Preventivas/  ← Templates e documentos reais dos 9 contratos
```

**Responsabilidade:** Desenvolvimento, manutenção e evolução do sistema AutoRelatório.  
**Sprint atual:** 3 — Upload de fotos via browser → geração de `.docx` no backend.

---

## 🔧 Pilar 2 — TM-MEUS-APPS (Ferramentas)

```
C:\Users\thiag\Desktop\TM-MEUS-APPS\
├── 01_Golden_Apps_meu_uso/      → Apps próprios em produção
│   └── AutoRelatorio_V4/APP/   → V4 rodando como referência operacional
├── 03_Arquivo_Morto_Legado/     → Versões antigas e código legado
│   └── .NEXT APPS/TURBO DEV/   → Experimentos descontinuados
├── Meus Plugins e Skills/       → Biblioteca de Skills do Claude Code ⭐
│   ├── relatorio-preventivo.skill
│   ├── relatorio-preventivo-v2.skill
│   ├── tm-automatizando/
│   ├── tm-testes/
│   ├── tm-design-system-plugin/
│   ├── antigravity-awesome-skills/
│   ├── organizar-relatorio.skill/
│   └── legenda-descricao-sp2.skill/
├── TM Design System - NOVO Laranjado/  → Design system (identidade visual)
├── Monetizacao_com_IA/          → Experimentos de monetização com IA
└── auto-chat-naming/            → Utilitário de naming automático
```

**Responsabilidade:** Manter, evoluir e reutilizar ferramentas, skills e o design system TM.  
**Asset mais crítico:** `Meus Plugins e Skills/` — biblioteca central de automações do Claude Code.

### Skills Disponíveis (ativar com `/nome-da-skill`)

| Skill | Comando | Propósito |
|-------|---------|-----------|
| relatorio-preventivo | `/relatorio-preventivo` | Extrair itens, gerar memorial, verificar divergências |
| relatorio-preventivo-v2 | `/relatorio-preventivo-v2` | Versão aprimorada |
| tm-automatizando | `/tm-automatizando` | SP2 completo — pré-finalizados |
| tm-testes | `/tm-testes` | Automação E2E com Playwright |
| tm-design-system-plugin | `/tm-design-system-plugin` | Design system laranjado |
| antigravity-awesome-skills | `/brainstorming`, `/debug` | Skills base multifuncionais |
| organizar-relatorio | `/organizar-relatorio` | Organização de relatórios |
| legenda-descricao-sp2 | `/legenda-descricao-sp2` | Legendas e descrições SP2 |

---

## 📋 Pilar 3 — 000 - Minha Demanda (Operação de Campo)

```
C:\Users\thiag\Desktop\000 - Minha Demanda\
├── 0 - Sala de controle/        → Visão geral, dashboards, controle diário
├── 1 - Preventivas 2026/        → Relatórios preventivos do ano corrente
├── 2 - Em andamento/            → Trabalhos em execução agora ← FOCO ATUAL
├── 3 - Aguardando correção/     → Itens pausados aguardando retorno do BB
├── 4 - Pessoal/                 → Documentos e controle pessoal
├── 5 - Arquivo morto/           → Trabalhos concluídos e arquivados
└── Placas de sinalização/       → Projeto EXPLAN — sinalização predial
```

**Responsabilidade:** Controle operacional de todas as demandas reais do Banco do Brasil.  
**Fluxo de trabalho:** demanda entra em `2 - Em andamento/` → processada com AutoRelatório → entregue → vai para `5 - Arquivo morto/`.

---

## 🔄 Como os Três Pilares Se Conectam

```
          ┌─────────────────────────────────────────────┐
          │          _workspace/ (HUB CENTRAL)           │
          │   Automações · Prompts · Skills · Memória    │
          └────────────┬───────────────────┬────────────┘
                       │                   │
          ┌────────────▼──────┐  ┌─────────▼────────────┐
          │  tm-tecnologia    │  │   TM-MEUS-APPS        │
          │  AutoRelatório V5 │  │   Skills + Apps       │
          └────────────┬──────┘  └─────────┬────────────┘
                       │                   │
          ┌────────────▼───────────────────▼────────────┐
          │          000 - Minha Demanda                  │
          │      Demandas reais → Relatórios gerados      │
          └──────────────────────────────────────────────┘
```

**Fluxo típico:**
1. Demanda entra em `2 - Em andamento/`
2. Fotos organizadas → AutoRelatório V5 (ou V4 como fallback) gera o `.docx`
3. Skills do Claude Code apoiam na análise, legendas e verificação
4. `.docx` revisado e enviado → demanda vai para `5 - Arquivo morto/`

---

## 📌 Regras do Ecossistema

1. **`_workspace/` é o hub** — toda automação nasce e é documentada aqui
2. **TM-MEUS-APPS** não é modificado por agentes IA sem confirmação explícita
3. **000 - Minha Demanda** é leitura apenas para agentes — nunca escrever ali sem instrução
4. **Skills** em `Meus Plugins e Skills/` são reutilizadas antes de qualquer nova criação
5. **Design system** laranjado TM é a identidade visual — sempre manter coerência

---

*Centro de controle: `C:\Users\thiag\Desktop\tm-tecnologia\_workspace\`*  
*Operado por: Thiago Nascimento — TM Sempre Tecnologia*
