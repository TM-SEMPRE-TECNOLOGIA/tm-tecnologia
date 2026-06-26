from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, UUID4


class StatusOS(str, Enum):
    aberta = "aberta"
    em_andamento = "em_andamento"
    concluida = "concluida"
    atrasada = "atrasada"
    cancelada = "cancelada"


class PrioridadeOS(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"


class TipoOS(str, Enum):
    corretiva = "corretiva"
    preventiva = "preventiva"
    preditiva = "preditiva"
    inspecao = "inspecao"


class RoleUsuario(str, Enum):
    manager = "manager"
    elaborador = "elaborador"
    contract_admin = "contract_admin"


# ── Contratos ──────────────────────────────────────────────

class ContratoBase(BaseModel):
    id: str  # "1565", "0908", etc.
    nome: str
    cliente: str
    modo: Optional[str] = None  # "tradicional", "sp", "sp2"


class Contrato(ContratoBase):
    ativo: bool = True


# ── Técnicos ───────────────────────────────────────────────

class TecnicoBase(BaseModel):
    nome: str
    email: Optional[str] = None
    especialidade: Optional[str] = None
    ativo: bool = True


class TecnicoCreate(TecnicoBase):
    pass


class Tecnico(TecnicoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Ordens de Serviço ─────────────────────────────────────

class OrdemServicoBase(BaseModel):
    numero_os: str
    titulo: str
    descricao: Optional[str] = None
    status: StatusOS = StatusOS.aberta
    prioridade: PrioridadeOS = PrioridadeOS.media
    tipo: TipoOS = TipoOS.corretiva
    contrato_id: str
    local: Optional[str] = None
    agencia: Optional[str] = None
    elaborador: Optional[str] = None
    tecnico: Optional[str] = None
    responsavel: Optional[str] = None
    tecnico_id: Optional[int] = None
    data_abertura: Optional[date] = None
    data_prazo: Optional[date] = None
    data_conclusao: Optional[date] = None
    observacoes: Optional[str] = None


class OrdemServicoCreate(OrdemServicoBase):
    pass


class OrdemServicoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusOS] = None
    prioridade: Optional[PrioridadeOS] = None
    tipo: Optional[TipoOS] = None
    local: Optional[str] = None
    agencia: Optional[str] = None
    elaborador: Optional[str] = None
    tecnico: Optional[str] = None
    responsavel: Optional[str] = None
    tecnico_id: Optional[int] = None
    data_prazo: Optional[date] = None
    data_conclusao: Optional[date] = None
    observacoes: Optional[str] = None


class OrdemServico(OrdemServicoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Notificações ──────────────────────────────────────────

class NotificacaoBase(BaseModel):
    titulo: str
    mensagem: str
    tipo: str = "info"  # info, warning, error, success
    os_id: Optional[int] = None
    lida: bool = False


class Notificacao(NotificacaoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Dificuldades ──────────────────────────────────────────

class DificuldadeBase(BaseModel):
    os_id: int
    descricao: str
    categoria: Optional[str] = None
    resolvida: bool = False


class DificuldadeCreate(DificuldadeBase):
    pass


class Dificuldade(DificuldadeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Importação Excel ──────────────────────────────────────

class ImportacaoResultado(BaseModel):
    total_linhas: int
    importadas: int
    ignoradas: int
    erros: List[str] = []
    ordens: List[dict] = []


# ── KPIs Dashboard ────────────────────────────────────────

class DashboardKPIs(BaseModel):
    total_os: int
    abertas: int
    em_andamento: int
    concluidas: int
    atrasadas: int
    taxa_conclusao: float
    vencendo_7_dias: int
    vencendo_30_dias: int = 0
    sla_cumprido_pct: Optional[float] = None
    contrato_id: Optional[str] = None
