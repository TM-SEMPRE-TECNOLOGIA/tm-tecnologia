# contracts/c3575/engine/word_builder_3575.py — Contrato 3575
# Tangará da Serra — Word Builder Modo Tradicional
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.

import sys
import pathlib

_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from word_utils import inserir_conteudo as _inserir_conteudo


def inserir_conteudo(
    modelo_path: str,
    conteudo: list,
    output_path: str,
    meta: dict = None,
) -> str:
    """
    Gera o .docx do contrato 3575 (Tangará da Serra) a partir do conteudo[].

    Args:
        modelo_path: Caminho para MODELO-3575.docx
        conteudo:    Array conteudo[] produzido pelo scanner_3575
        output_path: Caminho de saída do .docx gerado
        meta:        Dicionário com placeholders (nr_os, ag_cod, etc.)

    Returns:
        output_path do arquivo gerado
    """
    _inserir_conteudo(
        modelo_path=modelo_path,
        conteudo=conteudo,
        output_path=output_path,
        meta=meta,
    )
    return output_path
