from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from db.supabase import get_supabase
from models.schemas import Notificacao

router = APIRouter(prefix="/api/notificacoes", tags=["notificações"])

TABLE = "notificacoes"


@router.get("", response_model=List[dict])
def listar_notificacoes(
    lida: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
):
    db = get_supabase()
    q = db.table(TABLE).select("*")

    if lida is not None:
        q = q.eq("lida", lida)

    offset = (page - 1) * per_page
    q = q.order("created_at", desc=True).range(offset, offset + per_page - 1)

    result = q.execute()
    return result.data or []


@router.get("/count-nao-lidas")
def count_nao_lidas():
    db = get_supabase()
    result = db.table(TABLE).select("id", count="exact").eq("lida", False).execute()
    return {"count": result.count or 0}


@router.patch("/{notif_id}/lida")
def marcar_como_lida(notif_id: int):
    db = get_supabase()
    result = db.table(TABLE).update({"lida": True}).eq("id", notif_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return result.data[0]


@router.patch("/marcar-todas-lidas")
def marcar_todas_lidas():
    db = get_supabase()
    db.table(TABLE).update({"lida": True}).eq("lida", False).execute()
    return {"ok": True}


@router.delete("/{notif_id}", status_code=204)
def deletar_notificacao(notif_id: int):
    db = get_supabase()
    db.table(TABLE).delete().eq("id", notif_id).execute()
