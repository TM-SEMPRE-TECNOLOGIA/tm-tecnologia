# 🚀 Próximo Passo — AutoRelatório V5
## Guia Executivo para Sprint 3
> Atualizado: 2026-05-26

---

## Estado atual (resumo em 1 linha)
Backend 100% funcional. Frontend 90%. **Único gap crítico:** fotos do browser não chegam ao backend.

---

## O QUE FAZER AGORA (por ordem de prioridade)

### 🔴 P1 — Sprint 3: Upload Fotos via Multipart

**Problema:** O browser não pode fornecer `root_path` ao backend. Com `root_path` vazio, o `/generate` gera `.docx` só com cabeçalho — sem fotos.

**Solução:** Enviar as imagens via `multipart/form-data`.

#### Backend — novo endpoint
```python
# Adicionar em core/server.py:
from fastapi import UploadFile, File, Form
from typing import List

@app.post("/api/contracts/{contract_id}/generate-with-files")
async def generate_with_files(
    contract_id: str,
    nr_os: str = Form(...),
    ag_cod: str = Form(...),
    ag_nome: str = Form(...),
    dt_atend: str = Form(...),
    endereco: str = Form(""),
    responsavel: str = Form(""),
    desc_index: str = Form("1"),
    files: List[UploadFile] = File(default=[]),
):
    import tempfile, os, shutil
    engine = get_engine(contract_id)
    
    # Salvar arquivos em pasta temp com estrutura original
    with tempfile.TemporaryDirectory() as tmp_dir:
        for f in files:
            # f.filename inclui o caminho relativo (webkitdirectory preserva isso)
            dest = os.path.join(tmp_dir, f.filename)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'wb') as out:
                out.write(await f.read())
        
        meta = { "nr_os": nr_os, "ag_cod": ag_cod, ... }
        conteudo = engine.scan(tmp_dir)
        output = engine.build_word(str(tpl), conteudo, output_path, meta)
    
    return FileResponse(output, filename=f"Relatorio-OS{nr_os}.docx")
```

#### Frontend — enviar via FormData
```typescript
// Em lib/api.ts, adicionar:
export async function generateWithFiles(
  payload: GeneratePayload,
  files: File[]
): Promise<GenerateResponse> {
  const form = new FormData();
  form.append('nr_os', payload.nr_os);
  form.append('ag_cod', payload.ag_cod);
  // ... outros campos
  for (const f of files) {
    form.append('files', f, f.webkitRelativePath || f.name);
  }
  
  const res = await fetch(`${BASE_URL}/api/contracts/${payload.contrato_id}/generate-with-files`, {
    method: 'POST',
    body: form,  // NÃO colocar Content-Type — browser define boundary automático
  });
  // ... tratar FileResponse igual requestFile()
}
```

**Em useBlocks.ts:** os `File[]` originais do webkitdirectory já estão disponíveis — só passar para a nova função.

---

### 🟡 P2 — Testar Contratos Tradicionais

Os 7 contratos tradicionais (1507, 2056, 2057, 2626, 2627, 3575, 6122) têm engine migrado mas **não foram testados no V5**.

**Como testar:**
```bash
cd backend
python -c "
from contracts.c1507.engine.engine import Contract1507Engine
e = Contract1507Engine()
conteudo = e.scan(r'C:\caminho\para\pasta\de\fotos')
tpl = r'contracts/c1507/template/MODELO-1507.docx'
e.build_word(tpl, conteudo, r'output/teste-1507.docx', {'nr_os':'0001','ag_cod':'1234','ag_nome':'Teste','dt_atend':'01/01/2026','dt_elab':'26/05/2026'})
print('OK')
"
```

---

### 🟡 P3 — items.json para c2056, c2057, c6122

Esses 3 contratos têm `items.json` vazio. O dropdown de itens aparece vazio no Step 2.

**Precisam:** planilhas de itens do Thiago para Divinópolis, Varginha e Mato Grosso do Sul.

**Formato esperado** (ver c1507/items/items.json como referência):
```json
{
  "17.7": { "id": "17.7", "desc": "Pintura látex PVA", "un": "m²" },
  "17.10": { "id": "17.10", "desc": "Repintura teto", "un": "m²" }
}
```

---

### 🟡 P4 — Detecção Automática de Medidas

O useBlocks já extrai número sequencial do arquivo. Próximo passo: parsear medidas do nome.

**A função já existe em `core/utils_sp.py`:**
```python
from core.utils_sp import parse_medidas_arquivo
resultado = parse_medidas_arquivo("01 - 3,50 x 2,80.jpg")
# → { 'largura': 3.5, 'altura': 2.8, 'desconto': 0.0, 'total': 9.8, ... }
```

**No frontend (useBlocks.ts):** expor via endpoint ou re-implementar o parser em TypeScript:
```typescript
function parseMedidasNome(filename: string) {
  // "01 - 3,50 x 2,80.jpg" → { largura: 3.5, altura: 2.8 }
  const m = filename.match(/(\d+[,\.]\d+)\s*x\s*(\d+[,\.]\d+)/i);
  if (!m) return null;
  return {
    largura: parseFloat(m[1].replace(',', '.')),
    altura:  parseFloat(m[2].replace(',', '.')),
  };
}
```

---

## CHECKLIST DE SAÚDE DO SISTEMA

Antes de qualquer nova feature, verificar:

- [ ] `python -m uvicorn core.server:app --port 5000` inicia sem erro
- [ ] `GET http://localhost:5000/health` retorna `{"status":"ok","version":"5.0.0"}`
- [ ] `npm run dev` na pasta frontend inicia sem erro
- [ ] `http://localhost:3000` carrega a UI
- [ ] Botão "Verificar Backend" mostra toast verde
- [ ] Step 1: preencher OS + agência → Step 2 acessível
- [ ] Step 2: selecionar pasta de fotos → thumbnails aparecem
- [ ] Step 3: botão Gerar → download .docx com cabeçalho

---

## REFERÊNCIAS RÁPIDAS

| O que procurar | Onde está |
|----------------|-----------|
| Adicionar novo contrato | `registry.py` + criar `contracts/cXXXX/` |
| Mudar lógica de sort | `scanner.py` em qualquer engine trad |
| Mudar formato de tabela SP2 | `core/word_utils_sp2.py` |
| Adicionar placeholder novo | `core/word_utils.py` EXPECTED_PLACEHOLDERS |
| Lógica de medidas SP | `core/utils_sp.py::parse_medidas_arquivo` |
| Lógica de medidas SP2 | `core/utils_sp2.py::parse_medidas_sp2` |
| Estrutura de engine | `core/contract_engine.py` (ABC) |
| Todos os endpoints | `core/server.py` |
| Tipos TypeScript | `frontend/lib/api.ts` |
| Estado de blocos | `frontend/hooks/useBlocks.ts` |

---

*AutoRelatório V5 — 2026-05-26*
