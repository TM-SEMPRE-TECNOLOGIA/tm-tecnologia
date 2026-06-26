# Integração: AutoRelatório V5 ↔ /relatorio-preventivo Skill

**Data:** 2026-05-23  
**Contexto:** Como conectar o frontend V5 com a skill de geração de memoriais  
**Status:** Especificação de arquitetura

---

## VISÃO GERAL DO FLUXO

```
┌──────────────────────────────────┐
│  AutoRelatório V5 (Frontend)     │
│  • Upload planilha               │
│  • Cabeçalho + estrutura         │
│  • Seleção de fotos              │
└──────────────┬───────────────────┘
               │ Gera JSON
               ▼
        ┌─────────────────────┐
        │ Arquivo JSON:       │
        │ relatorio.json      │
        │ {                   │
        │   contrato: "1565", │
        │   cabecalho: {...}, │
        │   blocos: [...],    │
        │   memoriais: {      │
        │     itens: [...]    │
        │   }                 │
        │ }                   │
        └─────────┬───────────┘
                  │ Passa para skill
                  ▼
    ┌──────────────────────────────────┐
    │ /relatorio-preventivo Skill      │
    │ (4 Etapas)                       │
    │                                  │
    │ 1. Extrair itens → Excel         │
    │ 2. Gerar memorial → Word         │
    │ 3. Validar divergencias          │
    │ 4. Validar legendas de fotos     │
    │                                  │
    └─────────────┬────────────────────┘
                  │
                  ▼
    ┌──────────────────────────────────┐
    │ Outputs Finais:                  │
    │ • Memorial_Final.docx            │
    │ • Itens_Extraidos.xlsx           │
    │ • Validacoes.txt                 │
    │ • Relatorio_Completo.docx        │
    └──────────────────────────────────┘
```

---

## 1. ESTRUTURA JSON (Output do V5 Frontend)

```javascript
{
  // Metadados
  versao: "V5",
  timestamp: "2026-05-23T14:30:00Z",
  
  // Contrato
  contrato: {
    id: "1565",
    nome: "São José do Rio Preto",
    modo: "SP2",  // "SP2" ou "Tradicional"
    uf: "SP"
  },
  
  // Cabeçalho do relatório
  cabecalho: {
    nr_os: "1753",
    dt_atendimento: "2026-05-21",
    agencia_cod: "1234-5",
    agencia_nome: "Ag. Centro",
    endereco: "Rua das Flores, 100 — São José do Rio Preto/SP",
    responsavel_dependencia: "Mat. 12345 — João Silva",
    descricao_servico: "Levantamento Preventivo"
  },
  
  // Blocos de conteúdo (estrutura de relatório)
  blocos: [
    {
      tipo: "titulo",
      nivel: 1,
      conteudo: "1 — 1º Andar – Espaço Desativado"
    },
    {
      tipo: "subtitulo",
      nivel: 2,
      conteudo: "1.1 — Emassamento e pintura de teto"
    },
    {
      tipo: "imagem",
      numero: "01",
      descricao: "16,20 × 4,63.jpg",
      caminho: "/fotos/01.jpg",
      medidas: { largura: 16.20, altura: 4.63 }
    },
    {
      tipo: "tabela_calc",
      item_codigo: "17.2",
      item_descricao: "Emassamento PVA (m²)",
      tabela: [
        { foto: "01", comp: 16.20, alt: 4.63, desconto: 0, total: 75.01 },
        { foto: "02", comp: 8.40, alt: 3.00, desconto: 0, total: 25.20 }
      ],
      total: 100.21,
      unidade: "m²"
    }
    // ... mais blocos
  ],
  
  // Dados para memorial final (IMPORTANTE)
  memoriais: {
    tipo_memorial: "Thiago",  // "Thiago" ou "SP"
    
    // Se Thiago: duas abas separadas
    medidas: [
      {
        referencia: "Foto 01",
        largura: 16.20,
        altura: 4.63,
        desconto: 0,
        total_m2: 75.01
      },
      // ... mais medidas
    ],
    
    unidades: [
      {
        referencia: "Foto 434 a 437",
        quantidade: 4
      },
      // ... mais unidades
    ],
    
    // Se SP: consolidação de itens
    itens_consolidados: [
      {
        codigo: "17.2",
        descricao: "Emassamento PVA",
        total: 100.21,
        unidade: "m²"
      },
      // ... mais itens
    ]
  },
  
  // Validações (opcional)
  validacoes: {
    fotos_completas: true,
    legendas_sequenciais: true,
    divergencias: []
  }
}
```

---

## 2. DOIS TIPOS DE MEMORIAL

### TIPO 1: Thiago (Universal para Tradicionais)

**Planilhas geradas:**
```
Planilha de apoio preventivas - Thiago.xlsx
├─ Aba 1: "Planilha de cálculo MEDIDAS"
│  ├─ REFERÊNCIA (Foto X)
│  ├─ LARGURA (m)
│  ├─ ALTURA (m)
│  ├─ DESCONTO (m²)
│  └─ TOTAL (m²)
│
└─ Aba 2: "Planilha de cálculo UNIDADE"
   ├─ REFERÊNCIA (Foto X)
   ├─ REFERÊNCIA (item)
   └─ QUANTIDADE (un)
```

**Dados necessários do V5:**
```javascript
memoriais: {
  tipo_memorial: "Thiago",
  
  medidas: [
    { referencia: "Foto 433", largura: 2.0, altura: 4.5, desconto: 0, total_m2: 9.0 },
    { referencia: "Foto 434", largura: 5.7, altura: 3.0, desconto: 0, total_m2: 17.1 },
    // ...
  ],
  
  unidades: [
    { referencia: "Foto 434 a 437", quantidade: 4 },
    { referencia: "Foto 445", quantidade: 1 },
    // ...
  ]
}
```

### TIPO 2: SP (São Paulo — SP1 e SP2)

**Planilhas geradas:**
```
MEMORIAL DE CÁLCULO - SÃO PAULO.xlsx
├─ Aba 1: "Memorial de cálculo"
│  ├─ Item (código)
│  ├─ Foto
│  ├─ Comp. (m)
│  ├─ Altura (m)
│  ├─ Desconto (m²)
│  └─ TOTAL (m²)
│
└─ Aba 2: "Itens"
   ├─ ITEM
   ├─ DESCRIÇÃO
   ├─ QTDE
   ├─ UN.
   └─ VALORES (Material + Mão de Obra)
```

**Dados necessários do V5:**
```javascript
memoriais: {
  tipo_memorial: "SP",
  
  itens_consolidados: [
    {
      codigo: "17.2",
      descricao: "Emassamento PVA",
      quantidade: 100.21,
      unidade: "m²",
      valor_material: 21.57,
      valor_mao_obra: 86.69
    },
    // ...
  ]
}
```

---

## 3. INTEGRAÇÃO COM /relatorio-preventivo

### Entrada para a Skill

A skill espera:
1. **Arquivo JSON** (estrutura acima)
2. **Pasta de fotos** (validação de imagens)
3. **Tipo de contrato** (determina formato do memorial)

### Processamento (4 Etapas)

```python
# Pseudo-código da skill
def processar_relatorio(json_path, fotos_dir, contrato_id):
    
    # Etapa 1: Extrair lista de itens
    itens_xlsx = extrair_itens_para_excel(json_path)
    
    # Etapa 2: Gerar memorial final
    if contrato_id in ["1565", "0908"]:  # SP
        memorial_docx = gerar_memorial_sp(json_path)
    else:  # Tradicional
        memorial_docx = gerar_memorial_thiago(json_path)
    
    # Etapa 3: Verificar divergências
    divergencias = verificar_divergencias(json_path, memorial_docx)
    
    # Etapa 4: Verificar legendas
    legendas_ok = verificar_legendas_fotos(fotos_dir, json_path)
    
    return {
        "itens": itens_xlsx,
        "memorial": memorial_docx,
        "divergencias": divergencias,
        "legendas": legendas_ok
    }
```

### Saída para o Usuário

```
✅ Relatório processado com sucesso!

Arquivos gerados:
  • Memorial_Final_1565.docx (86 KB)
  • Itens_1565.xlsx (45 KB)
  • Validacoes_1565.txt (2 KB)

Validações:
  ✅ Fotos sequenciadas corretamente
  ✅ Não há divergências entre corpo e memorial
  ✅ Todas as legendas presentes
```

---

## 4. MAPEAMENTO CONTRATO → TIPO MEMORIAL

| Contrato | ID   | Modo | Tipo Memorial | Planilha Padrão |
|----------|------|------|---------------|-----------------|
| SJRP     | 1565 | SP2  | SP            | MEMORIAL DE CÁLCULO - SÃO PAULO.xlsx |
| São Paulo| 0908 | SP1  | SP            | MEMORIAL DE CÁLCULO - SÃO PAULO.xlsx |
| Divinópolis | 2056 | Trad | Thiago   | Planilha de apoio preventivas - Thiago.xlsx |
| Varginha | 2057 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |
| MS       | 6122 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |
| Salinas  | 2626 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |
| Valadares| 2627 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |
| Tangará  | 3575 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |
| Cuiabá   | 1507 | Trad | Thiago       | Planilha de apoio preventivas - Thiago.xlsx |

---

## 5. IMPLEMENTAÇÃO: Passo a Passo

### Passo 1: V5 Frontend - Gerar JSON
```javascript
// No botão "Gerar .docx" do passo 3
function generateReport() {
  const relatorioJSON = {
    versao: "V5",
    contrato: { id: currentContract.id, modo: currentContract.mode },
    cabecalho: { /* campos do form */ },
    blocos: [ /* estrutura detectada */ ],
    memoriais: { 
      tipo_memorial: getMemoralType(currentContract.id),
      medidas: [ /* extraído do Excel */ ],
      unidades: [ /* extraído do Excel */ ]
    }
  };
  
  // Salvar ou enviar para /relatorio-preventivo
  downloadJSON(relatorioJSON, `relatorio_${currentContract.id}.json`);
  // OU chamar skill: invokeSkilll("relatorio-preventivo", relatorioJSON)
}
```

### Passo 2: Skill - Processar JSON
```bash
/relatorio-preventivo relatorio_1565.json --modo full
# Gera: Memorial_Final.docx, Itens.xlsx, Validacoes.txt
```

### Passo 3: Output
```
✅ Relatório gerado com sucesso
📄 Memorial_Final_1565.docx
📊 Itens_Consolidados_1565.xlsx
✓ Validacoes_OK
```

---

## 6. BENEFÍCIOS DESSA ARQUITETURA

✅ **Separação clara de responsabilidades**
  - V5: UI + captura de dados
  - Skill: processamento + validação

✅ **Reutilização**
  - Mesma skill para todos os 9 contratos
  - Mesmo JSON para múltiplos formatos de saída

✅ **Validação centralizada**
  - Divergências, legendas, sequência de fotos
  - Tudo verificado antes de gerar DOCX final

✅ **Extensibilidade**
  - Novos tipos de memorial? Adicionar parser
  - Novas validações? Adicionar etapa 5, 6...

---

## PRÓXIMOS PASSOS

1. **Implementar gerador JSON no V5** (passo 3)
2. **Testar JSON com skill** (1 contrato de cada tipo)
3. **Validar memoriais gerados** (comparar com originals)
4. **Documentar em validation.md** (PREVC)
5. **Atualizar diario_de_dev.md** (PREVC)

---

**Status PREVC:** Planning ✅ | Review ⏳ | Execution ⏳ | Validation ⏳ | Confirmation ⏳

