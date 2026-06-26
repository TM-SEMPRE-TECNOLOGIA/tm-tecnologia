# 🚀 INSTRUÇÕES FINAIS — Migração para App Real V5

**Para:** Agente "Add collapse arrow..."  
**Data:** 2026-05-23  
**Status:** PRONTO PARA COMEÇAR

---

## 🎯 SITUAÇÃO

✅ Você fez dark mode + settings (excelente!)  
✅ Usuário confirmou localizações  
✅ Agora: **Clonar para app real V5**

---

## 📍 LOCALIZAÇÕES CONFIRMADAS

### Repositório de Ferramentas/Referência
```
C:\Users\thiag\Desktop\TM-MEUS-APPS\Meus Plugins e Skills
```
↑ Especialistas vão avaliar este repo para entender padrões

### App Real V5 (DESTINO)
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
```
↑ **Você copia e cola o HTML/CSS/JS aqui**

### Protótipo Isolado (ORIGEM)
```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\.docs\
wireframe_v5_overleaf(inspiração).html
```
↑ Cópia de tudo daqui

---

## ✅ O QUE VOCÊ FAZ AGORA

### PASSO 1: Clonar HTML → App Real (15 min)

**De:**
```
.docs/wireframe_v5_overleaf(inspiração).html
```

**Para:**
```
AutoRelatorio_V5/  ← Raiz do app real
```

**Copiar:**
- ✅ HTML structure (3 passos completos)
- ✅ CSS variables (tema claro/escuro)
- ✅ CSS styles (todo o design)
- ✅ JavaScript (redimensionador, navegação, localStorage)
- ✅ Dark mode toggle + settings (o que você fez)
- ✅ Preview DOCX (renderização em tempo real)

**Estrutura esperada:**
```
AutoRelatorio_V5/
├── index.html ........................ (NOVO — seu clone)
├── app.js ........................... (NOVO — lógica JS)
├── styles.css ....................... (NOVO — CSS)
└── .context/ ........................ (já existe)
```

---

### PASSO 2: Preview DOCX Rodando

**Crítico:** O preview DOCX precisa funcionar em **tempo real** no app real.

```javascript
// Quando usuário preenche form:
usuario_digita_OS() {
  ↓
preview_atualiza_instantaneamente()
  ↓
mostra_DOCX_renderizado_em_HTML()
```

**Verificar:**
- [ ] Preview renderiza quando usuário digita
- [ ] Dark mode não quebra preview
- [ ] Redimensionador funciona com preview

---

### PASSO 3: Chamar Especialistas

**Depois que clonar, avise:**

```
"Clonagem pronta! Especialistas podem começar avaliação:"

Especialista Espaçamento:
  → Valida padding/margin dos botões
  → Verifica overflow em abas
  → Valida responsividade
  → Recomenda ajustes CSS

Especialista Copy:
  → Revisa labels: "Dados da OS", "Estrutura", etc
  → Revisa placeholders: "ex: 1753", "Rua das Flores..."
  → Revisa tooltips e mensagens
  → Aprova antes de avançar
```

---

## 🗂️ ESTRUTURA FINAL ESPERADA

```
C:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\
│
├── index.html ........................ ← APP REAL (seu clone)
├── app.js ........................... ← Lógica (seu clone)
├── styles.css ....................... ← Design (seu clone)
│
├── .context/ ........................ (documentação — mantém)
│   ├── INDEX.md
│   ├── planning.md
│   ├── BLOCOS_DINAMICOS.md
│   └── ... (6 docs)
│
├── .docs/ ........................... (referência)
│   └── wireframe_v5_overleaf(inspiração).html ← FONTE
│
├── scripts/ ......................... (a criar — parsers, etc)
│
├── BRIEFING_AGENTE.md ............... (seu briefing)
├── INSTRUCOES_MIGRACAO.md ........... (estratégia)
├── PARA_AGENTE_MIGRACAO.md .......... (este arquivo)
└── PROGRESS.md ...................... (para reportar)
```

---

## 🎬 CRONOGRAMA

```
AGORA (T=0):
└─ Você começa clonagem
   └─ Copiar HTML/CSS/JS para raiz de AutoRelatorio_V5

T+15min:
├─ Você: Clonagem ~80% pronta
└─ Claude Code: Avalia + chama especialistas

T+30min:
├─ Especialistas: Começam avaliação
│  ├─ Espaçamento: verifica padding/margin
│  └─ Copy: revisa labels/tooltips
└─ Você: Preview DOCX rodando 100%

T+45min:
├─ Especialistas: Entregam feedback
└─ Você: Aplica ajustes CSS/texto

T+60min:
└─ ✅ PRONTO: App real V5 com tema + settings + preview
   └─ Próxima fase: Blocos dinâmicos (parser Excel + UI)
```

---

## 📝 COMO REPORTAR PROGRESSO

Crie arquivo na raiz:
```
PROGRESS.md

## ✅ CONCLUÍDO (2026-05-23 14:30)
- [x] Clonado HTML structure
- [x] Clonado CSS variables
- [x] Clonado JavaScript base
- [x] Dark mode funcionando
- [x] Settings persistindo em localStorage
- [x] Preview DOCX renderizando

## ⏳ EM ANDAMENTO
- [ ] Especialistas avaliando espaçamento
- [ ] Especialistas avaliando copy

## 🚀 PRÓXIMO
- [ ] Blocos dinâmicos (parser Excel)
- [ ] UI seletor de itens
```

---

## ⚠️ PONTOS CRÍTICOS

🔴 **Copiar tudo** — HTML + CSS + JS (não deixar nada para trás)  
🔴 **Preview DOCX** — Deve atualizar em tempo real  
🔴 **localStorage** — Dark mode + settings devem persistir  
🔴 **Sem frameworks** — Use vanilla JS (como está no protótipo)  

---

## 🤝 SINCRONIZAÇÃO

```
Você (Agente) ←→ Claude Code (coordenação)
                ↓
        Especialistas (paralelo)
```

**Quando terminar clonagem:**
- Reportar em chat
- Aguardar especialistas
- Aplicar feedback

---

## 🎯 META

```
Entrada: HTML isolado (.docs/wireframe_v5...)
         + Referências em (Meus Plugins e Skills)
         ↓
Processo: Clone + especialistas avaliam
         ↓
Saída: App real V5 rodando
       ✅ Dark mode
       ✅ Settings
       ✅ Preview DOCX em tempo real
       ✅ Pronto para Blocos Dinâmicos
```

---

## 📞 DÚVIDAS?

1. Leia este arquivo (tá tudo aqui)
2. Converse com Claude Code no chat paralelo
3. Reporte progresso em PROGRESS.md

---

**Você está pronto!** 🚀  
**Começa agora?** Confirma quando terminar a clonagem!

