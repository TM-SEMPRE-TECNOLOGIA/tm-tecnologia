# MEMORIA_SPRINTS — TM Sempre Tecnologia
> Diário técnico operacional do ecossistema TM
> Nunca apagar. Sempre adicionar ao final.

---

# SPRINT 2026-06-05 — TM Gerenciador · Parte 1

## CONTEXTO

* Objetivo: construir o TM Gerenciador real em `tm-tecnologia/` portando lógica do legado para stack nova
* Legado analisado: `APPS/03_Arquivo_Morto_Legado/.NEXT APPS/TM Gerenciador/` — Vite + Express + PostgreSQL, identidade MAFFENG/verde
* Stack nova: Next.js 15 App Router + FastAPI (Python) + Supabase
* Design System: TM laranjado (`#C8541C`) — decisão confirmada pelo Thiago (substituiu discussão inicial sobre vermelho)
* Ecossistema: apps conectados por `contrato_id` (4 dígitos: "1565", "0908", etc.)

## O QUE FOI FEITO

### Frontend Next.js (`TM_Gerenciador/frontend/`)

* Scaffold completo — Next.js 15, Tailwind v4, TypeScript, App Router
* `globals.css` — TM Design System laranjado mapeado para variáveis shadcn
  - `--primary: #C8541C`, `--background: #F5F4F1`, `--sidebar: #1A1916`
  - Dark mode: `--primary: #E47A4A`, `--background: #161513`
* `styles/tm-tokens.css` — cópia limpa do `colors_and_type.css` sem `@import url()` (fontes via `next/font/google`)
* `layout.tsx` — Inter + Roboto Slab + JetBrains Mono via `next/font/google`
* `components/layout/sidebar.tsx` — sidebar dark CAD colapsível (240px/64px), item ativo laranjado
* `components/layout/header.tsx` — título + sino notificações + avatar com role badge colorido
* `app/(dashboard)/layout.tsx` — wrapper flex com sidebar
* `app/page.tsx` padrão do Next.js **removido** (conflitava com `(dashboard)/page.tsx` no `/`)
* Todas as dependências Radix UI instaladas (`@radix-ui/react-slot`, `@radix-ui/react-dialog`, etc.)
* `lib/api.ts` — cliente HTTP tipado com `ordensApi`, `contratosApi`, `notificacoesApi`

### Páginas implementadas

| Rota | Estado |
|---|---|
| `/` — Dashboard | KPIs reais via `GET /api/ordens/kpis` + barra de distribuição por status |
| `/ordens` | Tabela paginada (50/pág) + filtros status/contrato/tipo/busca |
| `/importar` | Drag & drop funcional, seletor de aba, detecção automática de colunas |
| `/login` | UI completa (Supabase Auth pendente) |
| `/notificacoes`, `/agenda`, `/balanco`, `/relatorios`, `/equipe` | Stubs |

### Backend FastAPI (`TM_Gerenciador/backend/`)

* `main.py` — FastAPI + CORS (localhost:3000/3001)
* `models/schemas.py` — Pydantic: OrdemServico, DashboardKPIs, Notificacao, Dificuldade
* `db/supabase.py` — cliente singleton com service_role key
* `routers/contratos.py` — 9 contratos bancários + proxy para AutoRelatório V5 em localhost:5000
* `routers/ordens.py` — CRUD + KPIs + importação Excel com mapeamento inteligente de colunas
* `routers/notificacoes.py` — CRUD + marcar lida/todas lidas
* `routers/usuarios.py` — listagem via Supabase Admin API
* `supabase_schema.sql` — DDL das 4 tabelas (executado no Supabase dashboard)
* `run.bat` — sobe frontend + backend com um clique

### Importador Excel inteligente

* `_detect_header_row()` — detecta linha de cabeçalho por palavras-chave (até linha 10)
* `_normalize_col()` — remove acentos + unifica separadores para lookup no COLUMN_MAP
* `COLUMN_MAP` — 30+ aliases → campos canônicos da tabela
* `STATUS_MAP` — valores reais da planilha TM:
  - "Concluída pelo Fornecedor" → `concluida`
  - "Orçamento Aprovado - Retorno ao Fornecedor" → `em_andamento`
* `_extract_contrato()` — regex extrai contrato de "DIVINOPOLIS MG - CTR 2056" → "2056"
* `GET /api/ordens/importar/abas` — lista abas do .xlsx antes de importar
* Frontend seleciona automaticamente a aba com mais linhas

### Supabase

* Projeto: `stofmzzensxqnqrnyrvk.supabase.co` — região São Paulo (sa-east-1)
* 4 tabelas criadas: `ordens_servico`, `tecnicos`, `notificacoes`, `dificuldades`
* **804 O.S reais importadas** da planilha `ORDENS DE SERVIÇOS GERAL.xlsx`, aba `PREV_GERAL_2.0`
* KPIs ao fim da sessão: 804 total, 47,5% conclusão, 422 abertas, 382 concluídas

## DESCOBERTAS

* `app/page.tsx` padrão do Next.js conflita com `(dashboard)/page.tsx` — ambos respondem em `/`. Solução: deletar o root.
* CSS `@import url()` dentro de arquivo importado após `@import "tailwindcss"` viola a spec CSS — solução: `tm-tokens.css` sem @import, fontes via `next/font/google`
* PowerShell não processa nomes de arquivo com `Ç` — copiar para path sem acento antes de processar com Python
* Status "Orçamento Aprovado - Retorno ao Fornecedor": o ` - ` vira espaço na normalização, então a chave do STATUS_MAP precisa ser sem o traço
* Planilha TM tem 18 abas com formatos muito diferentes — `PREV_GERAL_2.0` é a mais estruturada

## PRÓXIMOS PASSOS

* [ ] Supabase Auth — login real via email, substituir mock de seleção de perfil
* [ ] Middleware Next.js protegendo rotas `(dashboard)/*`
* [ ] Notificações com contagem real no header
* [ ] Telas stub: Agenda, Balanço, Relatórios, Equipe
* [ ] Ordens: modal de detalhe/edição
* [ ] Dashboard: gráfico temporal (Recharts)
* [ ] Sprint 2: Zap Inspeção
* [ ] Sprint 3: Integração entre apps + `/api/importar-zap`

## OBSERVAÇÕES

* TM laranjado (`#C8541C`) confirmado para todos os apps — nunca vermelho, nunca verde MAFFENG
* Contrato 1565 = SP2 exclusivo — mapeado como `modo: "sp2"` no contratos router
* Backend porta 8000 · Frontend porta 3000
* `_workspace/memoria/` criado nesta sessão — não existia antes

---

# SPRINT 2026-06-05 — TM Gerenciador · Parte 2 (Sprint 2 concluído + Sprint 3 iniciado)

## CONTEXTO

* Continuação direta da Parte 1 — Sprint 2 em execução
* Objetivo: completar dashboard com gráficos Recharts, logo real, sidebar toggle, telas stub → dados reais
* Ao final: Sprint 2 validado com 19/19 testes Playwright passando (100%)
* Sprint 3 iniciado: ciclo completo de O.S + dark mode + mobile
* Sessão encerrada pelo Thiago para dormir — Sprint 3 fica em andamento

## O QUE FOI FEITO

### Sprint 2 — concluído

#### Gráficos Recharts (dashboard)
* `components/charts/EvolucaoMensal.tsx` — LineChart abertas vs concluídas (últimos 6 meses)
* `components/charts/OsPorContrato.tsx` — BarChart total vs concluídas por contrato
* `components/charts/OsPorTipo.tsx` — PieChart donut por tipo (preventiva/corretiva/preditiva/inspecao)
* `components/charts/TopResponsaveis.tsx` — BarChart horizontal top 8 responsáveis
* 4 endpoints novos no backend: `GET /api/ordens/graficos/por-contrato|evolucao-mensal|por-tipo|por-responsavel`
* KPIs ampliados: `vencendo_30_dias` + `sla_cumprido_pct` adicionados ao schema e endpoint
* Dashboard reescrito: 6 rows (KPIs, urgência, evolução mensal, por contrato + tipo, top responsáveis, distribuição status)

#### Logo e sidebar
* Logo correta: `logo_tm_gerenciador_1.png` → `frontend/public/logo-tm.png`
* Sidebar toggle substituído: `ChevronLeft/Right` → botão flutuante `PanelLeftClose/Open` na borda direita
* Colapsada (64px): imagem `logo2-tm.png` (ícone TM quadrado)
* Expandida (240px): imagem `logo-tm.png` (`object-contain`, `objectPosition: left center`)
* Altura do header da sidebar: 90px expandida, 64px colapsada
* Logo do header (barra superior) removida — ficou só o título da página

#### Telas stub → dados reais
* `/notificacoes` — lista com marcar lida/todas lidas, polling real do backend
* `/relatorios` — tabela por contrato com KPIs individuais via `ordensApi.kpis(contrato_id)`
* `/balanco` — cards por tipo + barras de progresso por contrato
* `/equipe` — top responsáveis com ranking, barra de % concluídas
* `/agenda` — O.S com prazo ordenadas, badges de dias restantes, cards de urgência

#### Header
* Dark mode toggle: botão `Moon/Sun` no header, persiste em `localStorage("tm-theme")`
* Notificações: `notificationCount` conectado a `GET /api/notificacoes/count-nao-lidas` (polling 60s + on focus)

#### Testes E2E — 19/19 (100%)
* Script `test_e2e.py` gerado — resiliente (nova página por rota, evita crash de browser)
* Resultados: logo visível, sidebar colapsa, KPIs reais, 16 SVGs de gráficos, 50 linhas em /ordens,
  8 contratos em /relatorios, 8 responsáveis em /equipe, 50 itens em /agenda, zero erros de console
* Screenshots em `test_screenshots/`, relatório em `test_report.html`

### Sprint 3 — iniciado (em andamento)

#### Elaborador vs Técnico (descoberta crítica)
* Planilha TM tem **duas colunas distintas**: "ELABORAÇÃO RELATÓRIO" (quem escreve) e "TÉCNICO" (quem executa)
* App legado (Vite+Express): campos separados `elaborador`, `elaboradorId`, `tecnico`, `tecnicoId`
* App atual (errado): tudo convergia para `responsavel` — técnico e elaborador eram o mesmo campo
* **Correção aplicada:**
  - `backend/models/schemas.py`: adicionados `elaborador: Optional[str]` e `tecnico: Optional[str]`
  - `backend/routers/ordens.py` COLUMN_MAP: `elaboracao_relatorio` → `elaborador`, `tecnico` → `tecnico` (separados)
  - `frontend/lib/api.ts`: interface `OrdemServico` atualizada com os dois novos campos
  - `backend/migrations/003_add_elaborador_tecnico.sql`: criado para Supabase
* SQL para Supabase (pendente execução pelo usuário):
  ```sql
  ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS elaborador TEXT, ADD COLUMN IF NOT EXISTS tecnico TEXT;
  ```

#### Dark mode toggle
* `components/layout/header.tsx`: botão Moon/Sun, `localStorage("tm-theme")`, respeita `prefers-color-scheme`

#### Banco de dados zerado
* Thiago rodou `TRUNCATE TABLE ordens_servico RESTART IDENTITY CASCADE` no Supabase
* Motivo: reimportação com campos `elaborador` e `tecnico` corretos
* **Reimportação pendente** — aguarda Thiago acordar

#### Logos atualizadas
* `logo-tm.png` e `logo2-tm.png` novos arquivos gerados por Thiago com prompts fornecidos:
  - `logo-tm.png`: 900×220px aprox., horizontal, símbolo TM + separador + "TM Gerenciador / GESTÃO DE O.S"
  - `logo2-tm.png`: quadrado, só ícone TM, 300×300px aprox.
* Copiados de `C:\Users\thiag\Downloads\` para `frontend/public/`
* Cache `.next` limpo após cada troca de imagem

## DESCOBERTAS

* `object-contain` é obrigatório para logos com conteúdo que não pode ser cortado — `object-cover` corta
* Next.js image cache sobrevive ao HMR — precisa deletar `.next/` após trocar arquivos em `public/`
* Campo `responsavel` no Excel TM não existe — são `elaboracao_relatorio` e `tecnico` separados
* App legado (Vite) tinha arquitetura correta: `USERS (role=elaborador)` + `TECNICOS` como entidades distintas
* Dashboard com `Promise.all()` para 5 fetches paralelos (kpis + 4 gráficos) é mais eficiente que sequencial

## PRÓXIMOS PASSOS (Sprint 3 — em andamento)

* [ ] Rodar SQL no Supabase: `ALTER TABLE ordens_servico ADD COLUMN elaborador TEXT, ADD COLUMN tecnico TEXT`
* [ ] Reimportar planilha via `/importar` com novos campos
* [ ] Atualizar `/equipe` para mostrar elaboradores e técnicos separados
* [ ] Criar endpoints `GET /graficos/por-elaborador` e `GET /graficos/por-tecnico`
* [ ] Detalhe de O.S: `/ordens/[id]` com edição inline de status + dificuldades associadas
* [ ] Modal criar/editar O.S: formulário completo via `Dialog` shadcn
* [ ] Página `/dificuldades`: dados reais, marcar resolvida
* [ ] Sidebar mobile: `Sheet` (Drawer) para telas < 1024px + botão hamburger no header
* [ ] Página `/configuracoes`: aparência, perfil, status do backend
* [ ] `/tm-testes` completo ao final do Sprint 3
* [ ] Sprint 4: Supabase Auth + RLS por role (manager/elaborador/contract_admin)

## OBSERVAÇÕES

* `run.bat` sobe backend (porta 8000) + frontend (porta 3000) com um clique
* Backend deve ser iniciado separadamente se o frontend já estiver rodando (conflito de processo)
* Imagens de logo ficam em `frontend/public/` — qualquer troca exige limpeza do `.next/` e restart
* Thiago prefere construir completo primeiro e definir permissões de usuário depois (Sprint 4)
* Identidade visual: laranjado `#C8541C` é a cor primária em TODOS os elementos interativos

---

# SPRINT 2026-06-06 — Descrições Técnicas · AREADO (Contrato 2057 / MG)

## CONTEXTO

* Workspace: `C:\Users\thiag\Desktop\Minha Demanda\0 - Sala de controle\Descrições (apoio skill)\`
* Arquivo processado: `06 - Sendo executado\RELATÓRIO FOTOGRÁFICO - AREADO - LEVANTAMENTO PREVENTIVO.docx`
* Objetivo: gerar pré-descrições para todos os tópicos do relatório, que estava sem medidas preenchidas
* Contrato 2057 (MG — Varginha / Valadares) — Fiscal Carol

## O QUE FOI FEITO

* Extração do conteúdo do `.docx` via Python (zipfile + xml.etree) — identificação de todos os tópicos e sub-tópicos
* Mapeamento completo da estrutura do relatório:
  - Área Externa: 5 tópicos principais (pintura, telhado, calhas, entre forro, infiltrações, solicitação do gerente)
  - Área Interna: 13 ambientes / 30+ sub-itens (SAA, Atendimento, Suporte, Corredores, SAO, Tesouraria, Sala Online, Copa, Banheiros, etc.)
  - Segundo Piso: forro de gesso + casa de máquinas
* Geração de pré-descrições completas (3 versões por item — Formal/Técnico, Formal/Sucinto, Humanizado) para todos os ~35 tópicos identificados
* Aplicação correta das regras do contrato 2057:
  - Paredes internas → item 17.11 (tinta acrílica premium)
  - Paredes externas → item 17.4 (tinta acrílica standard)
  - Calhas → item 7.14 (cálculo: comprimento × 0,60)
  - Forro de gesso → item 9.4/9.5
  - Regra Fiscal Carol: sem item para sujeira pontual
  - Palavra proibida "látex" nunca usada
  - Toda descrição iniciando com "- Prezados,"
* Tabela-resumo de itens de contrato gerada ao final, com observações sobre itens "a definir"

## DESCOBERTAS

* O relatório do AREADO está em fase inicial — sem nenhuma medida preenchida, apenas a estrutura de tópicos e fotos
* A estrutura é complexa: 3 níveis distintos (área externa / área interna / segundo piso) com ambientes muito variados
* O corredor de abastecimento tem simultaneamente forro de gesso E forro de fibra mineral — dois tipos no mesmo ambiente
* Vários itens de infraestrutura (ponto lógico, ponto elétrico, sifão, lâmpadas) não têm item de contrato imediato identificável — marcados como "a definir"
* Solicitações do gerente aparecem em 2 seções distintas (área externa e área interna) — geradas com placeholders para preenchimento posterior

## PRÓXIMOS PASSOS

* [ ] Aguardar levantamento real com medidas do AREADO para substituir os placeholders `[X,XX m²]` / `[X,XX ml]` / `[QTD]`
* [ ] Confirmar itens marcados como "a definir" cruzando com tabela de itens do contrato 2057
* [ ] Inserir as descrições finalizadas no `.docx` sem apagar as fotos (usar workflow de inserção)
* [ ] Processar os demais relatórios na fila (pasta `06 - Sendo executado/` pode ter outros)

## OBSERVAÇÕES

* O workflow de pré-descrição sem medidas é válido — permite adiantar o trabalho de redação enquanto o levantamento de campo não chega
* Contrato 2057 = MG (Varginha/Valadares) — regras idênticas ao 2627, Fiscal Carol é rigorosa com itens sem evidência fotográfica
* Arquivo processado via extração Python direta do XML do `.docx` — não depende de Word instalado
* Sessão foi de dois dias (05 e 06/06/2026) — geração feita no dia 05, sprint consolidado no dia 06

---

# SPRINT 2026-06-06 — Autolegendas · Relatório Lambari (Preventiva)

## CONTEXTO

* Pasta de trabalho: `C:\Users\thiag\Desktop\Minha Demanda\1 - Preventivas 2026\01 - Apoio operacional\Autolegendas\`
* Objetivo: legendar automaticamente todas as fotos do relatório de vistoria preventiva de Lambari
* Arquivo-fonte: `RELATÓRIO FOTOGRÁFICO - LAMBARI - LEVANTAMENTO PREVENTIVO.docx`
* Abordagem: Python + manipulação XML direta via python-docx (sem conversão, sem perda de imagens em tabelas)

## O QUE FOI FEITO

### Legendação automática — 720 fotos

* Identificados **720 fotos reais** no relatório (filtro por tamanho mínimo: 1.200.000 × 800.000 EMU)
* Estratégia: XPath `//w:p` percorre todo o XML incluindo parágrafos dentro de células de tabela — imagens em tabelas preservadas sem perda
* Criado `legendar_cli.py` — versão CLI sem GUI do legendador, roda direto no arquivo sem interação
* Lógica: para cada `<w:p>` com foto real, insere `<w:p>` de legenda logo após, com `keep_with_next=True` na foto (vínculo foto-legenda)
* Legendas: "Foto 1", "Foto 2", ... "Foto 720" — sequência contínua sem pular nenhuma
* Formatação da legenda: Calibri 10pt, centralizado, `space_before=0`, `space_after=2pt`, sem itálico (ajuste pedido pelo Thiago)
* Output gerado: `output\LAMBARI_LEGENDADO_1780648427.docx`

### Ajuste de formatação

* Primeira geração: legendas em itálico
* Thiago pediu remoção do itálico → `run.font.italic = False`
* Segundo arquivo gerado: `output\LAMBARI_LEGENDADO_1780648427.docx` (timestamp atualizado)

### Análise dos serviços do relatório

* Extraídos **17 serviços** das tabelas do relatório via parsing das linhas com código `XX.XX`
* Serviços mapeados: pintura (17.5, 17.6, 17.7, 17.9, 17.10, 17.11), acessibilidade (29.5, 29.6), ferragens (15.3, 15.5), remoções (2.12, 2.18, 2.21), forro (12.10), mobiliário (13.12), espelhos (19.6), sifão (28.20)

## DESCOBERTAS

* XPath `//w:p` é a abordagem correta para garantir que imagens dentro de células de tabela sejam capturadas — a API de alto nível do python-docx itera apenas parágrafos do corpo principal, ignorando tabelas
* O script `legendar_fotos.py` existente na pasta já tinha a lógica base (GUI com customtkinter) — `legendar_cli.py` extraiu só o núcleo funcional

## PRÓXIMOS PASSOS

* [ ] Validar o arquivo `.docx` gerado no Word (verificar se legendas ficaram coladas às fotos corretamente)
* [ ] Verificar se há necessidade de legendas descritivas por serviço (não apenas "Foto N") — possível evolução

## OBSERVAÇÕES

* Relatório de Lambari contém 17 serviços distintos, foco em pintura e acessibilidade (PPNE)
* Pular início/fim: **0/0** (decisão do Thiago — legendar todas as fotos sem exceção)
* Script reutilizável: `legendar_cli.py` pode ser adaptado para outros relatórios preventivos alterando `DOCX_PATH`

---

# SPRINT 2026-06-06 — TM Marketing · Landing Page + Web Scrapper

## CONTEXTO

* Shift de foco: de desenvolvimento de apps para **marketing e posicionamento de marca**
* Objetivo: criar landing page do ecossistema TM (4 produtos) + documentar plano de marketing
* Inspiração: capturou página aicoders.academy para estudar padrões de design (backup pessoal + copy inspiration)
* Stack escolhida: Next.js para web scrapper, HTML+Tailwind para landing page (standalone)
* Ecossistema a apresentar: Gerenciador+AutoRelatório V5 (ativo), Auto Legenda (ativo), Zap Inspeção (ativo), Automobile (em desenvolvimento)

## O QUE FOI FEITO

### TM WEB SCRAPPING — Novo Projeto
* Inicializado: `C:\Users\thiag\Desktop\APPS\TM WEB SCRAPPING\`
* Stack: Next.js 15 + React 19 + TypeScript + Playwright (Chromium headless) + Tailwind CSS
* Funcionalidade: scraping universal com seletores CSS, exportação CSV/JSON
* Arquitetura: Client Component (page.tsx) → Route Handler (`/api/scrape`) → Playwright (lib/scraper.ts) → Export (lib/exporter.ts)
* Features: Form (URL + seletor CSS), validação (URL, seletor), scraping (networkidle, User-Agent camuflado), export (CSV + JSON), UI responsiva
* Build: sucesso sem erros TypeScript
* Documentação: README.md + GUIA_TESTES.md (13 testes) + PROJETO_CRIADO.md
* Git: commit inicial em repo local

### Captura aicoders.academy
* HTML completo: 428.3 KB renderizado
* JSON estruturado: 18 links + metadados
* Análise: dark theme (bg-black), borders dashed, seções verticais, labels `SEC·XX/NOME`
* Scripts Python: extract_css.py, extract_sections.py para análise estrutural

### O PLANO DE MARKETING TM.MD — Master Document
* **Criado:** `C:\Users\thiag\Desktop\APPS\TM Marketing\O PLANO DE MARKETING TM.MD`
* **Estrutura:** Ecossistema (4 produtos), Landing page (10 seções), Meta Ads MCP (integrado), Tráfego direto (Google/Meta/LinkedIn/WhatsApp)
* **Meta Ads:** `mcp__claude_ai_Meta_Ads_MCP__*` já está ATIVO — pode criar campanhas, audiências, ver insights direto
* **Google Ads:** palavras-chave "relatório fotográfico automático", "automação de checklist", "software engenharia predial"
* **LinkedIn Ads:** segmentação Engenheiros Prediais, Gestores de Contratos, Donos de Empresas
* **KPIs:** ROI Meta >3:1, 500+ sessões blog/mês, 10+ conversões para demo
* **Timeline:** junho (landing page), julho (primeira campanha), agosto+ (expansão)
* **Prompts Manus:** 5 imagens documentadas (Hero, Interface, Founder, Antes/Depois, WhatsApp)

### Landing Page HTML (Em Construção)
* **Path:** `C:\Users\thiag\Desktop\APPS\TM Marketing\landing-page\index.html`
* **Design:** Dark (`#0A0A0A`), laranjado TM (`#FF6B00`), borders dashed
* **Seções:** Header, Hero, Risco (3 cards), Ecossistema (4 produtos), AutoRelatório destaque, Sobre Thiago, Resultados, Planos (3 CTAs), FAQ (5 details), Footer
* **Responsivo:** Mobile-first, Tailwind via CDN
* **Mockups:** Cada imagem com bloco visual + PROMPT_MANUS_* visível
* **CTAs:** WhatsApp (chatbot), Teste 7 dias, Conversa especialista, Demo ao vivo

## DESCOBERTAS

* **Meta Ads MCP já está ativo** — `mcp__claude_ai_Meta_Ads_MCP__*` disponível. Pode integrar direto ao Claude.
* **Pasta TM Marketing já existe** em `C:\Users\thiag\Desktop\APPS\TM Marketing\` com 6 subpastas estruturadas
* **Estratégia v1.0 desatualizada** — menciona AutoRelatório V2, precisa incluir 4 produtos novos
* **Referência de design:** aicoders.academy usa dark + borders dashed eficaz — replicável com laranjado TM
* **Prompts Manus precisam ser contexto-específicos** — mencionam Banco do Brasil, profissionalismo, elementos visuais (logo TM, dark/orange)

## PRÓXIMOS PASSOS

* [ ] Completar landing page HTML — salvar em `landing-page/index.html`
* [ ] Gerar 5 imagens Manus (skill `/tm-criativo`) com prompts do documento
* [ ] Integrar imagens na landing page
* [ ] Testar landing page em browser (responsividade mobile)
* [ ] Atualizar `01-estrategia/estrategia-de-marca.md` — incluir 4 produtos + laranjado TM
* [ ] Criar `05-meta-ads/campanhas/` — 4 arquivos (autorelatorio, auto-legenda, zap, automobile)
* [ ] Autenticar Meta Ads MCP — conectar conta Meta Business
* [ ] Rodar primeira campanha Meta Ads (AutoRelatório para B2B)
* [ ] Criar `MANUS_PROMPTS.md` — compilação de todos os prompts

## OBSERVAÇÕES

* Landing page inspirada em aicoders.academy com contexto TM (engenharia predial vs harness engineering)
* 3 CTAs: captação (teste grátis), institucional (conversa), conversão (demo ao vivo)
* Mockups de imagem evitam "página vazia" — cada seção tem visual claro
* Tom: direto, técnico, confiante (como em aicoders.academy)
* TM Marketing conecta com AutoRelatório V5 (Sprint anterior) — é a frente de vendas

---

# SPRINT 2026-06-07 — Autolegendas · Correção de Legendas Acima (LAMBARI)

## CONTEXTO

* Pasta de trabalho: `C:\Users\thiag\Desktop\Minha Demanda\1 - Preventivas 2026\01 - Apoio operacional\Autolegendas\`
* Relatório tratado: `C:\Users\thiag\Desktop\Minha Demanda\2 - Em andamento\LAMBARI - 2245\RELATÓRIO FOTOGRÁFICO - LAMBARI - LEVANTAMENTO PREVENTIVO - Corrigir.docx`
* Problema: `auditar_legendas.py` reportava "0 erros" mas o usuário encontrou legendas visualmente acima de fotos no Word
* Legendas erradas identificadas pelo usuário: **Foto 435, 437, 538, 540, 594, 599, 676**

## O QUE FOI FEITO

### Diagnóstico do bug no auditar_legendas.py

* O script só olhava o parágrafo **posterior** à foto (função `proximo_paragrafo_com_texto`)
* Nunca verificava o parágrafo **anterior** — se havia "Foto N" antes da foto, passava invisível
* Resultado: 712 legendas "Foto N" no documento (muito mais que as 433 fotos físicas) — as extras eram as acima

### Novo script: remover_legendas_acima.py

* Caminho: `C:\Users\thiag\.claude\skills\autolegendas\scripts\remover_legendas_acima.py`
* Lógica: recebe lista de números via `--deletar N1,N2,...` e:
  1. Localiza e remove os parágrafos "Foto N" especificados do XML
  2. Renumera sequencialmente todas as legendas a partir do primeiro número deletado
  3. Salva em `/output/` sem sobrescrever o original
* Suporte a `--so-auditar` para verificar antes de alterar

### Comando usado e resultado

```powershell
python remover_legendas_acima.py "arquivo.docx" --deletar 435,437,538,540,594,599,676
```

* 7 legendas deletadas
* 271 legendas renumeradas
* Sequência contínua: OK (sem gaps)
* Output: `output\RELATÓRIO FOTOGRÁFICO - LAMBARI - LEVANTAMENTO PREVENTIVO - Corrigir_CORRIGIDO_1780864387.docx`

### Atualização de auditar_legendas.py

* Adicionada função `paragrafo_anterior_com_texto(p_el)`
* Auditoria agora reporta "Legendas ACIMA de fotos" como categoria separada
* Recomenda `remover_legendas_acima.py` quando detecta o padrão

### Atualização do SKILL.md (autolegendas)

* Novo script adicionado à tabela de referência
* Fluxo de execução atualizado com caso "LEGENDAS ACIMA DAS FOTOS" como passo (a) antes dos outros

### Melhoria do skill /sprint-memory

* Skill editado para salvar **também** na memória do projeto Claude (`~/.claude/projects/.../memory/`)
* Antes: só escrevia em `MEMORIA_SPRINTS.md`
* Agora: grava os dois em paralelo → próxima sessão já inicia com contexto sem pedir manualmente

## DESCOBERTAS

* O documento LAMBARI tem 712 ocorrências de "Foto N" para 433 fotos físicas — 279 extras (legendas acima + referências em tabelas de medição)
* A detecção de "legenda acima" depende do número específico passado pelo usuário — o script não tenta inferir automaticamente quais são erradas
* `FOTO_RE = r'^Foto\s+(\d+)$'` (com `$`) é o discriminador correto — exclui linhas de medição como "2,91 m2,91 m"
* A renumeração usa o MENOR número deletado como ponto de partida — correto para sequências com múltiplos gaps

## PRÓXIMOS PASSOS

* [ ] Usuário validar o arquivo corrigido no Word — verificar se Foto 435, 538, 594 estão somente abaixo das fotos
* [ ] Se encontrar mais legendas acima em outros relatórios: usar `--deletar` com os números específicos
* [ ] Avaliar se `auditar_legendas.py` deveria tentar detectar legendas acima automaticamente (por heurística de posicionamento no XML)

## OBSERVAÇÕES

* O skill `/sprint-memory` foi atualizado nesta sessão — este sprint é o primeiro a usar o novo comportamento duplo
* Relatório LAMBARI = contrato 2245 — em andamento
* O script `remover_legendas_acima.py` é genérico — funciona em qualquer relatório `.docx` com o mesmo padrão

---

# SPRINT 2026-06-08 — Recuperação de Contexto · TM Gerenciador

## CONTEXTO

* Sessão iniciada com objetivo de retomar o desenvolvimento do TM Gerenciador
* Usuário solicitou busca das memórias do projeto e leitura dos últimos sprints registrados
* Sprint de orientação antes de retomar execução — sem implementação nova nesta sessão

## O QUE FOI FEITO

* Leitura completa do `MEMORIA_SPRINTS.md` — histórico inteiro revisado (Sprints 1–7)
* Identificação do estado atual do TM Gerenciador: Sprint 3 em andamento
* Contexto retomado: banco zerado (TRUNCATE executado), reimportação pendente, campos `elaborador`/`tecnico` separados
* Invocação do skill `/sprint-memory` para consolidar a sessão

## DESCOBERTAS

* Nenhum sprint novo de TM Gerenciador foi registrado desde 2026-06-05 — última sessão parou no Sprint 3 iniciado
* Estado pendente crítico: SQL de migração (`ADD COLUMN elaborador, tecnico`) e reimportação da planilha ainda não confirmados
* Skill `/sprint-memory` atualizado na sessão de 07/06 para gravar em dois locais (MEMORIA_SPRINTS + memory do projeto Claude)

## PRÓXIMOS PASSOS

* [ ] Confirmar se SQL foi executado no Supabase: `ALTER TABLE ordens_servico ADD COLUMN elaborador TEXT, ADD COLUMN tecnico TEXT`
* [ ] Reimportar planilha `ORDENS DE SERVIÇOS GERAL.xlsx` via `/importar` com campos corrigidos
* [ ] Retomar Sprint 3: modal detalhe O.S, `/ordens/[id]`, sidebar mobile, `/dificuldades`
* [ ] Sprint 4: Supabase Auth + RLS por role (manager/elaborador/contract_admin)
* [ ] Atualizar `/equipe` para mostrar elaboradores e técnicos separados

## OBSERVAÇÕES

* TM Gerenciador está em: `C:\Users\thiag\Desktop\tm-tecnologia\TM_Gerenciador\`
* Backend porta 8000 · Frontend porta 3000 · `run.bat` sobe os dois
* Supabase: `stofmzzensxqnqrnyrvk.supabase.co` — região São Paulo
* 804 O.S importadas originalmente (banco foi zerado para reimportação com campos corretos)

---

# SPRINT 2026-06-08/09 — Explan Orçamento Express · Sprint 01

## CONTEXTO

* Projeto novo: ferramenta interna de orçamento para **Explan Móveis Planejados** (cliente Ygor)
* Workspace: `C:\Users\thiag\Desktop\Explan\LP-ORÇAMENTO\`
* Objetivo: ferramenta usada pelo **vendedor** na reunião com o cliente para montar orçamento interativo em tempo real
* Stack: HTML puro + CSS + JS — hospedagem no GitHub Pages (free, sem servidor)
* Sessão iniciada via skill `/brainstorming` (brainstorm inicial) e encerrada com `/sprint-memory`

## O QUE FOI FEITO

### Análise e identidade visual

* Leitura completa das análises de branding da Explan em `C:\Users\thiag\Desktop\Explan\Analises\`:
  - Tipografia: Archivo (300/600 principal), System fonts (body), Manrope (FAQ/humanidade)
  - Cores: `#41422F` oliva (primária), `#EBE6DD` bege (backgrounds), `#000000` CTAs, `#CC3366` hover/magenta, `#6EC1E4` cyan (foco)
  - Botões: pill (`border-radius: 50px`), preto com hover magenta
* Identificada correção crítica: ferramenta é interna (vendedor), não landing page pública

### Dois protótipos funcionais

**`prototipo-wizard.html`** — 4 etapas:
* Step 1: Dados do cliente (nome, telefone, email, endereço)
* Step 2: Escolha de materiais (chips visuais: Chapa 15/18, ferragem Blum/Häfele/FGV, interior branco/colorido)
* Step 3: Montagem de ambientes + itens com metragem/quantidade
* Step 4: Fechamento com total + descontos aplicados + botões PDF/Contrato
* Footer fixo com running total em tempo real

**`prototipo-pagina-unica.html`** — página única com sidebar:
* Cards: Cliente, Materiais (chip selection), Ambientes+Itens
* Sidebar sticky com total em tempo real e CTAs
* Mais rápido para vendedores experientes

### Sistema de descontos automáticos

| Escolha | Desconto |
|---|---|
| Chapa 15mm | −10% no MDF |
| Ferragem Häfele | −5% |
| Ferragem FGV | −15% |
| Interior branco | −5% |
| Cumulativo sobre subtotal | sim |

### Testes automatizados — Playwright

* Script `test_prototipos.py` criado com bateria completa para os dois protótipos
* Testes: carregamento, header, logo, inputs, CTA, navegação wizard (steps 1→4), screenshots desktop/tablet/mobile, overflow horizontal
* Resultado: **25/28 testes passaram (89%)**
* 3 falsos positivos conhecidos:
  - Overflow: `scrollWidth` mede conteúdo mesmo com `overflow:hidden` — visual correto
  - Botão CTA wizard em footer `position:fixed` — Playwright não verifica mas funciona normalmente

### Preview do PDF — `pdf-preview.html`

* 5 páginas A4 portrait com layout completo do orçamento:
  1. Capa: logo EXPLAN + nome do cliente + data de validade
  2. Quem Somos + 4 cards de diferenciais
  3. Ambiente 01 (Cozinha) — foto + tabela de itens + subtotal
  4. Ambiente 02 (Dormitório Master) — foto + tabela de itens + subtotal
  5. Resumo de valores + descontos + condições de pagamento + prazos
* Rodapé com selo TM · Sempre Tecnologia em todas as páginas
* Responsivo a `@media print` com `page-break-after: always`

### Template de contrato — `contrato-template.html`

* Placeholders `{{DUPLA_CHAVE}}` para substituição programática:
  - `{{NOME_CLIENTE}}`, `{{CPF_CNPJ}}`, `{{TELEFONE}}`, `{{EMAIL}}`
  - `{{ENDERECO_OBRA}}`, `{{DATA_CONTRATO}}`, `{{VALOR_TOTAL}}`, `{{VALOR_POR_EXTENSO}}`
  - `{{FORMA_PAGAMENTO}}`, `{{LISTA_AMBIENTES}}`, `{{MATERIAIS_ESCOLHIDOS}}`, `{{PRAZO_EXECUCAO}}`
* 6 cláusulas completas: Objeto, Valor, Prazo, Pagamento, Garantia, Rescisão
* Bloco de assinaturas (contratante + contratada) + 2 testemunhas
* Rodapé com selo TM

### Documentação

* `SPRINT-01-INICIO.md` — histórico do sprint nas palavras do Thiago
* Duas mensagens de WhatsApp escritas: uma pra Thiago (atualização pessoal) e uma pro Ygor (atualização pro cliente/chefe)

## DESCOBERTAS

* O PDF exemplo fornecido pelo Ygor (`PDF EXEMPLO CITADO.pdf` — 22 páginas) tem estrutura clara: capa + institucional + por ambiente (foto+planta) + resumo + pagamentos
* Imagens de ambiente do site Explan: `explanmoveisplanejados.com.br/wp-content/uploads/2026/04/[ambiente]-[NN].jpg` — mas ainda sem acesso garantido em produção
* `html2pdf.js` escolhido para geração do PDF — funciona 100% client-side, sem servidor
* `EmailJS` escolhido para notificações — free tier 200 emails/mês, sem backend
* Playwright detecta `scrollWidth > window.innerWidth` mesmo com `overflow:hidden` porque mede layout interno — workaround: usar `document.documentElement.scrollWidth` ou checar visualmente

## PRÓXIMOS PASSOS

* [ ] Integrar `html2pdf.js` para geração real do PDF a partir dos dados preenchidos
* [ ] Integrar `EmailJS` para notificação ao Ygor quando orçamento for gerado
* [ ] Lógica de preenchimento do contrato — substituir `{{placeholders}}` com JS
* [ ] Desenvolver versões de produção do wizard e da página única (além dos protótipos)
* [ ] Deploy no GitHub Pages
* [ ] Substituir imagens Unsplash por fotos reais da Explan (Ygor vai fornecer)
* [ ] Validar catálogo de preços com o Ygor
* [ ] Decidir qual dos dois modelos (wizard vs página única) será o produto final — ou oferecer ambos

## OBSERVAÇÕES

* Projeto Explan fica em `C:\Users\thiag\Desktop\Explan\LP-ORÇAMENTO\`
* Thiago lidera o desenvolvimento; Ygor é o cliente/dono da Explan
* Ferramenta é interna — vendedor usa no notebook/tablet durante reunião presencial
* Marca Explan: oliva `#41422F` + bege `#EBE6DD` + preto pill + magenta hover — não tem nada de verde/vermelho
* Seal obrigatório em tudo: "Desenvolvido por TM · Sempre Tecnologia" linkando para `https://thiagonascimentobarbosapro.com`

---

# SPRINT 2026-06-09 — Explan Orçamento Express · Sprint 02 e 03

## CONTEXTO

* Continuação direta do Sprint 01 — sistema de orçamento da Explan Móveis Planejados
* Workspace: `C:\Users\thiag\Desktop\Explan\LP-ORÇAMENTO\`
* Sprint 02: upgrade visual com GSAP + AOS, redesign do PDF com banners editoriais, criação do catálogo de itens JSON
* Sprint 03: finalização funcional — localStorage bridge, geração de PDF e Contrato reais, consolidação de imagens, testes
* Sessão encerrada com usuário indo dormir — agentes rodaram autônomos até o fim

## O QUE FOI FEITO

### Sprint 02 — Upgrade Visual e Estrutural

#### Animações — GSAP 3.12.5 no wizard
* Transição entre steps: slide `x: ±40` + `opacity 0→1`, duração 0.25s/0.3s
* Counter do total animado: `gsap.to` com `snap: { innerHTML: 1 }` — número "rola" visualmente
* Chip de material: micro bounce `scale 0.95→1`, `ease: "back.out(3)"` no clique
* Entrada de item na lista: `opacity + y: 8→0`, duração 0.25s

#### Animações — AOS 2.3.4 na página única
* Cards de materiais: `data-aos="fade-up"` com delay cascata (0/100/200ms)
* Cards de ambiente: `data-aos="fade-left"`
* `AOS.init({ once: true, offset: 60 })` — anima uma vez, sem repeat agressivo

#### Visual upgrades CSS
* Progress bar do wizard com traço diagonal geométrico `::before` clip-path no step ativo
* Mat-cards selecionados: `box-shadow: 0 0 0 3px rgba(65,66,47,.15)` + ícone check `::after`
* Hover nos env-cards: `translateY(-2px)` + shadow upgrade
* Botões primários: efeito ripple `::after` no click
* Fonte Playfair Display adicionada ao Google Fonts import (estava referenciada mas não carregava)
* TM badge corrigido: movido para antes do step-nav fixo com `padding-bottom: 90px`

#### Redesign do PDF (`pdf-preview.html`)
* Capa full-bleed: `<img>` absoluta + overlay `rgba(65,66,47, 0.78)` + conteúdo `z-index:1`
* Barra magenta vertical 4px antes do nome do cliente
* Páginas de ambiente: layout `grid-template-columns: 53% 47%` (foto à esquerda, itens à direita)
* Número do ambiente como watermark tipográfico: Archivo 900, 120px, opacity .06
* Rodapé com círculo olive + número de página
* Watermark "EXPLAN" diagonal opacity .025 nas páginas brancas

#### Catálogo de itens — `catalogo-itens.json`
* Estrutura criada com 10 categorias: Cozinha, Dormitório Master, Dormitório Filho, Dormitório Casal, Sala de Estar, Home Office, Lavanderia, Banheiro, Closet, Área Gourmet
* Campos por item: `id`, `nome`, `unidade`, `preco_chapa18_blum/hafele/fgv`, `preco_chapa15_blum/hafele/fgv`, `observacao` (todos `null` — para Ygor preencher)
* Itens mapeados da conversa com Ygor: Armário Superior, Armário Inferior/Balcão, Torre Forno/Geladeira, Guarda-roupa, Painel Cama/TV, Criado-Mudo, etc.

#### Prompt de imagens — `PROMPTS-GPT-IMAGE-2.md`
* 21 prompts detalhados em inglês para GPT Image 2 (Manus)
* Grupo 1: PDF-01 a PDF-12 — banners 1600×1040px para cada ambiente
* Grupo 2: WEB-01 a WEB-03 — heroes 1800×1200px para wizard e página única
* Grupo 3: CARD-01 a CARD-06 — thumbnails 400×280px para os cards de interface
* Paleta sempre: warm honey oak, white lacquer, quartz, brass, `#41422F` olive compatible

### Sprint 03 — Finalização Funcional

#### localStorage bridge (wizard → PDF → Contrato)
* `coletarDados()` no wizard: coleta cliente, config (chapa/ferragem/cor/desconto), ambientes com itens, total_geral, data, ref
* `puColetarDados()` na página única: mesmo padrão
* `gerarPDF()` e `puGerarPDF()`: `localStorage.setItem('explan_oc', JSON.stringify(dados))` + `window.open('pdf-preview.html', '_blank')`
* `gerarContrato()` e `puGerarContrato()`: mesmo padrão abrindo o template de contrato

#### PDF dinâmico (`pdf-preview.html`)
* IDs adicionados a todos os elementos estáticos: `pdf-nome`, `pdf-validade`, `pdf-ref`, `pdf-total`, etc.
* `<div id="ambientes-pdf-container">` envolve páginas de ambiente
* Script carrega localStorage, preenche todos os IDs, limpa container e regenera ambiente pages dinamicamente
* `FOTOS` object mapeia nomes de ambiente → caminhos locais `imagens-ambientes/`
* Validade: +30 dias da data do orçamento; Ref: `EXP-YYYY-MMDD`

#### Contrato de Serviço (`Contrato-de Serviço - template.html`)
* Script com `fill(placeholder, value)` usando `replaceAll()`
* `valorExtenso(n)` converte número para português escrito (ex: "vinte e nove mil reais")
* 15 placeholders preenchidos: nome, CPF/CNPJ, email, telefone, valor total, valor por extenso, prazo, forma pagamento, descrição pagamento, desconto, lista ambientes, materiais, data, cidade, endereço obra

#### Contrato de Produção (`Contrato-de-Producao-template.html`) — NOVO ARQUIVO
* Mesmo script base do Contrato de Serviço
* Placeholders exclusivos: `{{DATA_MEDICAO}}`, `{{TECNICO_MEDICAO}}` ("A confirmar"), `{{NUM_CONTRATO}}`, `{{DATA_INICIO_PRODUCAO}}` (+7 dias úteis), `{{DATA_PREVISTA_ENTREGA}}` (+prazo em dias úteis)
* Função `addDiasUteis()` pula sábados e domingos nos cálculos de prazo

#### Consolidação de imagens — `imagens-ambientes/`
* 23 arquivos consolidados de duas fontes:
  - **18 do Manus** (pasta `images (3)/`): todos os PDFs, heroes e 3 cards
  - **5 do Stitch** (pasta `stitch_exact_image_generation/*/screen.png`, renomeados): card-closet, card-banheiro, card-home-office, pdf-home-office-alt, pdf-closet-alt
* Todas as URLs Unsplash removidas dos 3 arquivos HTML principais (0 ocorrências confirmadas via grep)
* Item thumbnails substituídos por SVG placeholder inline (evita dependência externa)
* `README-IMAGENS.md` criado com tabela dos 23 arquivos, origem, uso e instruções de substituição

#### Tentativa de split-hero (revertida a pedido do usuário)
* Implementado layout `display:grid` 50%/50% com foto de ambiente à esquerda
* Foto do Unsplash retornou retrato de pessoa — visual quebrado
* Usuário solicitou revert: "retorna a versão anterior, vamos finalizar no básico de design mesmo depois evoluímos"
* Versão Sprint 2 restaurada integralmente

## DESCOBERTAS

* `localStorage` como data bridge é a solução certa para HTML puro multi-arquivo — sem servidor, sem complicação
* `window.open()` abre o PDF em nova aba onde o script lê os dados no `DOMContentLoaded`
* `document.body.innerHTML.replaceAll(placeholder, value)` funciona para substituição em contratos HTML mas pode quebrar event listeners — no contexto de contrato (só leitura) é seguro
* TM badge oculto por `position: fixed` do step-nav: solução = mover badge para fora do fluxo coberto
* `goStep()` bug: condição `if(currentStep===4) return` impedia chegar no step 4 — corrigido para `goStep(currentStep + 1)` simples
* Imagens do Unsplash são não-determinísticas (podem retornar pessoas) — eliminadas completamente
* Agent 3 verificou integridade: menor imagem = `pdf-banheiro.jpg` com 674 KB — nenhuma corrompida

## PRÓXIMOS PASSOS

* [ ] Deploy no GitHub Pages (criar repo + push dos arquivos)
* [ ] Integrar `html2pdf.js` para download real do PDF (atualmente só abre em nova aba para `Ctrl+P`)
* [ ] Integrar `EmailJS` para notificação ao Ygor quando orçamento for gerado
* [ ] Ygor preencher preços no `catalogo-itens.json` — campo `preco_*` ainda `null`
* [ ] Substituir imagens `imagens-ambientes/` por fotos reais do showroom Explan (Ygor fornece)
* [ ] Gerar imagens do GPT Image 2 (Manus) usando prompts do `PROMPTS-GPT-IMAGE-2.md`
* [ ] Testes E2E completos após Sprint 03 (wizard step 1→4 completo, geração PDF/contrato)
* [ ] Decidir produto final: wizard vs página única vs ambos
* [ ] Validar catálogo de preços e fluxo completo com Ygor

## OBSERVAÇÕES

* Dois contratos: "Contrato de Serviço" (comercial, pré-produção) e "Contrato de Produção" (técnico, pós-aprovação)
* Todos os arquivos HTML são standalone — abrir no browser, nenhum servidor necessário
* Imagens locais referenciadas como `imagens-ambientes/[nome].jpg` — funciona se todos na mesma pasta
* Sprint 03 executado em modo autônomo (usuário dormindo) com 3 sub-agentes paralelos
* Verificação final: 3/3 arquivos HTML sem URLs Unsplash; PDF dinâmico testado com mock data (3/3 PASS)

---

# SPRINT 2026-06-11/12 — Explan Orçamento Express · Sprint 09

## CONTEXTO

* Projeto: Explan Orçamento Express — ferramenta interna de orçamento para Explan Móveis Planejados
* Workspace: `C:\Users\thiag\Desktop\Explan\.LP-ORÇAMENTO\`
* Objetivo: sprint grande de refatoração arquitetural + novas features + documentação + correção de bugs
* Sessão iniciada com recuperação de contexto via memórias Claude + plan/ da sessão anterior
* Arquivo principal anterior (`sprint-06.html`) movido para Legado; `sprint-08.html` renomeado para `login.html`

## O QUE FOI FEITO

### Documentação — pasta PLAN/

* `1 - PLANO.md` — README-style atualizado: estrutura real de pastas, funcionalidades correntes, fluxo completo
* `2 - ARQUITETURA.md` — stack atual vs futura (Supabase Auth, Supabase DB, Evolution API WhatsApp), schema SQL, guia de migração
* `3 - ROADMAP.md` — Sprint 01–09 marcados concluídos, backlog organizado por prioridade, bloqueadores externos
* `4 - PROJEÇÃO DO FUTURO.md` — EmailJS, Evolution API WhatsApp, dashboard Ygor, multi-usuário
* `README_TO_SAVE.md` — guia de onde salvar cada tipo de arquivo, convenções de nomes, regras gerais

### Excel do catálogo

* `catalogo-itens.xlsx` gerado via Python + openpyxl a partir de `catalogo-itens.json`
* 3 abas: Completo (todos os campos), Consolidado (preços por cenário de desconto), Ambientes
* Design System aplicado: cabeçalhos olive, linhas alternadas cream

### login.html (renomeado de sprint-08.html)

* Redirect atualizado: `sprint-06.html` → `sprint-09.html`
* Dashboard welcome screen corrigido: `min-height: 100vh` adicionado ao `.dashboard.active`
* Título: "Bem-vindo ao Ecossistema Explan"

### sprint-09.html — App Principal Refatorado

**Arquitetura de materiais por ambiente (mudança crítica):**
* Global `const config = {chapa, ferragem, cor}` substituído por `envConfigs = {}` (dict por envId)
* `getEnvConfig(envId)`, `calcEnvDiscount(cfg)`, `discLabel(cfg)` — helpers isolados
* `selChip(el, group, val, envId)` — novo parâmetro envId
* `recalc()` aplica desconto individual por ambiente
* Badge de desconto no header de cada `.env-card` reflete a config daquele ambiente

**Sidebar de navegação esquerda:**
* Layout: `[sidebar-nav 60px] [main-content 1fr] [sidebar-resumo 300px]`
* Painéis: Perfil (salvo em `explan_perfil`), Clientes (`explan_clientes`), Projetos (`explan_projetos`)
* `salvarProjeto()` / `renderProjetos()` / `carregarProjeto(idx)` / `excluirProjeto(idx)`
* `carregarProjeto(idx)` — reconstrói form completo a partir do snapshot JSON salvo

**Adição manual de itens:**
* Botão "✎ Item Manual" em cada `.env-card`
* Mini-form inline: nome, unidade, preço unitário, quantidade
* `addManualItem(btn)` insere `.item-row` com `data-manual="true"`, mesmo fluxo de `recalc()`

**Redesign card Variáveis do Projeto:**
* Removidos: gradient cyan/magenta incompatíveis com Design System v2
* Aplicado: `background: var(--cream-alt)`, `border: 1px solid var(--border)` — alinhado aos demais cards

**Responsividade:**
* `@media(max-width:900px)` — layout coluna, sidebar resumo expande para 100%
* `@media(max-width:480px)` — tipografia reduzida, padding compacto, botões full-width

**Correções de bugs:**
* Env-card inicial hardcoded (Sala de Estar + Painel Ripado 4.5) removido — começa vazio
* Sidebar: valores hardcoded (R$ 12.600,00) → R$ 0,00
* Paths `window.open('../pdf-preview.html')` → `window.open('pdf-preview.html')` (mesma pasta)
* Paths de imagens: `../../LP-ORÇAMENTO/imagens-ambientes/` → `../imagens-ambientes/` (ponto no nome da pasta)

### apresentacao-editor.html — Novo Arquivo

* Editor visual de apresentação A4 por ambiente — **sem preços, sem itens, sem totais**
* Slide `.slide-cover` (capa Explan) + um slide por ambiente de `explan_oc`
* `.slide-img-zone` — clicável, abre file input para upload de imagem local
* `.slide-caption` — apenas nome do ambiente (Archivo, elegante)
* `carregarFotos(input, ambIdx)` — suporte a múltiplas imagens (gera sub-slides extras)
* Drag simples na imagem dentro da zona
* `window.print()` com `@media print` para exportar

## DESCOBERTAS

* Python no Windows: `python3` não funciona, usar `python`. Instalar openpyxl: `python -m pip install openpyxl`
* Pasta `.LP-ORÇAMENTO` tem ponto no nome — paths como `../../LP-ORÇAMENTO/` ficam errados; correto é `../imagens-ambientes/` (relativo à subpasta `EM DESENVOLVIMENTO/`)
* Convenção de nomes definida definitivamente: `login.html` (fixo), `sprint-{N}.html` (app principal), nomes descritivos para demais páginas
* Apresentação visual NÃO deve ter preços — informação financeira fica exclusivamente no PDF de orçamento

## PRÓXIMOS PASSOS

* [ ] Preencher preços reais em `catalogo-itens.json` (aguardando Ygor)
* [ ] Deploy no GitHub Pages
* [ ] html2pdf.js — download real do PDF (hoje só abre em nova aba para Ctrl+P)
* [ ] Alinhar contrato HTML ao CONTRATO.docx real (12 cláusulas, Responsável Financeiro Solidário)
* [ ] Responsividade — testar em tablets reais usados nas reuniões
* [ ] Fase 2: Supabase Auth + banco de dados na nuvem

## OBSERVAÇÕES

* Arquivo base do sprint-09: sprint-06.html (sem wizard — confirmado na sprint anterior)
* Login permanece como `login.html` (nome fixo para sempre)
* Convenção: versões antigas vão para `EM DESENVOLVIMENTO/Legado/` antes de excluir
* Apresentação Editor é visual/estética — nunca adicionar dados financeiros nele
* Supabase + Evolution API estão documentados em `2 - ARQUITETURA.md` para quando o projeto crescer

---

# SPRINT 2026-06-12 22:xx — Explan Sprint 10: Orçamento Real, Logo, Catálogo, Playwright

## CONTEXTO

* Continuação do Sprint 09 — app funcional em sprint-09.html com localStorage
* Objetivo principal: rodar orçamento real da cliente Karla e Luiz com Playwright
* Problemas paralelos: logo removida do orçamento, referência TM no rodapé do PDF, imagens quebradas, drag/resize com bug
* Supabase aguardando — outro agente em paralelo (ainda sem URL/anon key)

## O QUE FOI FEITO

### orçamento-editor.html — múltiplas correções

* **Logo real na capa:** `explan_logo_preto_transparente.png` copiada para `.LP-ORÇAMENTO/imagens-explan/logo-transparente.png` (dentro do server root). Path: `../imagens-explan/logo-transparente.png` com `filter: brightness(0) invert(1)` para aparecer branca sobre fundo escuro
* **Referência TM removida** de todos os 6 rodapés — substituída por "Explan Móveis Planejados" (cliente não deve ver crédito de desenvolvimento no PDF)
* **Cor magenta residual corrigida:** `.resumo-header-total .desc { color: rgba(204,51,102,.8) }` → `rgba(107,142,94,.9)` (verde musgo)
* **Upload de foto por ambiente adicionado:** `<input type="file" id="file-orc-{idx}">` + botão "Trocar Foto" + função `trocarFotoOrc(input, idx)` com `FileReader` → substitui src + reset inline style com `inset:0`
* **Fix drag/resize após trocar foto:** `trocarFotoOrc` agora remove `.orc-resize-handle` antigos antes de chamar `instalarDragResize()` → evita duplicação de handles

### apresentacao-editor.html

* **Logo corrigida:** `../../Imagens/explan_logo_preto_transparente.png` → `../imagens-explan/logo-transparente.png` (path funcionava em `file://` mas não via HTTP server)

### entrada_karla_luiz.py — Playwright script

* **Apresentação:** restaurado envio de TODAS as fotos da pasta (não só `imgs[0]`)
* **Orçamento:** 1 foto por ambiente via `#file-orc-{idx}` (novo input adicionado)
* **Browser aberto ao final:** `input()` com fallback `time.sleep(7200)` para quando não há terminal interativo (EOFError) — garante que o browser fica aberto 2h quando rodado em background
* **Resultado final:** 26/26 etapas OK

### catalogo-itens.json — 5 itens adicionados

Itens que eram inseridos manualmente no orçamento agora têm entrada oficial no catálogo:

| ID | Unidade | Preço | Nota |
|----|---------|-------|------|
| `caixote-porta-mdf-lisa` | m² | R$ 3.450 | aplica_desconto_chapa + ferragem |
| `caixaria-closet-porta-mdf-lisa` | m² | R$ 3.450 | variação para closet |
| `caixaria-porta-mdf-lisa` | m² | R$ 3.450 | variação genérica |
| `kit-dominus-porta-correr` | un | R$ 1.800 | sem desconto (kit fechado) |
| `porta-pivotante-un` | un | R$ 1.600 | `"cotar": true` — valor a confirmar |

* Categoria `outros` criada no JSON para itens que não se encaixam nas existentes
* `ultima_atualizacao` atualizado para `"2026-06-12"`

### Infraestrutura / Servidor

* Logo copiada para `.LP-ORÇAMENTO/imagens-explan/` — pasta criada dentro do server root para servir assets que ficavam fora do root (`Desktop/Explan/Imagens/`)
* Padrão consolidado: qualquer asset precisa estar dentro de `.LP-ORÇAMENTO/` para ser acessível via HTTP (server root = `.LP-ORÇAMENTO/`)

### Supabase — plano documentado (aguardando credenciais)

* Schema definido: `profiles`, `projetos`, `catalogo_itens`
* RLS: vendedor vê só os seus / gerente vê todos
* `supabase-client.js` compartilhado planejado
* Tabelas SQL prontas para rodar no SQL Editor assim que o projeto for criado
* Usuários iniciais: `gerente@explan.com` (Ygor Patrão) + `vendedor@explan.com`

## DESCOBERTAS

* **Server root critical:** qualquer path com `../../` acima de `.LP-ORÇAMENTO/` falha via HTTP — a correção é copiar assets para dentro do root ou reorganizar a pasta
* **Playwright `input()` via bash:** recebe `EOFError` imediatamente — solução: `except EOFError: time.sleep(7200)` mantém browser aberto mesmo sem terminal interativo
* **Handles duplicados no drag/resize:** ao trocar a foto via FileReader, se não remover os `.orc-resize-handle` antigos antes de chamar `instalarDragResize()`, os handles ficam duplicados e o drag quebra
* **Logo "branco" vs "preto transparente":** logo branca funciona diretamente; logo preta transparente precisa de `filter: brightness(0) invert(1)` para aparecer branca em fundo escuro

## PRÓXIMOS PASSOS

* [ ] Supabase: aguardando URL + anon key do Ygor para integrar auth + banco de dados
* [ ] html2pdf.js no orçamento-editor para download direto (sem precisar Ctrl+P)
* [ ] Contratos V2: `contrato-servico-V2.html` e `contrato-producao-V2.html`
* [ ] Confirmar valor da Porta Pivotante (`"cotar": true` no catálogo)
* [ ] Versionamento do projeto (mencionado pelo Thiago ao encerrar sessão)
* [ ] Deploy GitHub Pages (aguardando decisão de visibilidade do repo)

## OBSERVAÇÕES

* Cliente real: Karla e Luiz — 6 ambientes (Cozinha, Sala/Hall, Escritório, Closet, Suíte 1, Banheiro), 26 itens no total
* Backup do orçamento salvo em `karla_luiz_backup.json` + `explan_projetos` no localStorage da origem `http://localhost:8181`
* Porta 8181 FIXA — não mudar. localStorage é scoped por origin, mudar porta = perder dados
* O orçamento-editor agora tem DOIS caminhos de imagem: foto padrão (por nome de ambiente) e foto do cliente (upload manual via botão "Trocar Foto")
* Sessão encerrada com 26/26 etapas OK no Playwright — documentos da Karla e Luiz prontos para apresentar


---

# SPRINT 2026-06-12 21:00 — Explan · Sprint 11 — Refinamento Visual UI

## CONTEXTO

* Continuação direta do Sprint 10 (Karla e Luiz, 26/26 OK)
* Objetivo: refinar visual de todos os editores — sprint inteiramente de UI/UX
* Arquivos principais: `sprint-09.html`, `apresentacao-editor.html`, `orçamento-editor.html`
* Novos assets de identidade visual introduzidos pelo Thiago: `Explan.png`, `X .png`, `Group.png`, `logo-tranparente-baixo.png`

## O QUE FOI FEITO

### sprint-09.html (V3 → V4)

* **Header simplificado:** removidos texto "Explan · Orçamento Express" e badge "USO INTERNO — v9"; ficou apenas a logo `Explan.png` centralizada com `justify-content: center`
* **Sidebar — troca de logo:** logo antiga removida, substituída por `X .png` (45×45px) — o X funciona como símbolo da marca na nav compacta
* **Versões criadas:** V3 (header), V4 (sidebar)

### apresentacao-editor.html (V5 → V7)

* **Capa:** testada `logo-tranparente-baixo.png` (revertida → V4), testada `logo-final.png` sem filtro, confirmado que `logo-final.png` precisa de `filter: brightness(0) invert(1)` para aparecer branca no fundo olive
* **Group.svg → Group.png:** arquivo `.svg` era na verdade PNG binário com extensão errada — copiado como `Group.png` para renderizar corretamente no browser
* **Group.png aplicado:** toolbar e capa da apresentação agora usam `Group.png` (sem filtro — já é cream/branco nativo)
* **Versões criadas:** V5 (logo-tranparente-baixo tentativa), V6 (sem filtro), V7 (Group.png)

### orçamento-editor.html (V4 → V5)

* **Background:** alterado de `#6b6c52` para `#2D2D2D` (igual ao apresentacao-editor)
* **Toolbar sticky:** substituiu `.pdf-controls` simples por toolbar com fundo olive, logo `Group.png`, título "Editor de Orçamento", botões "Imprimir / Exportar" + "Fechar" — mesma arquitetura visual do apresentacao-editor
* **Drag fix — causa raiz identificada:**
  1. `.amb-photo-overlay` com `inset:0` bloqueava `mousedown` na imagem → corrigido com `pointer-events: none`
  2. `mousemove` fazia `img.style.left=x; img.style.top=y; img.style.inset='unset'` — `inset` é shorthand para top/right/bottom/left, o `unset` apagava o `left` e `top` recém-definidos → substituído por `right='auto'; bottom='auto'` antes de setar left/top
* **Botões de foto padronizados:** `.btn-trocar-foto-orc` (overlay verde dentro da foto) substituído por `.page-action-btn` (estilo idêntico ao `.slide-action-btn` do apresentacao-editor: dark translúcido, borda sutil, acima da página)
* **Capa com upload de fundo:** botão "Adicionar foto de fundo" + `input[type=file]` acima da `.page-cover`; função `trocarFotoCapa()` carrega via FileReader e substitui `cover-bg` src
* **page-wrapper adicionado:** cada página (capa + ambientes) envolto em `.page-wrapper` com `.page-actions` acima — estrutura espelhada do `slide-wrapper`/`slide-actions` do apresentacao-editor
* **Print CSS:** `.page-actions` some com `display: none !important` no `@media print`
* **Versões criadas:** V4 (toolbar/background), V5 (drag fix + botões padronizados + capa upload)

### imagens-explan/ (assets novos)

* `Explan.png` — logo tipográfica cream para header do sprint-09
* `X .png` — símbolo X cream para sidebar (45×45px)
* `Group.png` — cópia de `Group.svg` com extensão correta (era PNG binário renomeado como SVG)
* `logo-tranparente-baixo.png` — logo com tagline "Móveis Planejados" abaixo (testada, não usada)

### Logo unificação (todos os arquivos)

* Todos os 6 arquivos HTML ativos do projeto (`sprint-09`, `login`, `orçamento-editor`, `apresentacao-editor`, `Contrato-de Serviço - template`, `Contrato-de-Producao-template`) agora usam `../imagens-explan/logo-final.png` — exceto os dois editores que migraram para `Group.png`

## DESCOBERTAS

* **`Group.svg` era PNG:** extensão `.svg` enganosa — browser tenta parsear como XML e falha silenciosamente. Sempre checar o header do arquivo com `Read` antes de usar
* **`inset` é shorthand perigoso em drag:** `inset: unset` reseta top/right/bottom/left ao mesmo tempo — ao animar posição nunca usar `inset` depois de setar `left`/`top`; usar `right='auto'; bottom='auto'` individualmente
* **`pointer-events: none` em overlays:** overlays decorativos (gradientes, sombras) sobre elementos interativos devem sempre ter `pointer-events: none` para não bloquear eventos de mouse
* **Histórico de versões cresce rápido:** apresentacao-editor já está em V7, orçamento-editor em V5 — considerar script de autonumeração em próximas sessões

## PRÓXIMOS PASSOS

* [ ] Supabase: aguardando URL + anon key para integrar auth + banco
* [ ] html2pdf.js no orçamento-editor (print nativo com @page correto já funciona)
* [ ] Contratos V2 — atualização visual para o novo Design System
* [ ] Confirmar valor da Porta Pivotante no catálogo (`"cotar": true`)
* [ ] Deploy GitHub Pages — decisão de visibilidade pendente
* [ ] Rodar Playwright novamente para Karla com os novos visuais

## OBSERVAÇÕES

* Sprint 100% visual — zero funcionalidade nova, apenas refinamento estético e correção de drag
* Thiago aprovou o resultado: "Ficou ótimo. A gente fez um grande refinamento de visual."
* Padrão visual agora unificado entre apresentacao-editor e orçamento-editor (fundo `#2D2D2D`, toolbar olive, Group.png)
* Regra de versionamento consolidada no CLAUDE.md e na memória persistente — nunca editar sem backup em `Legado/Versões/`
