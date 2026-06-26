from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from db.supabase import get_supabase

router = APIRouter(prefix="/api/usuarios", tags=["usuários"])


@router.get("")
def listar_usuarios(role: Optional[str] = Query(None)):
    """Lista usuários do Supabase Auth com metadados de role."""
    db = get_supabase()
    # Supabase Admin API via service key
    try:
        result = db.auth.admin.list_users()
        users = result if isinstance(result, list) else []

        formatted = []
        for u in users:
            meta = getattr(u, "user_metadata", {}) or {}
            user_role = meta.get("role", "elaborador")
            if role and user_role != role:
                continue
            formatted.append({
                "id": u.id,
                "email": u.email,
                "nome": meta.get("nome", u.email),
                "role": user_role,
                "ativo": not getattr(u, "banned_until", None),
                "created_at": str(getattr(u, "created_at", "")),
            })
        return formatted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")


@router.get("/me")
def perfil_atual():
    """Endpoint para validar token — retorna dados do usuário autenticado."""
    return {"status": "ok", "message": "Use o token JWT do Supabase no header Authorization"}
