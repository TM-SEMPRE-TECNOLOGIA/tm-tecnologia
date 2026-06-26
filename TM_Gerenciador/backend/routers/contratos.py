from fastapi import APIRouter, HTTPException
from typing import List
import httpx

from models.schemas import Contrato

router = APIRouter(prefix="/api/contratos", tags=["contratos"])

# Os 9 contratos bancários TM — espelha o AutoRelatório V5
CONTRATOS: list[Contrato] = [
    Contrato(id="0908", nome="Agências BB – Lote 0908", cliente="Banco do Brasil", modo="tradicional"),
    Contrato(id="1507", nome="Agências BB – Lote 1507", cliente="Banco do Brasil", modo="tradicional"),
    Contrato(id="1565", nome="Agências BB – S.J.R.Preto", cliente="Banco do Brasil", modo="sp2"),
    Contrato(id="2056", nome="Agências BB – Lote 2056", cliente="Banco do Brasil", modo="tradicional"),
    Contrato(id="2057", nome="Agências BB – Lote 2057", cliente="Banco do Brasil", modo="tradicional"),
    Contrato(id="2626", nome="Agências BB – Lote 2626", cliente="Banco do Brasil", modo="sp"),
    Contrato(id="2627", nome="Agências BB – Lote 2627", cliente="Banco do Brasil", modo="sp"),
    Contrato(id="3575", nome="Agências BB – Lote 3575", cliente="Banco do Brasil", modo="tradicional"),
    Contrato(id="6122", nome="Agências BB – Lote 6122", cliente="Banco do Brasil", modo="tradicional"),
]

CONTRATOS_MAP = {c.id: c for c in CONTRATOS}


@router.get("", response_model=List[Contrato])
def listar_contratos():
    return CONTRATOS


@router.get("/{contrato_id}", response_model=Contrato)
def obter_contrato(contrato_id: str):
    contrato = CONTRATOS_MAP.get(contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail=f"Contrato {contrato_id} não encontrado")
    return contrato


@router.get("/{contrato_id}/items")
async def listar_items_contrato(contrato_id: str):
    """Proxy para o AutoRelatório V5 — retorna banco de itens do contrato."""
    if contrato_id not in CONTRATOS_MAP:
        raise HTTPException(status_code=404, detail=f"Contrato {contrato_id} não encontrado")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"http://localhost:5000/api/contracts/{contrato_id}/items")
            resp.raise_for_status()
            return resp.json()
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="AutoRelatório V5 não está acessível em localhost:5000. Inicie o app para usar esta rota."
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
