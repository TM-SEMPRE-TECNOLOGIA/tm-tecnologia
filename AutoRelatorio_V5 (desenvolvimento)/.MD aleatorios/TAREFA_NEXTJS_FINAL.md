# 🚀 TAREFA: Portar App Real V5 para Next.js + React

**Para:** Agente "Add collapse arrow..."  
**De:** Thiago (você LEMBROU que não era para ser HTML, é um app REAL)  
**Tipo:** Refatoração crítica (HTML vanilla JS → Next.js com lógica integrada)  
**Tempo estimado:** 4-5 horas  
**Prioridade:** MÁXIMA  
**Status:** App HTML 100% funcional em `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\` — PRECISA VIRAR REACT

---

## 🎯 SITUAÇÃO ATUAL

**O app V5 JÁ EXISTE E FUNCIONA:**
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
├── index.html ........................ ✅ App completo, 100% funcional
├── app.js ........................... ✅ Toda a lógica vanilla JS
├── styles.css ....................... ✅ Design system com CSS variables
├── run.bat + run.py ................. ✅ Launcher criado
├── backend/ ......................... ✅ Engine dos 9 contratos já existe
└── .docs/
    └── wireframe_v5_overleaf(inspiração).html ... origem
```

**PROBLEMA:** É um app vanilla HTML/JS quando DEVERIA ser Next.js com React components.

**SOLUÇÃO:** Portar a lógica COMPLETA do app.js para React, estrutura em Next.js.

---

## 📋 O QUE PORTAR (Lógica Completa)

### Dados Globais
```javascript
// Estes vêm de app.js linhas 2-23
const CONTRACTS = [
  { id:'0908', name:'São José dos Campos', short:'SJC', mode:'sp', uf:'SP' },
  { id:'1507', name:'Cuiabá', short:'Cuiabá', mode:'trad', uf:'MT' },
  // ... 9 contratos total
];

const DESCS = {
  '1': 'Informamos que foi realizada visita técnica...',
  '2': 'No cumprimento das atividades...',
  // ... 4 descrições
};

let currentContract = CONTRACTS[2]; // 1565 default
let currentStep = 2;
let zoomScale = 0.9;
```

### Funções Críticas a Portar

| Função | Arquivo | Linhas | Tipo | Descrição |
|--------|---------|--------|------|-----------|
| `renderContractList()` | app.js | 26-38 | Render | Lista 9 contratos |
| `selectContract(id)` | app.js | 40-46 | Handler | Alterna contrato selecionado |
| `updateTopbar()` | app.js | 48-70 | Update | Atualiza topbar com contrato/modo |
| `liveUpdate()` | app.js | 83-120 | Sync | Sincroniza campos ↔ preview |
| `setStep(n)` | app.js | 123-142 | Nav | Navegação 3 steps |
| `nextStep() / prevStep()` | app.js | 144-145 | Nav | Botões prev/next |
| `zoom(delta)` | app.js | 148-153 | Preview | Zoom 50%-150% |
| `generateReport()` | app.js | 156-177 | Action | Simulação progresso geração |
| `showToast(msg)` | app.js | 180-187 | UI | Notificações toast |
| `toggleNavCollapse()` | app.js | 222-228 | UI | Collapse sidebar |
| `toggleDarkMode()` | app.js | 231-244 | Theme | Dark/light toggle com localStorage |
| `initDarkMode()` | app.js | 259-270 | Init | Restaurar tema em load |
| Resizable divider | app.js | 190-219 | Drag | Editor ↔ Preview redimensionável |

---

## 🏗️ ESTRUTURA NEXTJS FINAL

```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\frontend\
├── app/
│   ├── page.tsx ........................ (root layout + app)
│   ├── layout.tsx ..................... (html tag, providers)
│   └── globals.css ..................... (CSS variables + base styles)
│
├── components/
│   ├── TopBar.tsx ..................... (logo, contract selector, mode pill, buttons)
│   ├── Sidebar.tsx .................... (nav, contracts list, dark mode, settings)
│   ├── EditorPanel.tsx ................ (3 steps + form)
│   ├── PreviewPanel.tsx ............... (docx preview)
│   ├── ResizableDivider.tsx ........... (drag logic)
│   ├── Toast.tsx ...................... (notifications)
│   ├── ProgressOverlay.tsx ............ (generation progress)
│   └── hooks/
│       ├── useContracts.ts ............ (state + functions)
│       ├── useTheme.ts ................ (dark mode + localStorage)
│       └── useSteps.ts ................ (step navigation)
│
├── lib/
│   ├── contracts.ts ................... (CONTRACTS const)
│   ├── descriptions.ts ................ (DESCS const)
│   └── types.ts ....................... (IContract, etc)
│
├── styles/
│   ├── theme.css ...................... (CSS variables dark/light)
│   └── components.module.css .......... (component-specific styles)
│
├── public/
│   └── (assets se houver)
│
├── package.json ....................... (dependências)
├── next.config.js ..................... (config)
├── tsconfig.json ...................... (TypeScript)
└── .env.local .......................... (URLs etc)
```

---

## ✅ CHECKLIST DETALHADO

### FASE 1: Setup (30 min)
- [ ] Copiar V4 frontend de `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V4\APP\frontend`
- [ ] Colar em `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\frontend`
- [ ] `npm install` no novo frontend
- [ ] `npm run dev` — deve rodar sem erros em `localhost:3000`

### FASE 2: Constants & Types (30 min)
- [ ] Criar `lib/contracts.ts` com CONTRACTS array (copiar de app.js linhas 2-12)
- [ ] Criar `lib/descriptions.ts` com DESCS objeto (copiar de app.js linhas 14-19)
- [ ] Criar `lib/types.ts` com types:
  ```typescript
  interface IContract {
    id: string;
    name: string;
    short: string;
    mode: 'sp2' | 'sp' | 'trad';
    uf: string;
  }
  interface IFormData {
    nr_os: string;
    ag_cod: string;
    ag_nome: string;
    dt_atend: string;
    endereco: string;
    responsavel_dependencia: string;
    desc: '1' | '2' | '3' | '4';
  }
  ```

### FASE 3: Hooks (1h)
- [ ] **useContracts.ts**: State + functions
  ```typescript
  export function useContracts() {
    const [currentContract, setCurrentContract] = useState(CONTRACTS[2]);
    
    const selectContract = (id: string) => {
      const contract = CONTRACTS.find(c => c.id === id);
      if (contract) setCurrentContract(contract);
    };
    
    return { currentContract, selectContract, contracts: CONTRACTS };
  }
  ```

- [ ] **useTheme.ts**: Dark mode com localStorage
  ```typescript
  export function useTheme() {
    const [isDark, setIsDark] = useState(true);
    
    useEffect(() => {
      const saved = localStorage.getItem('theme') || 'dark';
      setIsDark(saved === 'dark');
      document.documentElement.className = saved === 'dark' ? '' : 'light-mode';
    }, []);
    
    const toggle = () => {
      const newState = !isDark;
      setIsDark(newState);
      localStorage.setItem('theme', newState ? 'dark' : 'light');
      document.documentElement.className = newState ? '' : 'light-mode';
    };
    
    return { isDark, toggle };
  }
  ```

- [ ] **useSteps.ts**: Step navigation
  ```typescript
  export function useSteps() {
    const [currentStep, setStep] = useState(2);
    const next = () => currentStep < 3 && setStep(currentStep + 1);
    const prev = () => currentStep > 1 && setStep(currentStep - 1);
    return { currentStep, setStep, next, prev };
  }
  ```

### FASE 4: Components (2h)
- [ ] **TopBar.tsx**: (app.js linhas 48-75)
  - Mostrar `currentContract.id`, `currentContract.name`, modo (SP2/SP/TRAD)
  - Botão "START" → call `iniciarApp()`
  - Botão "Novo" → `setStep(1)`
  - Botão "Gerar .docx" → `generateReport()`
  - Status "VISUALIZAÇÃO PRÉVIA" ← (ajuste crítico do outro agente)

- [ ] **Sidebar.tsx**: (app.js linhas 26-38, 222-228)
  - Mostrar lista CONTRACTS
  - Highlight selected
  - Dark mode toggle (lua/sol) ← `useTheme().toggle`
  - Settings button (engrenagem) → toast "em desenvolvimento"
  - Toggle collapse nav

- [ ] **EditorPanel.tsx**: (app.js linhas 123-142, 83-120)
  - **3 Steps bar** com progresso
  - **Step 1 (Cabeçalho):**
    - Campos: nr_os, ag_cod, ag_nome, dt_atend, endereco, responsavel, desc dropdown
    - Conectados a `liveUpdate()` (oninput)
  - **Step 2 (Estrutura):**
    - Placeholder para blocos (será preenchido depois)
  - **Step 3 (Gerar):**
    - Resumo dos dados
    - Botão "Gerar .docx"
  - Botões: Voltar, Próximo, Gerar

- [ ] **PreviewPanel.tsx**: (app.js linhas 148-153)
  - Docx preview skeleton
  - Zoom controls (+/-)
  - Zoom level display (50%-150%)
  - Live updates dos campos (flash animation)
  - Filename: `RELATÓRIO-{id}-{short}.docx`

- [ ] **ResizableDivider.tsx**: (app.js linhas 190-219)
  - Mouse drag logic
  - Min width: 300px, Max: app width - 300px
  - Highlight on active
  - Cursor col-resize during drag

- [ ] **ProgressOverlay.tsx**: (app.js linhas 156-177)
  - Progress bar 0-100%
  - Status messages
  - Triggered by generateReport()

- [ ] **Toast.tsx**: (app.js linhas 180-187)
  - Show messages com icon ✓
  - Auto-hide após 3.5s
  - Fade out animation

### FASE 5: Styling (45 min)
- [ ] Copiar CSS variables de `styles.css` para `app/globals.css`:
  ```css
  :root {
    --shell-bg: #111110;
    --shell-text: #EFEDE8;
    --orange: #C8541C;
    /* ... todo o resto */
  }
  html.light-mode {
    --shell-bg: #F8F7F4;
    /* ... light mode vars */
  }
  ```
- [ ] Adaptar estilos para Tailwind ou CSS modules
- [ ] Manter responsividade e animações

### FASE 6: Lógica Integrada (1h)
- [ ] **app/page.tsx**: 
  ```typescript
  'use client';
  import { useContracts } from '@/hooks/useContracts';
  import { useTheme } from '@/hooks/useTheme';
  import { useSteps } from '@/hooks/useSteps';
  import TopBar from '@/components/TopBar';
  import Sidebar from '@/components/Sidebar';
  import EditorPanel from '@/components/EditorPanel';
  import PreviewPanel from '@/components/PreviewPanel';
  import ResizableDivider from '@/components/ResizableDivider';
  
  export default function Home() {
    const contracts = useContracts();
    const theme = useTheme();
    const steps = useSteps();
    
    return (
      <>
        <TopBar contract={contracts.currentContract} />
        <div className="app">
          <Sidebar 
            contracts={contracts}
            theme={theme}
          />
          <EditorPanel 
            contract={contracts.currentContract}
            step={steps.currentStep}
            onStepChange={steps.setStep}
          />
          <ResizableDivider />
          <PreviewPanel contract={contracts.currentContract} />
        </div>
      </>
    );
  }
  ```

- [ ] **useState em componentes** para form fields (f-nr-os, f-ag-cod, etc)
- [ ] **useEffect** para liveUpdate quando form muda
- [ ] **localStorage** integrado em useTheme

### FASE 7: Testes (30 min)
- [ ] `npm run dev` — app roda em localhost:3000 ✓
- [ ] Alternar contratos (9 opções) ✓
- [ ] Navegação 3 steps funciona ✓
- [ ] Dark mode toggle salva em localStorage ✓
- [ ] Campos form → preview sync em tempo real ✓
- [ ] Botão Gerar mostra progress overlay ✓
- [ ] Toast notificações funcionam ✓
- [ ] Redimensionador painéis funciona ✓
- [ ] `npm run build` — sem erros TypeScript/build ✓

---

## 🔧 INSTRUÇÕES TÉCNICAS

### ⚠️ LEITURA OBRIGATÓRIA — NÃO COPIE O HTML

O arquivo `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\index.html` é sua **INSPIRAÇÃO**, não seu template.

**O que fazer:**
```
✅ Abra o HTML e ENTENDA a estrutura visual
✅ Veja como os 3 steps estão organizados
✅ Veja os componentes (topbar, sidebar, editor, preview)
✅ Veja como campos conectam ao preview (liveUpdate logic)
✅ Copie CSS variables + design system
✅ Copie a lógica funcional de app.js
```

**O que NÃO fazer:**
```
❌ Copiar HTML direto para tsx
❌ Apenas reindent o HTML como React
❌ Manter estrutura DOM do vanilla JS
```

**A diferença:**
- **HTML:** `<div id="topbar">`, `onclick="setStep(1)"`, DOM manipulation
- **React:** `<TopBar contract={...} />`, `onClick={() => setStep(1)}`, state management

### 1. Não remova nada do V4
O Next.js do V4 provavelmente tem config útil. Mantenha:
- `next.config.js`
- `tsconfig.json`
- Configuração Tailwind (se houver)

### 2. Use HTML como REFERÊNCIA VISUAL + LÓGICA
**O HTML mostra:**
- Layout: topbar (48px) + [sidebar | editor | preview]
- Components: 4 sections principais (header, nav, section.editor, section.preview)
- Styling: CSS variables (`--shell-bg`, `--orange`, etc)
- Lógica: functions em app.js (renderContractList, liveUpdate, setStep, etc)

**React vai:**
- Estruturar como components: `<TopBar />`, `<Sidebar />`, `<EditorPanel />`, `<PreviewPanel />`
- State management em hooks: `useContracts()`, `useTheme()`, `useSteps()`
- CSS modules ou Tailwind (não cópia do styles.css)
- Event handlers como funções React (não onclick inline)

### 3. Live Update é crítico
Quando usuário digita em `f-nr-os`:
1. Estado local muda (useState)
2. useEffect detecta mudança
3. liveUpdate() roda
4. Preview atualiza com flash animation

### 4. localStorage para tema
```typescript
const saved = localStorage.getItem('theme') || 'dark';
// Restaurar ao load
// Salvar ao toggle
```

### 5. Resizable divider
Precisão importante:
- Min width editor: 300px
- Max width: app.width - 300px
- Drag logic smooth sem lag

---

## 📝 PRÓXIMOS PASSOS APÓS ESTA TAREFA

1. ✅ Portar app.js para React hooks
2. ⏳ Integrar Excel parser (SheetJS) — Step 2
3. ⏳ Blocos dinâmicos — UI seletor itens
4. ⏳ Gerador JSON para skill

---

## 💬 COMUNICAÇÃO

**Antes de começar:** Não altere diretamente. Converse comigo se tiver dúvidas sobre:
- Qual parte da lógica mapear para qual hook
- Como estruturar componentes em React
- Padrões do V4 que devo manter

**Durante:** Update a cada 30-45 min com progresso
**Após:** Share lista dos componentes criados + testes passando

---

**Hora de começar!** Copie V4 frontend para V5/frontend, vire React profissional mantendo a lógica 100%. 🚀
