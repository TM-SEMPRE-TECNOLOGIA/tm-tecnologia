# core/registry.py — AutoRelatório V5
# Registro central de todos os contratos ativos
# Para adicionar um novo contrato: criar módulo em /contracts/cXXXX/ e registrar aqui.

from .contract_engine import ContractEngine

from contracts.c0908.engine.engine import Contract0908Engine
from contracts.c1507.engine.engine import Contract1507Engine
from contracts.c1565.engine.engine import Contract1565Engine
from contracts.c2056.engine.engine import Contract2056Engine
from contracts.c2057.engine.engine import Contract2057Engine
from contracts.c2626.engine.engine import Contract2626Engine
from contracts.c2627.engine.engine import Contract2627Engine
from contracts.c3575.engine.engine import Contract3575Engine
from contracts.c6122.engine.engine import Contract6122Engine

# Modos: "tradicional" | "sp" | "sp2"
# Cada engine implementa seu próprio scanner e word_builder.
# Mesmo que dois contratos sejam idênticos internamente, cada um tem seu módulo
# para permitir ajustes independentes (nome de arquivo, regras locais, etc.)

_ENGINES: dict[str, ContractEngine] = {
    "0908": Contract0908Engine(),
    "1507": Contract1507Engine(),
    "1565": Contract1565Engine(),   # SP2 — memória de cálculo
    "2056": Contract2056Engine(),
    "2057": Contract2057Engine(),
    "2626": Contract2626Engine(),
    "2627": Contract2627Engine(),
    "3575": Contract3575Engine(),
    "6122": Contract6122Engine(),
}

def get_engine(contract_id: str) -> ContractEngine:
    if contract_id not in _ENGINES:
        raise ValueError(f"Contrato '{contract_id}' não registrado. Disponíveis: {list(_ENGINES)}")
    return _ENGINES[contract_id]

def list_contracts() -> list[dict]:
    return [
        {
            "id": cid,
            "name": engine.contract_name,
            "template": engine.template_file,
            "generation_mode": engine.generation_mode,
            "reading_modes": engine.reading_modes,
        }
        for cid, engine in _ENGINES.items()
    ]
