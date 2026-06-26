# ⚡ MUDANÇA DE ESTRATÉGIA — Migração Imediata para App Real

**Data:** 2026-05-23  
**Para:** Agente "Add collapse arrow..."  
**Prioridade:** CRÍTICA

---

## 🎯 NOVO OBJETIVO

**NÃO** refinar protótipo HTML isolado.

**SIM:** Clone o HTML direto para o **aplicativo real V5** e integre **especialistas para avaliar**.

---

## 📋 FLUXO REVISADO

### 1️⃣ ESPECIALISTAS AVALIAM AMBOS (Em paralelo)

```
Especialista Espaçamento:
  ├─ Avalia: HTML isolado (.docs/wireframe_v5...)
  ├─ Avalia: App real (V5 React/Next)
  └─ Recomenda: Implementação no app real

Especialista Copy:
  ├─ Avalia: Labels/placeholders/tooltips
  ├─ Avalia: Fluxo de mensagens 3 passos
  └─ Aprova: Copy antes da integração
```

### 2️⃣ VOCÊ: Clone para App Real

```
De: .docs/wireframe_v5_overleaf(inspiração).html
Para: C:\Users\thiag\TM-MEUS-APPS\03_Arquivo_Morto_Legado\.NEXT APPS\TURBO DEV
      (ou wherever the real V5 app está)

Copiar:
  ✅ HTML structure (3 passos)
  ✅ CSS (dark mode + variáveis)
  ✅ JavaScript (redimensionador, navegação)
  ✅ Preview DOCX em tempo real

Não copiar:
  ❌ Estilos inline (use CSS modules/Tailwind do app)
  ❌ JavaScript global (use state management do app)
```

### 3️⃣ INTEGRAR PREVIEW DOCX

**O preview em tempo real (mostrando Word renderizado) precisa rodar NO APP REAL.**

```
Localizar:
  - Onde está o preview DOCX no app real?
  - Qual é o componente?
  - Usa qual lib? (html2canvas? custom render?)

Integrar:
  - Trazer lógica de preview do protótipo
  - Adaptar para componentes React/Next
  - Manter renderização em tempo real
```

---

## 📍 LOCALIZAÇÃO DO APP REAL

```
C:\Users\thiag\TM-MEUS-APPS\
└── 03_Arquivo_Morto_Legado\
    └── .NEXT APPS\
        └── TURBO DEV  ← APP REAL V5 (provavelmente)
```

**⚠️ Confirme com usuário a pasta exata do app real!**

---

## ✅ CHECKLIST DO AGENTE

### Antes de começar:
- [ ] Confirmar localização do app real V5
- [ ] Identificar estrutura do app (React? Next.js? Vue?)
- [ ] Mapear componentes existentes (tema, settings, etc)

### Clonagem:
- [ ] Copiar HTML structure (3 passos)
- [ ] Copiar CSS (tema claro/escuro)
- [ ] Copiar lógica JavaScript (converter para estado do app)
- [ ] Integrar preview DOCX em tempo real

### Chamada de especialistas:
- [ ] Espaçamento: avaliar integração no app real
- [ ] Copy: revisar labels/tooltips no contexto do app
- [ ] Aplicar feedback

### Não tocar em:
- [ ] Blocos dinâmicos (ainda não)
- [ ] Parser Excel (ainda não)
- [ ] Gerador JSON (ainda não)

**Isso vem DEPOIS da migração.**

---

## 🚀 ORDEM DE EXECUÇÃO

```
T=0min:
└─ Você começa:
   1. Confirmar localização app real
   2. Analisar estrutura
   3. Iniciar clonagem

T=15min:
├─ Você: ~30% clonado
└─ Especialistas: Começam avaliação

T+30min:
├─ Você: ~70% clonado + preview DOCX rodando
└─ Especialistas: Entregam feedback

T+45min:
└─ Você: Aplica feedback + tudo pronto

Result: App real V5 com tema + settings + preview DOCX rodando ✅
```

---

## ⚠️ PONTOS CRÍTICOS

🔴 **APP REAL:** Qual é a pasta exata? Estrutura? Framework?  
🔴 **PREVIEW DOCX:** Como está implementado no app real?  
🔴 **STATE MANAGEMENT:** Redux? Context? Zustand?  
🔴 **CSS:** Tailwind? CSS Modules? Styled Components?

**→ Não avance sem estas respostas!**

---

## 📞 COMUNICAÇÃO

**Para você (Agente):**
1. Leia este arquivo
2. Confirme localização do app real
3. Reporte cada 15min no chat do usuário
4. Qualquer dúvida: converse com Claude Code

**Para Claude Code:**
- Você vai revisar a clonagem
- Depois chamar especialistas
- Depois validar integração

---

## ✨ META FINAL

```
✅ HTML/CSS/JS do protótipo → App Real V5
✅ Dark mode + Settings rodando
✅ Preview DOCX em tempo real
✅ Especialistas validaram espaçamento + copy
✅ Pronto para Blocos Dinâmicos (próxima fase)
```

---

**Status:** Aguardando confirmação do app real  
**Bloqueador:** Localização exata + estrutura do app

