# 🧠 README OPERACIONAL — TM Sempre Tecnologia
**Hub Central de Controle do Ecossistema Profissional TM**
**Criado em:** 2026-05-27  
**Versão:** 2.0.0

---

## 🎯 O Que É Este Workspace

Esta pasta (`_workspace/`) é o **hub central de controle do ecossistema profissional** de Thiago Nascimento — TM Sempre Tecnologia. Ela governa **três pilares** do trabalho de vida:

| Pilar | Pasta | Papel |
|-------|-------|-------|
| 🏭 Produto | `tm-tecnologia/` | AutoRelatório V5 — sistema principal |
| 🔧 Ferramentas | `TM-MEUS-APPS/` | Apps, Skills Claude Code, Design System |
| 📋 Operação | `000 - Minha Demanda/` | Controle de demandas reais de campo (BB) |

> **Veja o mapa completo em [`ECOSISTEMA_TM.md`](ECOSISTEMA_TM.md)**

Este workspace centraliza:

- Automações e scripts reutilizáveis (para os 3 pilares)
- Prompts de IA validados e curados
- Workflows operacionais documentados
- Templates de documentos e execução
- Memória técnica e decisões arquiteturais
- Logs de auditoria e histórico de execuções
- Configurações de agentes IA

> **Princípio:** Toda automação criada aqui é documentada, rastreável e expansível. Nada existe sem registro.

---

## 📂 Estrutura de Pastas

```
_workspace/
├── automacoes/          → Scripts e automações prontos para uso
├── prompts/             → Biblioteca de prompts reutilizáveis
│   ├── reutilizaveis/   → Prompts validados e estáveis
│   ├── skills/          → Skills modulares por domínio
│   └── snippets/        → Fragmentos rápidos de prompt
├── workflows/           → Fluxos de trabalho documentados
│   ├── validados/       → Workflows aprovados em produção
│   └── em-construcao/   → Workflows em desenvolvimento
├── templates/           → Templates de documentos e execução
│   ├── docx/            → Templates Word (.docx)
│   ├── excel/           → Templates Excel (.xlsx)
│   ├── relatorio/       → Templates de relatórios operacionais
│   └── prompt/          → Templates de prompts por categoria
├── logs/                → Registro de execuções e auditoria
│   ├── execucoes/       → Log de cada automação executada
│   ├── erros/           → Erros capturados e análises
│   └── auditorias/      → Revisões de qualidade
├── docs/                → Documentação técnica
│   ├── specs/           → Especificações de automações
│   ├── decisoes/        → ADRs (Architectural Decision Records)
│   └── tutoriais/       → Guias de uso passo a passo
├── scripts/             → Scripts por linguagem
│   ├── python/          → Scripts Python
│   ├── powershell/      → Scripts PowerShell
│   └── batch/           → Scripts .bat
├── testes/              → Suite de testes
│   ├── fixtures/        → Dados de entrada para testes
│   ├── resultados/      → Resultados de execuções de teste
│   └── snapshots/       → Snapshots de saída esperada
├── scans/               → Varreduras e análises automáticas
│   ├── resultados/      → Resultados de cada scan
│   └── historico/       → Histórico de scans anteriores
├── memoria/             → Inteligência operacional acumulada
│   ├── descobertas/     → Achados técnicos documentados
│   ├── heuristicas/     → Regras e padrões validados
│   └── decisoes-arquiteturais/ → Registro de decisões de design
├── snapshots/           → Backups pontuais do estado do projeto
│   ├── contratos/       → Estado dos 9 contratos por data
│   └── backups/         → Backups manuais e automáticos
├── pipelines/           → Definições de pipelines de automação
│   ├── definicoes/      → YAML/JSON de configuração de pipelines
│   └── resultados/      → Outputs de execuções de pipeline
├── agentes/             → Configuração de agentes IA
│   ├── configs/         → Perfis e configs de cada agente
│   ├── prompts/         → Prompts de sistema por agente
│   └── logs/            → Histórico de sessões por agente
└── configs/             → Configurações globais do workspace
```

---

## 🚀 Como Usar Este Workspace

### Para Claude Code (AI Copilot)
1. Leia `CONTEXTO_PROJETO.md` antes de qualquer tarefa
2. Consulte `FLUXO_DE_TRABALHO.md` para entender o processo correto
3. Registre descobertas em `memoria/descobertas/`
4. Use prompts de `prompts/reutilizaveis/` antes de criar novos
5. Documente toda automação criada em `docs/specs/`

### Para Operador Humano (Thiago)
1. Verifique `ROADMAP.md` para ver o estado atual do projeto
2. Consulte `logs/execucoes/` para rastrear o histórico
3. Use `workflows/validados/` para tarefas repetitivas
4. Registre novos templates em `templates/`

---

## 🔗 Ecossistema Coberto

### Pilar 1 — tm-tecnologia (Produto)
| Projeto | Localização | Status |
|---------|-------------|--------|
| AutoRelatório V5 | `../AutoRelatorio_V5/` | 🔶 Em Desenvolvimento |
| AutoRelatório V4 | `../AutoRelatorio_V4/` | ✅ Referência Canônica |
| Documentos Preventivas | `../Documentos Preventivas/` | ✅ Produção |

### Pilar 2 — TM-MEUS-APPS (Ferramentas)
| Recurso | Localização | Status |
|---------|-------------|--------|
| Skills Claude Code | `C:\...\TM-MEUS-APPS\Meus Plugins e Skills\` | ✅ Biblioteca Ativa |
| Golden Apps | `C:\...\TM-MEUS-APPS\01_Golden_Apps_meu_uso\` | ✅ Em Uso |
| Design System TM | `C:\...\TM-MEUS-APPS\TM Design System - NOVO Laranjado\` | ✅ Identidade Visual |
| Legado | `C:\...\TM-MEUS-APPS\03_Arquivo_Morto_Legado\` | 📦 Arquivo |

### Pilar 3 — 000 - Minha Demanda (Operação)
| Pasta | Localização | Papel |
|-------|-------------|-------|
| Sala de Controle | `C:\...\000 - Minha Demanda\0 - Sala de controle\` | Dashboard diário |
| Preventivas 2026 | `C:\...\000 - Minha Demanda\1 - Preventivas 2026\` | Relatórios do ano |
| Em Andamento | `C:\...\000 - Minha Demanda\2 - Em andamento\` | ← Foco atual |
| Aguardando | `C:\...\000 - Minha Demanda\3 - Aguardando correção\` | Pausados |
| Arquivo Morto | `C:\...\000 - Minha Demanda\5 - Arquivo morto\` | Concluídos |

> Para o mapa completo e fluxo de conexão entre os três pilares: [`ECOSISTEMA_TM.md`](ECOSISTEMA_TM.md)

---

## 📋 Convenções Obrigatórias

1. **Nomes de arquivo:** `KEBAB-CASE.md` para docs, `snake_case.py` para scripts
2. **Todo script novo:** deve ter cabeçalho com `# OBJETIVO:`, `# ENTRADA:`, `# SAÍDA:`, `# DEPENDÊNCIAS:`
3. **Todo log:** formato `YYYY-MM-DD_HH-MM_<acao>.log`
4. **Todo prompt:** deve ter seção de `## Contexto`, `## Instruções`, `## Exemplo`
5. **Toda decisão arquitetural:** registrar em `memoria/decisoes-arquiteturais/`

---

## ⚠️ Regras de Ouro

- ❌ **NUNCA** mover arquivos de produção sem backup em `snapshots/`
- ❌ **NUNCA** criar automação sem documentar em `docs/specs/`
- ✅ **SEMPRE** testar em `testes/fixtures/` antes de rodar em produção
- ✅ **SEMPRE** registrar erros em `logs/erros/` com análise de causa-raiz
- ✅ **SEMPRE** reutilizar o que existe antes de criar do zero

---

*Mantido por: Claude Code + Thiago Nascimento — TM Sempre Tecnologia*
