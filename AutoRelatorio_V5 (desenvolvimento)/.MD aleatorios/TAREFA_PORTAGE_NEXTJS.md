---
name: portage-nextjs-react
description: Portage completo de app vanilla JS para Next.js + React (4-5h)
metadata:
  type: tarefa
  prioridade: ALTA
  tempo: 240-300 min
---

# 🚀 TAREFA: Portar App Real V5 para Next.js + React

**Status:** Pronto para começar  
**Tempo estimado:** 4-5 horas  
**Estrutura base:** V4 frontend (já exists, clonar e adaptar)

---

## 📍 LOCALIZAÇÕES

### Origem (Inspiração)
- **HTML vanilla:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\index.html`
- **JS lógica:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\app.js`
- **CSS design:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\styles.css`

### Base Next.js (Template)
- **V4 frontend:** `C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V4\APP\frontend`
- **Estrutura:** já pronta (app/, components/, store/, lib/, styles/)
- **Config:** next.config.ts, tsconfig.json, package.json

### Destino (Novo)
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\frontend\
├── app/
├── components/
├── lib/
├── store/
├── styles/
├── public/
├── package.json
└── next.config.ts
```

---

## 🏗️ ARQUITETURA REACT

### 7 FASES SEQUENCIAIS

#### FASE 1: Setup Base (30 min)

**O que fazer:**
1. Copiar estrutura V4 para V5/frontend (ou criar novo Next.js)
2. Validar `npm install` (sem erros)
3. Validar `npm run dev` (localhost:3000)

**Checklist:**
- [ ] Pasta `frontend/` criada em V5
- [ ] Todos os arquivos base presentes
- [ ] `npm install` rodou OK
- [ ] `npm run dev` abre http://localhost:3000 sem erro

---

#### FASE 2: Constants & Types (30 min)

**Criar:** `lib/contracts.ts`

```typescript
export const CONTRACTS = [
  { id: '0908', name: 'São José dos Campos', short: 'SJC', mode: 'sp' as const, uf: 'SP' },
  { id: '1507', name: 'Cuiabá', short: 'Cuiabá', mode: 'trad' as const, uf: 'MT' },
  { id: '1565', name: 'SJRP / Ribeirão Preto', short: 'SJRP', mode: 'sp2' as const, uf: 'SP' },
  { id: '2056', name: 'Divinópolis', short: 'Divin.', mode: 'trad' as const, uf: 'MG' },
  { id: '2057', name: 'Varginha', short: 'Varginha', mode: 'trad' as const, uf: 'MG' },
  { id: '2626', name: 'Salinas', short: 'Salinas', mode: 'trad' as const, uf: 'MG' },
  { id: '2627', name: 'Gov. Valadares', short: 'Valadares', mode: 'trad' as const, uf: 'MG' },
  { id: '3575', name: 'Tangará da Serra', short: 'Tangará', mode: 'trad' as const, uf: 'MT' },
  { id: '6122', name: 'Mato Grosso do Sul', short: 'MS', mode: 'trad' as const, uf: 'MS' },
];

export type ContractMode = 'sp2' | 'sp' | 'trad';

export interface IContract {
  id: string;
  name: string;
  short: string;
  mode: ContractMode;
  uf: string;
}
```

**Criar:** `lib/descriptions.ts`

```typescript
export const DESCRIPTIONS = {
  '1': 'Informamos que foi realizada visita técnica à agência para fins de levantamento preventivo...',
  '2': 'No cumprimento das atividades programadas, nosso técnico realizou uma visita à agência...',
  '3': 'Informamos que nosso técnico realizou uma visita à agência para a execução...',
  '4': 'Nosso técnico realizou uma visita à agência para a execução do levantamento preventivo...',
};
```

**Criar:** `lib/types.ts`

```typescript
import type { ContractMode } from './contracts';

export interface IContract {
  id: string;
  name: string;
  short: string;
  mode: ContractMode;
  uf: string;
}

export interface IFormData {
  nr_os: string;
  ag_cod: string;
  ag_nome: string;
  dt_atend: string;
  endereco: string;
  responsavel_dependencia: string;
  desc: '1' | '2' | '3' | '4';
}

export interface IPreviewData extends IFormData {
  contrato: string;
  uf: string;
  responsavel_tecnico: string;
}
```

**Checklist:**
- [ ] `lib/contracts.ts` criado com 9 contratos
- [ ] `lib/descriptions.ts` criado com 4 templates
- [ ] `lib/types.ts` criado com interfaces
- [ ] TypeScript compile OK (sem erros)

---

#### FASE 3: Hooks Customizados (1h)

**Criar:** `hooks/useContracts.ts`

```typescript
'use client';

import { useState } from 'react';
import { CONTRACTS, type IContract } from '@/lib/contracts';

export function useContracts() {
  const [currentContract, setCurrentContract] = useState<IContract>(CONTRACTS[2]); // 1565 default

  const selectContract = (id: string) => {
    const contract = CONTRACTS.find(c => c.id === id);
    if (contract) setCurrentContract(contract);
  };

  return {
    currentContract,
    contracts: CONTRACTS,
    selectContract,
  };
}
```

**Criar:** `hooks/useTheme.ts`

```typescript
'use client';

import { useEffect, useState } from 'react';

export function useTheme() {
  const [isDark, setIsDark] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Restaurar tema salvo
    const saved = localStorage.getItem('theme') || 'dark';
    setIsDark(saved === 'dark');
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    
    const html = document.documentElement;
    if (isDark) {
      html.classList.remove('light-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      html.classList.add('light-mode');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark, mounted]);

  const toggleTheme = () => setIsDark(!isDark);

  return { isDark, toggleTheme, mounted };
}
```

**Criar:** `hooks/useSteps.ts`

```typescript
'use client';

import { useState } from 'react';

export function useSteps() {
  const [currentStep, setStep] = useState(2); // Default: step 2

  const nextStep = () => {
    if (currentStep < 3) setStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setStep(currentStep - 1);
  };

  return {
    currentStep,
    setStep,
    nextStep,
    prevStep,
  };
}
```

**Criar:** `hooks/useFormData.ts`

```typescript
'use client';

import { useState, useCallback } from 'react';
import type { IFormData } from '@/lib/types';

const initialData: IFormData = {
  nr_os: '',
  ag_cod: '',
  ag_nome: '',
  dt_atend: new Date().toISOString().split('T')[0],
  endereco: '',
  responsavel_dependencia: '',
  desc: '1',
};

export function useFormData() {
  const [formData, setFormData] = useState<IFormData>(initialData);

  const updateField = useCallback((field: keyof IFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  }, []);

  const reset = useCallback(() => {
    setFormData(initialData);
  }, []);

  return {
    formData,
    updateField,
    reset,
  };
}
```

**Checklist:**
- [ ] `hooks/useContracts.ts` criado
- [ ] `hooks/useTheme.ts` criado com localStorage
- [ ] `hooks/useSteps.ts` criado
- [ ] `hooks/useFormData.ts` criado
- [ ] Todos compile OK

---

#### FASE 4: Componentes UI (2h)

**Criar:** `components/TopBar.tsx`

```typescript
'use client';

import { useContracts } from '@/hooks/useContracts';
import type { ContractMode } from '@/lib/contracts';

interface TopBarProps {
  onStartClick: () => void;
  onNewClick: () => void;
  onGenerateClick: () => void;
}

export function TopBar({ onStartClick, onNewClick, onGenerateClick }: TopBarProps) {
  const { currentContract } = useContracts();

  const modeConfig: Record<ContractMode, { label: string; className: string }> = {
    'trad': { label: 'TRADICIONAL', className: 'mode-trad' },
    'sp': { label: 'SP', className: 'mode-sp' },
    'sp2': { label: 'SP2', className: 'mode-sp2' },
  };

  const modeInfo = modeConfig[currentContract.mode];

  return (
    <header className="topbar">
      <a className="brand" href="#">
        <div className="brand-logo">📄</div>
        <span className="brand-name">AutoRelatório</span>
        <span className="brand-ver">V5</span>
      </a>
      
      <div className="topbar-div"></div>
      
      <div className="topbar-contract">
        <span className="contract-pill">{currentContract.id}</span>
        <span className="contract-name">{currentContract.name}</span>
        <span className={`mode-pill ${modeInfo.className}`}>{modeInfo.label}</span>
      </div>

      <div className="topbar-spacer"></div>

      <div className="topbar-actions">
        <div className="status-badge">
          <span className="dot-live"></span>
          VISUALIZAÇÃO PRÉVIA
        </div>
        
        <button className="btn btn-primary btn-sm" onClick={onStartClick} title="Inicia servidor local">
          ▶ START
        </button>
        
        <button className="btn btn-ghost btn-sm" onClick={onNewClick} title="Novo relatório">
          ← Novo
        </button>
        
        <button className="btn btn-primary btn-sm" onClick={onGenerateClick} title="Gera arquivo .docx">
          📄 Gerar .docx
        </button>
      </div>
    </header>
  );
}
```

**Criar:** `components/Sidebar.tsx`

```typescript
'use client';

import { useContracts } from '@/hooks/useContracts';
import { useTheme } from '@/hooks/useTheme';
import { useState } from 'react';

interface SidebarProps {
  onSettingsClick: () => void;
}

export function Sidebar({ onSettingsClick }: SidebarProps) {
  const { currentContract, contracts, selectContract } = useContracts();
  const { isDark, toggleTheme } = useTheme();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <nav className={`nav ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="nav-section">
        <div className="nav-label">Menu</div>
        <button className="nav-item active">
          📄 Gerar Relatório
        </button>
        <button className="nav-item">
          🕐 Histórico
        </button>
      </div>

      <div className="nav-div"></div>

      <div className="nav-toggle-row">
        <div className="nav-label">Contratos</div>
        <button 
          className="nav-toggle-btn" 
          onClick={() => setIsCollapsed(!isCollapsed)}
          title="Encolher/Expandir"
        >
          ◀
        </button>
      </div>

      <div className="contract-list">
        {contracts.map(contract => (
          <div
            key={contract.id}
            className={`c-item ${contract.id === currentContract.id ? 'active' : ''}`}
            onClick={() => selectContract(contract.id)}
          >
            <span className="c-id">{contract.id}</span>
            {!isCollapsed && (
              <>
                <div className="c-info">
                  <div className="c-name">{contract.name}</div>
                  <div className="c-mode">{contract.mode.toUpperCase()} · {contract.uf}</div>
                </div>
                <div className="c-dot"></div>
              </>
            )}
          </div>
        ))}
      </div>

      <div className="nav-footer">
        <button 
          className="nav-footer-btn" 
          onClick={toggleTheme}
          title={isDark ? 'Modo claro' : 'Modo escuro'}
        >
          {isDark ? '☀️' : '🌙'}
        </button>
        <button 
          className="nav-footer-btn" 
          onClick={onSettingsClick}
          title="Configurações"
        >
          ⚙️
        </button>
      </div>
    </nav>
  );
}
```

**Criar:** `components/EditorPanel.tsx`

Estrutura dos 3 steps com formulários (lógica de app.js linhas 140-250)

**Criar:** `components/PreviewPanel.tsx`

Preview DOCX com sincronização live (lógica de app.js linhas 260+)

**Criar:** `components/Toast.tsx`

Sistema de notificações

**Checklist:**
- [ ] TopBar.tsx criado
- [ ] Sidebar.tsx com contracts list + dark mode
- [ ] EditorPanel.tsx com 3 steps
- [ ] PreviewPanel.tsx com live sync
- [ ] Toast.tsx para notificações
- [ ] ResizableDivider.tsx para drag
- [ ] Todos componentes compilam

---

#### FASE 5: Styling (45 min)

**Copiar:** CSS variables de `styles.css` para `app/globals.css`

```css
:root {
  /* Dark shell */
  --shell-bg: #111110;
  --shell-card: #1A1917;
  --shell-border: #2A2825;
  --shell-text: #EFEDE8;
  --shell-muted: #8C8A85;
  /* Brand orange */
  --orange: #C8541C;
  --orange-hover: #E06428;
  /* ... etc */
}

html.light-mode {
  --shell-bg: #F8F7F4;
  --shell-card: #FFFFFF;
  --shell-text: #2C2C2C;
  /* ... etc */
}
```

**Adaptar:** Componentes para CSS modules ou Tailwind

**Checklist:**
- [ ] CSS variables copiadas
- [ ] Dark/light mode funciona
- [ ] Animações funcionam (pulse, flash, spin)
- [ ] Responsividade OK

---

#### FASE 6: Orquestração (1h)

**Criar:** `app/page.tsx`

```typescript
'use client';

import { useState, useEffect } from 'react';
import { TopBar } from '@/components/TopBar';
import { Sidebar } from '@/components/Sidebar';
import { EditorPanel } from '@/components/EditorPanel';
import { PreviewPanel } from '@/components/PreviewPanel';
import { Toast } from '@/components/Toast';
import { useTheme } from '@/hooks/useTheme';
import { useContracts } from '@/hooks/useContracts';
import { useSteps } from '@/hooks/useSteps';
import { useFormData } from '@/hooks/useFormData';

export default function Home() {
  const { mounted } = useTheme();
  const { currentContract } = useContracts();
  const { currentStep, setStep } = useSteps();
  const { formData, updateField } = useFormData();
  const [toast, setToast] = useState<string | null>(null);

  if (!mounted) return null; // Avoid hydration mismatch

  return (
    <div className="app-container">
      <TopBar
        onStartClick={() => setToast('🚀 Para iniciar: execute run.bat')}
        onNewClick={() => setStep(1)}
        onGenerateClick={() => setToast('Gerando relatório...')}
      />

      <div className="app-layout">
        <Sidebar onSettingsClick={() => setToast('⚙️ Configurações em breve')} />
        
        <EditorPanel
          currentStep={currentStep}
          formData={formData}
          onUpdateField={updateField}
          onSetStep={setStep}
          currentContract={currentContract}
        />

        <PreviewPanel
          formData={formData}
          currentContract={currentContract}
        />
      </div>

      {toast && <Toast message={toast} onClose={() => setToast(null)} />}
    </div>
  );
}
```

**Checklist:**
- [ ] page.tsx orquestra todos os components
- [ ] useState para toast/modals
- [ ] useEffect para localStorage
- [ ] Hydration OK (mounted check)

---

#### FASE 7: Testes (30 min)

**Rodar em dev:**
```bash
cd C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\frontend
npm run dev
```

**Testes manuais:**
- [ ] App abre em localhost:3000
- [ ] 9 contratos navegáveis (clique em cada)
- [ ] Contrato muda topbar + editor + preview
- [ ] 3 steps navegáveis (botões Próximo/Voltar)
- [ ] Campos → preview live update (tipo campo + vê alteração no preview)
- [ ] Dark mode toggle salva em localStorage (reload e mantém tema)
- [ ] Settings button mostra toast
- [ ] Toast desaparece após 3s
- [ ] Preview zoom funciona (50%-150%)
- [ ] Sidebar colapsável (números ficar visíveis)
- [ ] Redimensionador funciona (drag divider entre editor e preview)

**Build:**
```bash
npm run build
```

- [ ] Build sem erros
- [ ] Output: `.next/` gerado

**Checklist final:**
- [ ] Todos os testes passaram
- [ ] Nenhum console.error
- [ ] Performance OK (sem lag ao digitar)

---

## 📋 CHECKLIST GERAL

### Antes de começar:
- [ ] Leu este documento completamente
- [ ] Entendeu as 7 fases
- [ ] Tem V4 frontend como referência
- [ ] Próxima ação: Começar FASE 1

### Durante (cada 45 min):
- [ ] Report progresso na fase atual
- [ ] Bloqueia? Avisa Claude Code

### Depois de tudo:
- [ ] Todos os testes passaram
- [ ] `npm run build` OK
- [ ] Código commitado (se usar git)
- [ ] Próximo: Blocos Dinâmicos em React

---

## 💡 NOTAS CRÍTICAS

**1. "use client" em todos hooks/components**
```typescript
'use client';
// Necessário para useState, useEffect, etc
```

**2. Live Update é essencial**
```typescript
// Em EditorPanel.tsx
useEffect(() => {
  if (formData.nr_os) {
    updatePreview(); // Recalcula preview
  }
}, [formData]); // Dispara quando formData muda
```

**3. LocalStorage timing**
```typescript
// Em useTheme.ts
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
// Evita hydration mismatch
```

**4. Resizable divider sem lag**
```typescript
// MouseMove listener no document, não no divider
// classList toggle em mousedown/mouseup
// Cursor change para feedback
```

**5. Mantenha V4 patterns**
- Store structure (Zustand se usar)
- next.config.ts settings
- tsconfig paths
- ESLint rules

---

## 📞 COMUNICAÇÃO

**Se bloquear:**
- Diga qual fase + qual componente
- Compartilhe o erro exato
- Claude Code resolve

**Progress updates:**
- A cada 45 min
- Qual fase, % de conclusão
- Bloqueios identificados

**Após completar:**
- Compartilha componentes criados
- Screenshot dos testes
- Pronto para Blocos Dinâmicos

---

## ✨ META FINAL

```
Entrada: HTML vanilla V5 + JS lógica
         ↓
Processo: 7 fases React, mantendo 100% funcionalidade
         ↓
Saída: Next.js profissional pronto para:
       ✅ Excel parser (SheetJS)
       ✅ Blocos dinâmicos UI
       ✅ JSON generator
       ✅ Backend integration
```

---

**Tempo total:** 4-5 horas  
**Complexidade:** ALTA (mas bem documentada)  
**Resultado:** App production-ready em React

**Pode começar! 🚀**
