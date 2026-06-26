# 🎯 PLANO DE IMPLEMENTAÇÃO — 6 Ajustes Críticos

**Para:** Agente "Add collapse arrow..."  
**De:** Especialistas (Spacing + Copy)  
**Status:** Pronto para implementar  
**Tempo:** 10-15 min

---

## 📊 RESUMO EXECUTIVO

✅ Clonagem concluída  
✅ App real rodando com dark mode + preview DOCX  
✅ Dois especialistas validaram tudo  

🎯 **Agora:** Aplicar 6 ajustes críticos encontrados

---

## 🔧 AJUSTE 1: Overflow em Campos

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
```css
/* Adicionar overflow handling em: */
.f-input, .f-select, .bc-name, .ia-pasta-label {
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Onde:** Dentro da seção `<style>` com os outros `.f-input` styles

**Por quê:** Labels e nomes longos estão quebrando o layout

---

## 🔧 AJUSTE 2: Line-height Consistente

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
```css
/* Adicionar line-height em: */
.f-label { line-height: 1.4; margin-bottom: 6px; }
.nav-item { line-height: 1.2; }
.c-name { line-height: 1.3; }
```

**Onde:** Dentro da seção `<style>`

**Por quê:** Espaçamento vertical desigual entre linhas

---

## 🔧 AJUSTE 3: Min-width em Flex Children

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
```css
/* Adicionar min-width em flex children: */
.bc-name, .ia-pasta-label { 
  min-width: 0; 
}
```

**Onde:** Dentro da seção `<style>`

**Por quê:** Flex items estão expandindo além do container

---

## 📝 AJUSTE 4: "PREVIEW LIVE" → "VISUALIZAÇÃO PRÉVIA"

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
Encontrar a linha com:
```html
<div class="status-badge"><span class="dot-live"></span>PREVIEW LIVE</div>
```

Trocar para:
```html
<div class="status-badge"><span class="dot-live"></span>VISUALIZAÇÃO PRÉVIA</div>
```

**Onde:** Dentro da seção `<header class="topbar">` (topo direito)

**Por quê:** Texto em inglês em interface pt-BR

---

## 📝 AJUSTE 5: "Data Atendimento" → "Data da Vistoria"

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
Encontrar:
```html
<div class="f-label">Data Atendimento <span class="req">*</span>
```

Trocar para:
```html
<div class="f-label">Data da Vistoria <span class="req">*</span>
```

**Onde:** Passo 1 (Cabeçalho), lado direito do campo "Nº da OS"

**Por quê:** Termo correto para relatório preventivo

---

## 📝 AJUSTE 6: Remover "PROCESSAMENTO NEURAL"

**Arquivo:** `.docs/wireframe_v5_overleaf(ispiração).html`

**O que fazer:**
Encontrar a seção de resumo (Passo 3) com:
```html
<div class="gen-row"><span class="gen-key">Motor</span><span class="gen-val sp2">SP2</span></div>
```

**Remover ou esconder:**
Qualquer referência a "PROCESSAMENTO NEURAL" ou "Interpolarizando" nos status logs

**Onde:** Na seção de geração (passo 3) ou progress overlay

**Por quê:** Enganoso — não há IA processando, é apenas simulação de UI

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] AJUSTE 1: overflow handling (CSS)
- [ ] AJUSTE 2: line-height consistency (CSS)
- [ ] AJUSTE 3: min-width flex children (CSS)
- [ ] AJUSTE 4: "PREVIEW LIVE" → "VISUALIZAÇÃO PRÉVIA" (HTML)
- [ ] AJUSTE 5: "Data Atendimento" → "Data da Vistoria" (HTML)
- [ ] AJUSTE 6: Remover "PROCESSAMENTO NEURAL" (HTML)

---

## 📋 ORDEM DE EXECUÇÃO RECOMENDADA

1. **CSS primeiro** (3 ajustes) — editar seção `<style>`
2. **HTML depois** (3 ajustes) — buscar e substituir textos

**Tempo estimado:** 10-15 min

---

## 🧪 TESTE DEPOIS

Depois de aplicar todos os 6:

- [ ] Abrir `.docs/wireframe_v5_overleaf(ispiração).html` no navegador
- [ ] Testar campos com textos longos (não devem quebrar)
- [ ] Verificar espaçamento vertical (uniforme)
- [ ] Confirmar textos em português
- [ ] Verificar preview DOCX ainda funciona

---

## 📞 DEPOIS DISSO

Quando terminar:
1. Converse com Claude Code no chat
2. Ele vai revisar + validar tudo
3. Próximo: **Blocos Dinâmicos** (parser Excel + UI seletor)

---

**Pronto para começar?** 🚀

