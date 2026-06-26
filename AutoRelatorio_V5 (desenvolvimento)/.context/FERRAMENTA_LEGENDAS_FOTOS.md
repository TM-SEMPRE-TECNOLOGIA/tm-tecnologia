# Ferramenta: Inserir e Corrigir Legendas de Fotos em .docx

**Data:** 2026-05-27  
**Status:** Scripts prontos e testados (contrato 2057 - Ipuiuna)  
**Integração V5:** Pendente — referência para futura feature no app

---

## O QUE FAZ

Insere `Foto 1`, `Foto 2`, ... abaixo de cada imagem em relatórios .docx preventivos.  
Detecta imagens em parágrafos soltos **e** em células de tabela (layout colunar).

Existe também script de **correção de sequência**: quando o usuário edita o documento manualmente e a numeração quebra, o script renumera tudo e reporta onde estava quebrado.

---

## SCRIPTS PRONTOS

**Localização:** `C:\Users\thiag\Desktop\tm-tecnologia\_workspace\scripts\python\`

### 1. `inserir_legendas_simples.py`
Insere legendas onde não existem.

```powershell
python inserir_legendas_simples.py "arquivo.docx"
# → gera arquivo_LEGENDADO.docx
```

**Lógica:**
- Percorre `body` em ordem de aparição (parágrafos + tabelas)
- Para cada parágrafo com imagem (`a:blip`), verifica se o próximo já é `Foto \d`
- Se não, insere `Foto N` centralizado abaixo da imagem
- Numera de trás para frente (para não deslocar posições no XML)

**Resultado no Ipuiuna (547 imagens totais):** 182 legendas inseridas (1 por parágrafo/slot de imagem)

### 2. `corrigir_sequencia_legendas.py`
Renumera legendas existentes em sequência correta.

```powershell
python corrigir_sequencia_legendas.py "arquivo_LEGENDADO.docx"
# → gera arquivo_LEGENDADO_CORRIGIDO.docx
# → imprime onde havia quebras de sequência
```

**Output exemplo:**
```
Legendas encontradas: 182
⚠️  Quebras de sequência detectadas (2):
   Posição 45: após Foto 44 veio Foto 48 (esperado Foto 45)
   Posição 89: após Foto 88 veio Foto 91 (esperado Foto 89)
Legendas renumeradas: 7 alterações
Sequência final: Foto 1 a Foto 182
```

---

## SKILL CLAUDE CODE

**Path:** `C:\Users\thiag\.claude\skills\legendar-fotos.md`  
**Trigger:** `/legendar-fotos` ou quando usuário mencionar "legendar fotos", "inserir legendas", "corrigir sequência"

---

## COMO INTEGRAR AO AUTORELATORIO V5

### Opção A — Botão "Legendar Fotos" na tela de processamento
1. Frontend envia path do .docx para endpoint FastAPI
2. Backend chama `inserir_legendas_simples.py` como subprocess
3. Retorna path do `_LEGENDADO.docx` para download

### Opção B — Função Python direta no backend
Importar `inserir_legendas` e `corrigir_sequencia` como módulos:

```python
from scripts.inserir_legendas_simples import inserir_legendas
from scripts.corrigir_sequencia_legendas import corrigir_sequencia

# Inserir
inserir_legendas(input_path, output_path)

# Corrigir
corrigir_sequencia(input_path, output_path)
```

### Endpoint sugerido (FastAPI)
```python
@router.post("/legendas/inserir")
async def inserir_legendas_endpoint(file: UploadFile):
    # salva temp, processa, retorna arquivo legendado
    ...

@router.post("/legendas/corrigir")
async def corrigir_legendas_endpoint(file: UploadFile):
    # salva temp, processa, retorna arquivo corrigido com relatório de quebras
    ...
```

---

## CONTRATOS QUE USAM

- **Contrato 2057 (Ipuiuna)** — testado e validado ✅
- Aplicável a qualquer relatório preventivo .docx com imagens em tabelas

---

## REFERÊNCIA TÉCNICA

**Detecção de imagem:** XPath `a:blip` no namespace DrawingML  
**Detecção de legenda:** regex `^\s*Foto\s*\d+\s*$`  
**Inserção:** `elem.addnext(make_caption_para(n))` — XML direto, sem python-docx API  
**Formato:** parágrafo centralizado, sem negrito, texto `Foto N`  
**Dependência:** `python-docx` (já no ambiente do projeto)
