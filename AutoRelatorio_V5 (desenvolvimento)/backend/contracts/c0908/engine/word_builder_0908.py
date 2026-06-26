# contracts/c0908/engine/word_builder_0908.py — Contrato 0908
# São Paulo / São José dos Campos — Word Builder Modo SP
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.

import sys
import pathlib

# Garante que core/ está no path
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from word_utils_sp import inserir_conteudo_sp as _inserir_conteudo_sp


def inserir_conteudo_sp(
    modelo_path: str,
    conteudo: list,
    output_path: str,
    meta: dict = None,
) -> str:
    """Interface V5 do word builder SP."""
    _inserir_conteudo_sp(
        modelo_path=modelo_path,
        conteudo=conteudo,
        output_path=output_path,
        meta=meta,
    )
    return output_path
