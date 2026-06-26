# contracts/c2627/engine/scanner_2627.py — Contrato 2627
# Governador Valadares — Scanner Modo Tradicional
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.

import sys
import pathlib
import os
import re
from typing import Callable, List, Any

_CORE = str(pathlib.Path(__file__).parent.parent.parent.parent / "core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

ORDEM_PASTAS = ["- Área externa", "- Área interna", "- Segundo piso"]


def folder_sort_key(name: str):
    name_lower = name.lower()
    if "vista ampla" in name_lower:
        return (0, name_lower)
    match = re.match(r'^(\d+)(.*)', name)
    if match:
        return (1, int(match.group(1)), match.group(2))
    if "detalhes" in name_lower:
        return (3, name_lower)
    return (2, name_lower)


def build_content_from_root(
    pasta_raiz: str,
    log_errors_path: str,
    logger: Callable[[str], None] = lambda _: None,
) -> List[Any]:
    """
    Varre a pasta raiz do contrato 2627 (Governador Valadares) e monta conteudo[].

    Retorna lista com:
    - str com prefixo »  → título de seção
    - {"imagem": path}   → foto
    - {"quebra_pagina": True} → quebra de página
    """
    os.makedirs(os.path.dirname(log_errors_path), exist_ok=True)

    with open(log_errors_path, "w", encoding="utf-8") as log:
        log.write("LOG DE ERROS — c2627 Governador Valadares — Leitura de pastas\n\n")

    conteudo: List[Any] = []
    logger(">>> [c2627] Lendo estrutura de pastas...")

    for root_dir, dirs, files in os.walk(pasta_raiz, topdown=True):
        try:
            root_dir = os.fsdecode(root_dir)
            dirs[:] = [os.fsdecode(d) for d in dirs]
            files = [os.fsdecode(f) for f in files]
        except Exception as e:
            with open(log_errors_path, "a", encoding="utf-8") as log:
                log.write(f"Falha ao decodificar nomes em: {root_dir} ({e})\n")
            continue

        if root_dir == pasta_raiz:
            dirs.sort(key=lambda x: (
                0 if x == "- Vista ampla" else 1,
                ORDEM_PASTAS.index(x) if x in ORDEM_PASTAS else len(ORDEM_PASTAS),
                folder_sort_key(x),
            ))
        else:
            dirs.sort(key=folder_sort_key)

        path_parts = os.path.relpath(root_dir, pasta_raiz).split(os.sep)
        nome = path_parts[-1]

        if nome != ".":
            nivel = len(path_parts)
            prefixos = {1: "", 2: "»", 3: "»»"}
            conteudo.append(f"{prefixos.get(nivel, '»»»')}{nome}")

        try:
            arquivos_imagens = [
                os.path.join(root_dir, f)
                for f in files
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
            try:
                arquivos_imagens.sort(key=os.path.getctime)
            except Exception:
                arquivos_imagens.sort()

            for imagem_path in arquivos_imagens:
                if os.path.exists(imagem_path):
                    conteudo.append({"imagem": imagem_path})

            conteudo.append({"quebra_pagina": True})

        except Exception as e_dir:
            with open(log_errors_path, "a", encoding="utf-8") as log:
                log.write(f"Falha ao processar pasta: {root_dir} ({e_dir})\n")
            continue

    logger(">>> [c2627] Estrutura lida completamente.")
    return conteudo
