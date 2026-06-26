# contracts/c1565/engine/word_builder_1565.py — Contrato 1565
# São José do Rio Preto / Ribeirão Preto — Word Builder Modo SP2
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.
#
# O V4 usava imports planos (from word_utils import ..., from utils_sp2 import ...).
# No V5, os utilitários ficam em core/. Este wrapper garante que os imports
# do core/word_utils_sp2.py funcionem corretamente via sys.path.
#
# Interface esperada pelo engine.py:
#   inserir_conteudo_sp2(modelo_path, conteudo, output_path, meta) -> str

import sys
import pathlib

# Garante que core/ está no path para os imports do word_utils_sp2.py
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

# Importa a função real do core/
from word_utils_sp2 import inserir_conteudo_sp2 as _inserir_conteudo_sp2


def inserir_conteudo_sp2(
    modelo_path: str,
    conteudo: list,
    output_path: str,
    meta: dict = None,
) -> str:
    """
    Interface V5 do word builder SP2.

    Adapta o retorno do V4 (int = total de imagens inseridas) para a interface
    do ContractEngine.build_word() que espera str (output_path).
    """
    _inserir_conteudo_sp2(
        modelo_path=modelo_path,
        conteudo=conteudo,
        output_path=output_path,
        meta=meta,
    )
    return output_path
