# contracts/c1565/engine/scanner_1565.py — Contrato 1565
# São José do Rio Preto / Ribeirão Preto — Scanner Modo SP2
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.
#
# O V4 usava imports planos (from utils_sp2 import ...).
# No V5, os utilitários ficam em core/ e os engines em contracts/cXXXX/engine/.
# Este arquivo redireciona sys.path para que o generator_sp2.py (copiado do V4)
# possa encontrar os módulos de core/.
#
# Interface esperada pelo engine.py:
#   build_content_sp2(root_path: str, logger=None) -> list

import os
import sys
import pathlib
import tempfile
import logging
from typing import Callable, List, Any, Optional

# Garante que core/ está no path para os imports do generator_sp2.py
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

# Importa o scanner original (que agora encontra utils_sp2 via sys.path acima)
from .generator_sp2 import build_content_sp2 as _build_content_sp2


def build_content_sp2(
    root_path: str,
    logger: Optional[Callable[[str], None]] = None,
) -> List[Any]:
    """
    Interface V5 do scanner SP2.

    Adapta a assinatura do V4 (que exige log_errors_path) para a interface
    do ContractEngine.scan(root_path, logger) do V5.
    """
    # Cria um arquivo de log temporário para compatibilidade com o V4
    log_file = os.path.join(tempfile.gettempdir(), "autorelatoriov5_sp2_scan.log")

    # Se nenhum logger foi passado, usa um logger silencioso
    if logger is None:
        _log = logging.getLogger("scanner_sp2")
        def logger(msg: str) -> None:
            _log.debug(msg)

    return _build_content_sp2(root_path, log_file, logger)
