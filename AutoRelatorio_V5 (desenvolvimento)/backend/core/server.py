# core/server.py — AutoRelatório V5
# FastAPI principal — rotas por contrato
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from .registry import get_engine, list_contracts

VERSION = "5.0.0"

app = FastAPI(title="AutoRelatório V5 API", version=VERSION)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Request Models ────────────────────────────────────────────────────────────

class ScanRequest(BaseModel):
    root_path: str
    reading_mode: str = "disco"

class GenerateRequest(BaseModel):
    root_path: str
    output_path: str
    conteudo: list
    meta: dict
    annotated_images: Optional[dict] = None

class GenerateFlatRequest(BaseModel):
    """Payload flat enviado pelo frontend (lib/api.ts → generateReport())."""
    contrato_id:   str
    nr_os:         str
    ag_cod:        str
    ag_nome:       str
    dt_atend:      str
    endereco:      Optional[str] = ""
    responsavel:   Optional[str] = ""
    desc_index:    Optional[str] = "1"
    modo:          Optional[str] = "sp2"
    root_path:     Optional[str] = ""   # pasta de fotos (pode vir do frontend)

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Verifica saúde do backend — usado pelo frontend via checkHealth()."""
    return {"status": "ok", "version": VERSION}

@app.post("/generate")
def generate_flat(body: GenerateFlatRequest):
    """
    Endpoint de geração direta — aceita o payload flat do frontend.
    Fluxo: scan(root_path) → build_word() → retorna FileResponse.
    """
    import os, pathlib, tempfile, datetime

    engine = get_engine(body.contrato_id)

    # Monta o meta para substituição de placeholders no template
    meta = {
        "nr_os":                   body.nr_os,
        "ag_cod":                  body.ag_cod,
        "ag_nome":                 body.ag_nome,
        "dt_atend":                body.dt_atend,
        "endereco":                body.endereco or "",
        "responsavel_dependencia": body.responsavel or "",
        "dt_elab":                 datetime.date.today().strftime("%d/%m/%Y"),
    }

    # Scan da pasta de fotos (se fornecida)
    conteudo: list = []
    if body.root_path and os.path.isdir(body.root_path):
        validation = engine.validate_folder(body.root_path)
        if not validation.valid:
            raise HTTPException(422, detail={"errors": validation.errors})
        conteudo = engine.scan(body.root_path)

    # Template do contrato
    tpl = (
        pathlib.Path(__file__).parent.parent
        / "contracts" / f"c{body.contrato_id}"
        / "template" / engine.template_file
    )
    if not tpl.exists():
        raise HTTPException(500, detail=f"Template não encontrado: {tpl}")

    # Output temporário
    out_dir = pathlib.Path(__file__).parent.parent / "output"
    out_dir.mkdir(exist_ok=True)
    filename = f"Relatorio-OS{body.nr_os}-{body.ag_cod}.docx"
    output_path = str(out_dir / filename)

    output = engine.build_word(str(tpl), conteudo, output_path, meta)
    return FileResponse(output, filename=filename, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

@app.get("/api/contracts")
def api_list_contracts():
    return list_contracts()

@app.get("/api/contracts/{contract_id}")
def api_get_contract(contract_id: str):
    engine = get_engine(contract_id)
    return {
        "id": contract_id,
        "name": engine.contract_name,
        "template": engine.template_file,
        "reading_modes": engine.reading_modes,
        "meta_fields": [f.__dict__ for f in engine.get_meta_fields()],
    }

@app.post("/api/contracts/{contract_id}/scan")
def api_scan(contract_id: str, body: ScanRequest):
    engine = get_engine(contract_id)
    validation = engine.validate_folder(body.root_path)
    if not validation.valid:
        raise HTTPException(422, detail={"errors": validation.errors})
    conteudo = engine.scan(body.root_path)
    return {"conteudo": conteudo, "warnings": validation.warnings}

@app.post("/api/contracts/{contract_id}/generate")
def api_generate(contract_id: str, body: GenerateRequest):
    import os, pathlib
    engine = get_engine(contract_id)
    tpl = pathlib.Path(__file__).parent.parent / "contracts" / f"c{contract_id}" / "template" / engine.template_file
    output = engine.build_word(str(tpl), body.conteudo, body.output_path, body.meta)
    return FileResponse(output, filename=os.path.basename(output))

@app.post("/api/contracts/{contract_id}/validate")
def api_validate(contract_id: str, body: ScanRequest):
    engine = get_engine(contract_id)
    result = engine.validate_folder(body.root_path)
    return result.__dict__

@app.get("/api/contracts/{contract_id}/items")
def api_get_items(contract_id: str):
    engine = get_engine(contract_id)
    return engine.get_items()

if __name__ == "__main__":
    uvicorn.run("core.server:app", host="0.0.0.0", port=5000, reload=True)
