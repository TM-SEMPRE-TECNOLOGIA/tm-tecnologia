# Blocos Dinâmicos — Seleção de Fotos + Itens + Tabelas

**Data:** 2026-05-23  
**Contexto:** Requisito do usuário — adaptação dinâmica conforme unidade  
**Status:** Especificação de funcionalidade

---

## VISÃO GERAL

No **Passo 2 (Estrutura de Blocos)**, quando o usuário seleciona uma **foto**:

1. Sistema oferece **lista de itens** (importados do Excel)
2. Usuário escolhe item (ex: 17.2 — Emassamento PVA — m²)
3. Sistema **adapta o formulário** conforme a unidade
4. Usuário **preenche medidas** (valores variam por tipo)
5. Sistema **calcula automaticamente** o total
6. Sistema **renderiza tabela** no preview DOCX

---

## TIPOS DE UNIDADE E SUAS TABELAS

### 1️⃣ UNIDADE CONTÁVEL (un, pçs, etc)

**Exemplo:** Item 1.2 — Chamado (un)

```
Quando selecionado:
┌─────────────────────────────────────────┐
│ Item: 1.2 — Chamado                     │
│ Unidade: un                             │
│                                         │
│ [Foto 01] [Quantidade: ____]            │
│ [Foto 02] [Quantidade: ____]            │
│ [Foto 03] [Quantidade: ____]            │
└─────────────────────────────────────────┘

Tabela gerada no relatório:
┌─────────┬────────────┬──────────┐
│REFERÊNCIA│QUANTIDADE│ TOTAL    │
├─────────┼────────────┼──────────┤
│Foto 01  │    2      │   2 un   │
│Foto 02  │    1      │   1 un   │
│Foto 03  │    3      │   3 un   │
├─────────┼────────────┼──────────┤
│TOTAL    │            │   6 un   │
└─────────┴────────────┴──────────┘
```

---

### 2️⃣ UNIDADE DE ÁREA (m², cm², km²)

**Exemplo:** Item 17.2 — Emassamento PVA (m²)

```
Quando selecionado:
┌────────────────────────────────────────┐
│ Item: 17.2 — Emassamento PVA           │
│ Unidade: m²                            │
│                                        │
│ [Foto 01]                              │
│   Largura: [16.20] m                   │
│   Altura:  [4.63] m                    │
│   Desconto: [0] m²                     │
│   TOTAL: 75.01 m²                      │
│                                        │
│ [Foto 02]                              │
│   Largura: [8.40] m                    │
│   Altura:  [3.00] m                    │
│   Desconto: [0] m²                     │
│   TOTAL: 25.20 m²                      │
└────────────────────────────────────────┘

Tabela gerada no relatório:
┌─────────┬────────┬────────┬──────────┬──────────┐
│REFERÊNCIA│COMP(m) │ALT(m)  │DESC(m²)  │TOTAL(m²) │
├─────────┼────────┼────────┼──────────┼──────────┤
│Foto 01  │ 16.20  │ 4.63   │    0     │  75.01   │
│Foto 02  │  8.40  │ 3.00   │    0     │  25.20   │
├─────────┼────────┼────────┼──────────┼──────────┤
│TOTAL    │        │        │          │ 100.21   │
└─────────┴────────┴────────┴──────────┴──────────┘
```

---

### 3️⃣ UNIDADE DE VOLUME (m³, cm³, l)

**Exemplo:** Item 2.1 — Demolição concreto (m³)

```
Quando selecionado:
┌────────────────────────────────────────┐
│ Item: 2.1 — Demolição concreto         │
│ Unidade: m³                            │
│                                        │
│ [Foto 001]                             │
│   Comprimento: [10.50] m               │
│   Altura:      [2.80] m                │
│   Profundidade:[0.80] m                │
│   TOTAL: 23.52 m³                      │
│                                        │
│ [Foto 002]                             │
│   Comprimento: [5.20] m                │
│   Altura:      [2.80] m                │
│   Profundidade:[0.60] m                │
│   TOTAL: 8.74 m³                       │
└────────────────────────────────────────┘

Tabela gerada no relatório:
┌─────────┬────────┬────────┬────────┬──────────┐
│FOTO     │COMP(m) │ALT(m)  │PROF(m) │TOTAL(m³) │
├─────────┼────────┼────────┼────────┼──────────┤
│001      │ 10.50  │ 2.80   │ 0.80   │  23.52   │
│002      │  5.20  │ 2.80   │ 0.60   │   8.74   │
├─────────┼────────┼────────┼────────┼──────────┤
│TOTAL    │        │        │        │  32.26   │
└─────────┴────────┴────────┴────────┴──────────┘
```

---

### 4️⃣ UNIDADE LINEAR (m, cm, km)

**Exemplo:** Item 29.2 — Rodapé (m)

```
Quando selecionado:
┌────────────────────────────────────────┐
│ Item: 29.2 — Rodapé                    │
│ Unidade: m                             │
│                                        │
│ [Foto 150]                             │
│   Comprimento: [28.50] m               │
│   TOTAL: 28.50 m                       │
│                                        │
│ [Foto 151]                             │
│   Comprimento: [15.30] m               │
│   TOTAL: 15.30 m                       │
└────────────────────────────────────────┘

Tabela gerada no relatório:
┌─────────┬────────┬──────────┐
│FOTO     │COMP(m) │TOTAL(m)  │
├─────────┼────────┼──────────┤
│150      │ 28.50  │  28.50   │
│151      │ 15.30  │  15.30   │
├─────────┼────────┼──────────┤
│TOTAL    │        │  43.80   │
└─────────┴────────┴──────────┘
```

---

## FLUXO DE IMPLEMENTAÇÃO (JavaScript)

```javascript
// 1. Usuário seleciona uma foto
function selecionarFoto(fotoNumero) {
  mostrarModalSelecaoItem();  // Abre lista de itens disponíveis
}

// 2. Usuário escolhe item
function selecionarItem(itemCodigo) {
  const item = tabelaValores.find(i => i.codigo === itemCodigo);
  const unidade = item.unidade; // "un", "m²", "m³", "m"
  
  // 3. Sistema adapta o formulário
  const formulario = gerarFormularioDinamico(unidade, item);
  mostrarFormulario(formulario);
}

// 4. Gerador dinâmico conforme unidade
function gerarFormularioDinamico(unidade, item) {
  switch(unidade) {
    case "un":
    case "pçs":
    case "kg":
      return {
        campos: ["quantidade"],
        template: "contavel"
      };
    
    case "m²":
    case "cm²":
      return {
        campos: ["largura", "altura", "desconto"],
        formula: "largura * altura - desconto",
        template: "area"
      };
    
    case "m³":
    case "cm³":
      return {
        campos: ["comprimento", "altura", "profundidade"],
        formula: "comprimento * altura * profundidade",
        template: "volume"
      };
    
    case "m":
    case "cm":
      return {
        campos: ["comprimento"],
        formula: "comprimento",
        template: "linear"
      };
    
    default:
      return { campos: [], template: "generico" };
  }
}

// 5. Cálculo automático
function calcularTotal(unidade, valores) {
  switch(unidade) {
    case "un":
      return valores.quantidade;
    
    case "m²":
      return (valores.largura * valores.altura) - valores.desconto;
    
    case "m³":
      return valores.comprimento * valores.altura * valores.profundidade;
    
    case "m":
      return valores.comprimento;
  }
}

// 6. Gerar tabela para preview
function gerarTabelaMemorial(item, registros) {
  return {
    titulo: `Item ${item.codigo} — ${item.descricao}`,
    unidade: item.unidade,
    linhas: registros.map(r => ({
      foto: r.numero,
      // Campos variam conforme unidade
      ...r.medidas,
      total: calcularTotal(item.unidade, r.medidas)
    })),
    total: registros.reduce((sum, r) => sum + calcularTotal(item.unidade, r.medidas), 0)
  };
}
```

---

## ESTRUTURA DE DADOS (JavaScript)

```javascript
// Estado de um bloco selecionado
const blocoSelecionado = {
  numero_foto: "01",
  item_codigo: "17.2",
  item_descricao: "Emassamento PVA",
  unidade: "m²",
  
  // Registros de medidas (um por foto)
  registros: [
    {
      numero_foto: "01",
      largura: 16.20,
      altura: 4.63,
      desconto: 0,
      // TOTAL calculado automaticamente:
      // total = (16.20 * 4.63) - 0 = 75.01
    },
    {
      numero_foto: "02",
      largura: 8.40,
      altura: 3.00,
      desconto: 0,
      // total = (8.40 * 3.00) - 0 = 25.20
    }
  ],
  
  // TOTAL consolidado (calculado automaticamente)
  total_consolidado: 100.21  // 75.01 + 25.20
}
```

---

## MAPEAMENTO: Excel → UNIDADE → FORMULÁRIO

```
Excel (importado)
├─ Item 17.2 — Emassamento PVA — m²
├─ Item 1.2 — Chamado — un
├─ Item 2.1 — Demolição concreto — m³
└─ Item 29.2 — Rodapé — m

Sistema (detecta unidade)
├─ m² → Formulário ÁREA
│  └─ Campos: Largura | Altura | Desconto
│     Cálculo: L × A - D
│
├─ un → Formulário CONTÁVEL
│  └─ Campos: Quantidade
│     Cálculo: Qtd
│
├─ m³ → Formulário VOLUME
│  └─ Campos: Comp | Altura | Prof
│     Cálculo: C × A × P
│
└─ m → Formulário LINEAR
   └─ Campos: Comprimento
      Cálculo: C

Saída no relatório
├─ Tabela EMASSAMENTO (5 colunas: FOTO | COMP | ALT | DESC | TOTAL)
├─ Tabela CHAMADO (3 colunas: FOTO | QTD | TOTAL)
├─ Tabela DEMOLIÇÃO (5 colunas: FOTO | COMP | ALT | PROF | TOTAL)
└─ Tabela RODAPÉ (3 colunas: FOTO | COMP | TOTAL)
```

---

## VALIDAÇÕES

Quando o usuário preenche os campos:

```javascript
function validarPreenchimento(registro, unidade) {
  const validacoes = {
    "m²": [
      { campo: "largura", minimo: 0.01, maximo: 999 },
      { campo: "altura", minimo: 0.01, maximo: 999 },
      { campo: "desconto", minimo: 0, maximo: 999 }
    ],
    "m³": [
      { campo: "comprimento", minimo: 0.01, maximo: 999 },
      { campo: "altura", minimo: 0.01, maximo: 999 },
      { campo: "profundidade", minimo: 0.01, maximo: 999 }
    ],
    "un": [
      { campo: "quantidade", minimo: 1, maximo: 99999 }
    ],
    "m": [
      { campo: "comprimento", minimo: 0.01, maximo: 999 }
    ]
  };
  
  return validacoes[unidade]?.every(v => 
    registro[v.campo] >= v.minimo && registro[v.campo] <= v.maximo
  );
}
```

---

## EXEMPLOS DE FLUXO REAL

### Exemplo 1: Emassamento (m²)

```
1. Usuário clica em [Foto 01]
   ↓
2. Sistema mostra dropdown de itens
   ├─ 17.2 — Emassamento PVA (m²)
   ├─ 17.11 — Pintura acrílica (m²)
   └─ ... (outros itens)
   ↓
3. Usuário seleciona: 17.2 — Emassamento PVA
   ↓
4. Sistema detecta unidade = "m²"
   ↓
5. Sistema exibe formulário:
   ┌─────────────────┐
   │ Foto: 01        │
   │ Largura: [__]m  │
   │ Altura: [__]m   │
   │ Desconto: [__]m² │
   │ TOTAL: 0.00 m²  │
   └─────────────────┘
   ↓
6. Usuário preenche:
   Largura: 16.20
   Altura: 4.63
   Desconto: 0
   ↓
7. Sistema calcula: 16.20 × 4.63 - 0 = 75.01 m²
   ↓
8. Preview atualiza com tabela:
   ┌─────────┬────────┬────────┬────────┬───────┐
   │REFERÊNCIA│COMP(m) │ALT(m)  │DES(m²) │TOT(m²)│
   ├─────────┼────────┼────────┼────────┼───────┤
   │Foto 01  │ 16.20  │ 4.63   │   0    │ 75.01 │
   └─────────┴────────┴────────┴────────┴───────┘
```

### Exemplo 2: Chamado (un — contável)

```
1. Usuário clica em [Foto 15]
   ↓
2. Sistema mostra dropdown
   ├─ 1.2 — Chamado (un)
   ├─ 1.3 — Revisão (un)
   └─ ...
   ↓
3. Usuário seleciona: 1.2 — Chamado
   ↓
4. Sistema detecta unidade = "un"
   ↓
5. Sistema exibe formulário simples:
   ┌──────────────────┐
   │ Foto: 15         │
   │ Quantidade: [__] │
   │ TOTAL: 0 un      │
   └──────────────────┘
   ↓
6. Usuário preenche:
   Quantidade: 3
   ↓
7. Sistema calcula: 3 un
   ↓
8. Preview atualiza:
   ┌──────────┬──────────┬────────┐
   │REFERÊNCIA│QUANTIDADE│TOT(un) │
   ├──────────┼──────────┼────────┤
   │Foto 15   │    3     │   3    │
   └──────────┴──────────┴────────┘
```

---

## CONSOLIDAÇÃO NO MEMORIAL

Quando há **múltiplas fotos do mesmo item**:

```
Foto 01: 75.01 m² (17.2 — Emassamento)
Foto 02: 25.20 m² (17.2 — Emassamento)

Sistema consolida em UMA tabela no memorial:

┌─────────┬────────┬────────┬────────┬───────┐
│REFERÊNCIA│COMP(m) │ALT(m)  │DES(m²) │TOT(m²)│
├─────────┼────────┼────────┼────────┼───────┤
│Foto 01  │ 16.20  │ 4.63   │   0    │ 75.01 │
│Foto 02  │  8.40  │ 3.00   │   0    │ 25.20 │
├─────────┼────────┼────────┼────────┼───────┤
│TOTAL    │        │        │        │100.21 │
└─────────┴────────┴────────┴────────┴───────┘

E linkado na tabela de itens:

┌───────────────────────────────────┐
│ Item 17.2 | Emassamento PVA | m²  │
│ Total consolidado: 100.21 m²      │
└───────────────────────────────────┘
```

---

## BENEFÍCIOS DESSA ABORDAGEM

✅ **Interface adaptativa** — Muda conforme a unidade  
✅ **Menos erros** — Cálculos automáticos  
✅ **Workflow natural** — Foto → Item → Medidas  
✅ **Memorial auto-gerado** — Tabelas preenchidas automaticamente  
✅ **Reutilizável** — 9 contratos, mesma lógica  
✅ **Validação integrada** — Valores realistas  

---

## IMPLEMENTAÇÃO: Próximas Etapas

1. **Atualizar HTML** — Adicionar seletor dinâmico de itens no passo 2
2. **Implementar parser** — Gerar `tabelaValores` do Excel
3. **Criar formulários dinâmicos** — conforme unidade
4. **Gerar tabelas** — Renderizar no preview conforme dados
5. **Consolidar memorial** — Agrupar múltiplas fotos do mesmo item

---

**Status:** Especificação completa, pronta para implementação  
**Próximo passo:** Desenvolvimento do seletor de itens + formulários dinâmicos

