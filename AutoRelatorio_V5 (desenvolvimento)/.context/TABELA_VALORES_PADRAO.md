# Padrão Genérico de Tabela de Valores — AutoRelatório V5

**Versão:** 1.0  
**Data:** 2026-05-22  
**Status:** Especificação de design

---

## 1. ESTRUTURA PADRÃO (9 Contratos)

Todos os 9 contratos **compartilham** a mesma tabela de valores, porém:
- **SP1 (0908) e SP2 (1565)**: Aba "Valores" ou "Valores Unitários" (tabela estruturada)
- **Tradicionais (outros 7)**: Planilha Thiago com estrutura similar

### Coluna Padrão
```
┌────┬──────────────────────┬──────┬────┬─────────┬─────────┬───────┐
│ A  │ B                    │ C    │ D  │ E       │ F       │ Total │
├────┼──────────────────────┼──────┼────┼─────────┼─────────┼───────┤
│ ID │ Descrição            │ Qtde │ UN │ Valor $ │ Mão Obra│ Geral │
├────┼──────────────────────┼──────┼────┼─────────┼─────────┼───────┤
│ 1  │ PRELIMINARES         │      │    │         │         │       │
│1.1 │ Chamado              │ 249  │ un │ 21.57   │ 86.69   │108.26 │
│1.2 │ Deslocamento         │299981│ km │ 1.66    │ 0.73    │  2.39 │
│...│ ...                  │ ... │...|  ...     │  ...    │  ...  │
└────┴──────────────────────┴──────┴────┴─────────┴─────────┴───────┘
```

---

## 2. MAPEAMENTO POR CONTRATO

### SP2 (Contrato 1565) — RAT Estruturado ✓
```
Arquivo: Modelo RAT - SP 1565.xlsx
Aba: "Valores Unitários"
Estrutura:
  Linha 7: Cabeçalho (ITEM | blank | QTDE | UN | UNITÁRIO MATERIAL | UNITÁRIO MÃO DE OBRA | ...)
  Linha 8+: Dados (código | descrição | quantidade | unidade | valores)
  
Campos chave:
  • Col A: Código do item (ex: 1, 1.1, 2.2)
  • Col B: Descrição (ex: "PRELIMINARES", "Chamado")
  • Col C: Quantidade numérica
  • Col D: Unidade (un, km, m², h, etc)
  • Col E: Valor unitário material
  • Col F: Valor unitário mão de obra
  • Col G: Total unitário
```

### SP1 (Contrato 0908) — RAT Simplificado
```
Arquivo: PREVISÃO ORÇAMENTÁRIA... SÃO PAULO.xlsx
Aba: "Valores"
Estrutura: IDÊNTICA ao SP2 (linha 7 = cabeçalho)
Diferença: Alguns campos preenchidos com fórmulas (=V9, =W9, etc)
```

### Tradicionais (Contratos 2056, 2057, 6122, 2626, 2627, 3575, 1507) — Planilha Thiago
```
Arquivo: Planilha de apoio preventivas - Thiago.xlsx
Abas: "Planilha de cálculo MEDIDAS", "Planilha de cálculo UNIDADE"

ABA 1: "Planilha de cálculo MEDIDAS"
  Linha 1: "MEMORIAL DE MEDIDAS (m²)"
  Linha 2: Cabeçalho (REFERÊNCIA | LARGURA | ALTURA | DESCONTO | TOTAL)
  Estrutura: Referência de foto + dimensões
  
EFERÊNCIA: "Foto 433", "Foto 434 a 437", etc
  Largura/Altura: Valores numéricos
  Total: Cálculo área (m²)
  
EXEMPLO:
  Foto 433       │ 2.0  │ 3.5 │ -    │ 7.0
  Foto 434a437   │ 5.7  │ 2.2 │ 0.5  │ 12.04

ABA 2: "Planilha de cálculo UNIDADE"
  Linha 1: "MEMORIAL DE UNIDADES COM (UN)"
  Linha 2: Cabeçalho (REFERÊNCIA | blank | QUANTIDADE)
  Estrutura: Contagem de itens por foto
  
EXEMPLO:
  Foto 434 a 437 │ │ 4
  Foto 445       │ │ 1
  Foto 450 a 462 │ │ 13
```

---

## 3. PARSER GENÉRICO (JavaScript + Python)

### Fluxo de Importação
```
1. Usuário seleciona arquivo .xlsx
2. Sistema detecta tipo (SP1/SP2/Tradicional)
3. Parser extrai tabela de valores
4. Dados alimentam campo "blocos" do relatorio{}
5. Frontend renderiza em tempo real
```

### Estrutura de Dados (JS Object)
```javascript
const tabela_valores = {
  contrato: "1565",
  modo: "SP2",
  items: [
    {
      id: "1",
      descricao: "PRELIMINARES",
      eh_titulo: true,
      quantidade: null,
      unidade: null,
      valor_material: null,
      valor_mao_obra: null
    },
    {
      id: "1.1",
      descricao: "Chamado",
      eh_titulo: false,
      quantidade: 249,
      unidade: "un",
      valor_material: 21.57,
      valor_mao_obra: 86.69,
      total: 108.26
    },
    // ... mais itens
  ]
}
```

---

## 4. PARSER PYTHON (Pseudo-código)

```python
def parse_valores_sp2(xlsx_path):
    """Extrai tabela de valores do RAT SP2 (1565, 0908)"""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["Valores Unitários"]  # ou "Valores"
    
    items = []
    for row in range(8, ws.max_row + 1):
        codigo = ws.cell(row, 1).value
        descricao = ws.cell(row, 2).value
        qty = ws.cell(row, 3).value
        unidade = ws.cell(row, 4).value
        valor_mat = ws.cell(row, 5).value
        valor_mao = ws.cell(row, 6).value
        
        if not codigo or not descricao:
            continue
            
        items.append({
            "id": str(codigo),
            "descricao": str(descricao),
            "eh_titulo": "." not in str(codigo),  # "1" = título, "1.1" = item
            "quantidade": float(qty) if qty else None,
            "unidade": str(unidade) if unidade else None,
            "valor_material": float(valor_mat) if valor_mat else None,
            "valor_mao_obra": float(valor_mao) if valor_mao else None,
            "total": float(valor_mat or 0) + float(valor_mao or 0)
        })
    
    return items

def parse_valores_tradicional(xlsx_path):
    """Extrai tabelas de medidas + unidades (Planilha Thiago)"""
    wb = openpyxl.load_workbook(xlsx_path)
    
    items = []
    
    # Aba 1: Medidas (m²)
    ws_medidas = wb["Planilha de cálculo MEDIDAS"]
    for row in range(3, ws_medidas.max_row + 1):
        referencia = ws_medidas.cell(row, 1).value
        largura = ws_medidas.cell(row, 2).value
        altura = ws_medidas.cell(row, 3).value
        desconto = ws_medidas.cell(row, 4).value
        total = ws_medidas.cell(row, 5).value
        
        if not referencia:
            continue
            
        items.append({
            "referencia": str(referencia),
            "tipo": "medida",
            "largura": float(largura) if largura else None,
            "altura": float(altura) if altura else None,
            "desconto": float(desconto) if desconto else 0,
            "total_m2": float(total) if total else None
        })
    
    # Aba 2: Unidades
    ws_unidades = wb["Planilha de cálculo UNIDADE"]
    for row in range(3, ws_unidades.max_row + 1):
        referencia = ws_unidades.cell(row, 1).value
        quantidade = ws_unidades.cell(row, 3).value
        
        if not referencia:
            continue
            
        # Buscar item correspondente e adicionar quantidade
        for item in items:
            if item["referencia"] == referencia:
                item["quantidade"] = int(quantidade) if quantidade else None
                item["tipo"] = "medida+unidade"
                break
    
    return items
```

---

## 5. INTEGRAÇÃO COM FRONTEND V5

### Passo 2: "Estrutura de Blocos"
```
[Modo Disco] [Modo App]

┌─────────────────────────────────────────┐
│ [Importar Planilha Excel]               │  ← Novo botão
│  Ou selecionar pasta de fotos           │
└─────────────────────────────────────────┘

BLOCOS DETECTADOS: 127
[1 PRELIMINARES]
  └─ [1.1 Chamado] — qty: 249, un
  └─ [1.2 Deslocamento] — qty: 299981, km
  └─ [1.3 Revisão de instalações] — qty: 151, un
```

### Preview DOCX (Bloco de Tabela)
```
┌──────┬─────────────────────────┬──────┬────┬─────┐
│Código│ Descrição               │ Qtde │ UN │Total│
├──────┼─────────────────────────┼──────┼────┼─────┤
│1.1   │ Chamado                 │ 249  │ un │$... │
│1.2   │ Deslocamento            │299981│ km │$... │
│1.3   │ Revisão de instalações  │ 151  │ un │$... │
└──────┴─────────────────────────┴──────┴────┴─────┘
```

---

## 6. CRITÉRIOS DE SUCESSO

| Critério | Target | Validação |
|----------|--------|-----------|
| **Cobertura** | 9/9 contratos | ✓ Testar importação em cada um |
| **Fidelidade tabela** | 99%+ linhas | ✓ Comparar célula por célula |
| **Performance** | <2s para 500 itens | ✓ Medir tempo de parse |
| **Validação dados** | 95%+ acurácia | ✓ Verificar tipos (qty, valores) |

---

## PRÓXIMOS PASSOS

1. **Parser Python** — Implementar funções de extração (SP2 + Tradicional)
2. **Importador JS** — UI para upload + preview de dados extraídos
3. **Validação** — Cruzar dados com documentos reais de 3+ contratos
4. **Integração** — Conectar parser ao bloco de "Estrutura" do V5

