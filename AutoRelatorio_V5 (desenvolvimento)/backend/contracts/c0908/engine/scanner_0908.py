# contracts/c0908/engine/scanner_0908.py — Contrato 0908
# São Paulo / São José dos Campos — Scanner Modo SP
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.

import sys
import pathlib
import tempfile
import os
import logging
from typing import Callable, List, Any, Optional

# Garante que core/ está no path
_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from .generator_sp import build_content_sp as _build_content_sp


def build_content_sp(
    root_path: str,
    logger: Optional[Callable[[str], None]] = None,
) -> List[Any]:
    """Interface V5 do scanner SP."""
    log_file = os.path.join(tempfile.gettempdir(), "autorelatoriov5_sp_scan.log")

    if logger is None:
        _log = logging.getLogger("scanner_sp")
        def logger(msg: str) -> None:
            _log.debug(msg)

    return _build_content_sp(root_path, log_file, logger)
