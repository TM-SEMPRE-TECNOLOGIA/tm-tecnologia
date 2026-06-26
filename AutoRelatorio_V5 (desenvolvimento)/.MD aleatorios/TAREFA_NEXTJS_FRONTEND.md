# 🚀 TAREFA: Integrar Frontend Next.js Real (V5)

**Para:** Agente "Add collapse arrow..."  
**Tipo:** Implementação crítica  
**Tempo estimado:** 2-3 horas  
**Prioridade:** MÁXIMA

---

## 🎯 OBJETIVO

**NÃO:** Copiar HTML direto  
**SIM:** Criar componentes React profissionais baseados no HTML como REFERÊNCIA

**Resultado esperado:**
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
├── APP/
│   ├── frontend/ ...................... ← NEXT.JS REAL (criar)
│   │   ├── app/
│   │   ├── components/
│   │   ├── public/
│   │   ├── styles/
│   │   └── package.json
│   │
│   └── backend/ ....................... (opcional, phase 2)
│
├── .docs/
│   └── wireframe_v5_overleaf(inspiração).html ← REFERÊNCIA (consultar)
│
└── scripts/ ........................... (auxiliares)
```

---

## 📋 ESTRUTURA BASE (Copiar da V4)

### Source
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V4\APP\frontend\
```

### Destination
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\APP\frontend\
```

**O que copiar:**
```
V4 frontend/
├── app/ ........................ Manter (App Router de Next.js 13+)
├── components/ ................. Manter estrutura
├── public/ ..................... Adaptar (logos, ícones)
├── styles/ ..................... Adaptar (CSS, Tailwind)
├── package.json ................ IMPORTANTE: manter dependências
├── next.config.js .............. Manter
├── tsconfig.json ............... Manter
└── .env.local .................. Adaptar URLs
```

---

## 🛠️ O QUE IMPLEMENTAR

### PASSO 1: Setup Next.js (30 min)

```bash
# 1. Copiar V4 frontend como base
cp -r "C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V4\APP\frontend" \
      "C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\APP\frontend"

# 2. Instalar dependências
cd C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\APP\frontend
npm install

# 3. Testar build
npm run build
npm run dev
```

---

### PASSO 2: Layout Principal (Usar HTML como Referência)

**Arquivo:** `app/page.tsx` (ou `app/layout.tsx`)

**HTML de referência:** `.docs/wireframe_v5_overleaf(inspiração).html`

**Estrutura esperada:**

```tsx
// app/page.tsx
export default function Home() {
  return (
    <>
      <TopBar /> {/* Barra superior com logo + contrato + mode pill */}
      <div className="app-layout">
        <Sidebar /> {/* Nav esquerda com contratos */}
        <EditorPanel /> {/* Passo 1, 2, 3 - navegável */}
        <ResizableDivider /> {/* Divisor redimensionável */}
        <PreviewPanel /> {/* Preview DOCX em tempo real */}
      </div>
    </>
  );
}
```

---

### PASSO 3: Componentes Críticos

#### 1️⃣ TopBar Component

**Referência:** HTML linhas 318-342

**O que ter:**
- Logo + nome "AutoRelatório" + versão "V5"
- Contract selector (dropdown)
- Mode pill (SP2/SP1/TRAD)
- Status badge "VISUALIZAÇÃO PRÉVIA" (português!)
- Botões: "Novo", "Gerar .docx"
- Theme toggle (lua/sol)
- Settings button (engrenagem)

```tsx
// components/TopBar.tsx
export function TopBar({ contract, onContractChange }) {
  return (
    <header className="topbar">
      {/* Logo + branding */}
      {/* Contract selector */}
      {/* Mode pill */}
      {/* Actions (novo, gerar) */}
      {/* Theme toggle + settings */}
    </header>
  );
}
```

---

#### 2️⃣ EditorPanel (3 Steps)

**Referência:** HTML linhas 367-562

**O que ter:**
- Step navigation (1. Dados da OS | 2. Estrutura | 3. Gerar)
- Step 1: Formulário cabeçalho (OS, agência, endereço, etc)
- Step 2: Estrutura de blocos (scan zone, blocos detectados)
- Step 3: Resumo geração
- Botões: Voltar, Próximo, Gerar .docx

```tsx
// components/EditorPanel.tsx
export function EditorPanel() {
  const [step, setStep] = useState(1);
  
  return (
    <section className="editor">
      <EditorTopBar />
      <StepsBar currentStep={step} onStepChange={setStep} />
      <EditorBody step={step} />
      <EditorFooter step={step} onStepChange={setStep} />
    </section>
  );
}
```

---

#### 3️⃣ PreviewPanel

**Referência:** HTML linhas 565-689

**O que ter:**
- Preview topbar (label, filename, zoom controls)
- Preview viewport com renderização DOCX HTML
- Zoom in/out (+/-)
- Scroll com documento simulado

```tsx
// components/PreviewPanel.tsx
export function PreviewPanel({ data }) {
  const [zoom, setZoom] = useState(0.9);
  
  return (
    <section className="preview">
      <PreviewTopbar zoom={zoom} onZoom={setZoom} />
      <PreviewViewport zoom={zoom} />
    </section>
  );
}
```

---

#### 4️⃣ ResizableDivider

**Referência:** HTML linhas 90-99 (CSS) + 563-564 (HTML)

**O que ter:**
- Divisor redimensionável entre editor e preview
- Mouse drag para ajustar largura
- Visual feedback (cor muda)
- Min/max width constraints

```tsx
// components/ResizableDivider.tsx
export function ResizableDivider({ editorWidth, onResize }) {
  // Drag logic: mousedown → mousemove → width update
  return (
    <div 
      className="resizable-divider"
      onMouseDown={(e) => handleResize(e, onResize)}
    />
  );
}
```

---

### PASSO 4: Dark Mode + Settings

**Status:** Já implementado no HTML! ✅

**Manter:**
- CSS variables (--shell-bg, --shell-text, etc)
- localStorage persistence
- Theme toggle (lua/sol)
- Settings button com engrenagem

```tsx
// hooks/useTheme.tsx
export function useTheme() {
  const [isDark, setIsDark] = useState(true);
  
  useEffect(() => {
    // Ler de localStorage
    // Aplicar classe "light-mode" ou "dark-mode"
    // Persistir mudanças
  }, [isDark]);
  
  return { isDark, toggle: () => setIsDark(!isDark) };
}
```

---

### PASSO 5: Styling (Usar HTML como Referência)

**Referência:** HTML linhas 9-312 (CSS completo)

**O que fazer:**
- Copiar CSS do HTML para `styles/globals.css`
- Adicionar CSS variables do tema
- Adaptar para Next.js/Tailwind (se usar)
- Manter dark mode variables

```css
/* styles/globals.css ou styles/theme.css */

:root {
  /* Dark mode padrão */
  --shell-bg: #111110;
  --shell-card: #1A1917;
  --shell-text: #EFEDE8;
  /* ... resto das variáveis */
}

html.light-mode {
  /* Light mode */
  --shell-bg: #F8F7F4;
  --shell-card: #FFFFFF;
  --shell-text: #2C2C2C;
  /* ... resto das variáveis */
}
```

---

## 📋 CHECKLIST IMPLEMENTAÇÃO

### Setup (30 min)
- [ ] Copiar estrutura V4 frontend para V5
- [ ] npm install
- [ ] npm run dev (verificar que roda)

### Componentes (90 min)
- [ ] TopBar (logo + contract + mode + actions)
- [ ] EditorPanel com 3 steps
- [ ] PreviewPanel com viewport
- [ ] ResizableDivider
- [ ] Sidebar com lista de contratos

### Estilo (30 min)
- [ ] CSS variables (dark/light mode)
- [ ] Aplicar stylesheet do HTML
- [ ] Verificar responsividade

### Features (30 min)
- [ ] Dark mode toggle (lua/sol)
- [ ] Settings button
- [ ] localStorage persistence
- [ ] Navegação 3 steps

### Testes (30 min)
- [ ] npm run build (sem erros)
- [ ] npm run dev (roda em localhost:3000)
- [ ] Dark/light mode funciona
- [ ] Settings persistem
- [ ] Preview atualiza em tempo real

---

## 🔗 REFERÊNCIAS

| O que | Onde no HTML |
|------|-------------|
| TopBar | Linhas 317-342 |
| Sidebar | Linhas 346-364 |
| EditorPanel | Linhas 366-562 |
| PreviewPanel | Linhas 565-689 |
| CSS variables | Linhas 9-42 |
| Dark mode CSS | Linhas 44-60 |
| ResizableDivider | Linhas 90-99 (CSS) + 563 (HTML) |

---

## 📝 NÃO FAZER

❌ Copiar HTML direto como .html no Next.js  
❌ Usar CSS inline (usar Tailwind ou CSS modules)  
❌ Hardcoded colors (usar CSS variables)  
❌ Esquecer localStorage para tema  
❌ Deixar console.logs de debug  

---

## 🎬 COMEÇAR

1. Ler este documento (5 min)
2. Copiar estrutura V4 (5 min)
3. Instalar dependências (5 min)
4. Testar que Next.js roda (5 min)
5. Começar implementar componentes (2h)

**Total:** ~2.5 horas

---

## 📞 DÚVIDAS FREQUENTES

**P: Preciso usar Tailwind?**  
R: Se V4 usa, mantenha. Se prefere CSS puro, tá OK também.

**P: Componentizar tudo ou deixar em page.tsx?**  
R: Componentizar! Cada seção é um component.

**P: E o backend da V5?**  
R: Phase 2. Agora é só frontend.

**P: Onde fica o run.bat?**  
R: Na raiz, após frontend estar pronto.

---

**Status:** Pronto para começar 🚀  
**Próximo checkpoint:** Após frontend rodar, implementar Blocos Dinâmicos

