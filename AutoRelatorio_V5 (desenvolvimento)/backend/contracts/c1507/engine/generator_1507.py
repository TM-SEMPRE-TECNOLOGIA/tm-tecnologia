# contracts/c1507/engine/generator_1507.py — Contrato 1507
# Cuiabá — Pipeline completo (scan + build)
# Módulo exclusivo deste contrato. Alterar aqui não afeta nenhum outro.

import os
import tempfile
from dataclasses import dataclass
from typing import Callable, List, Any, Optional

from .scanner_1507 import build_content_from_root
from .word_builder_1507 import inserir_conteudo


@dataclass
class RunResult:
    output_docx: str
    log_process: str
    log_errors: str
    total_images: int


def _default_logger(_: str) -> None:
    return


def run_all(
    pasta_raiz: str,
    modelo_path: str,
    pasta_saida: str,
    logger: Callable[[str], None] = _default_logger,
    conteudo_aprovado: Optional[List[Any]] = None,
    meta: Optional[dict] = None,
) -> RunResult:
    """
    Pipeline completo do contrato 1507 (Cuiabá):
    varre pasta → monta conteudo[] → gera .docx
    """
    os.makedirs(pasta_saida, exist_ok=True)

    nome_pasta_raiz = os.path.basename(pasta_raiz.strip(os.sep))
    output_docx = os.path.join(
        pasta_saida,
        f"RELATÓRIO FOTOGRÁFICO - {nome_pasta_raiz} - LEVANTAMENTO PREVENTIVO.docx",
    )
    log_errors = os.path.join(pasta_saida, "c1507_erros_pastas.txt")
    log_process = os.path.join(pasta_saida, "c1507_process_log.txt")

    def file_logger(msg: str) -> None:
        logger(msg)
        with open(log_process, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    with open(log_process, "w", encoding="utf-8") as f:
        f.write("PROCESS LOG — c1507 Cuiabá\n\n")
        f.write(f"Pasta raiz: {pasta_raiz}\n")
        f.write(f"Modelo:     {modelo_path}\n")
        f.write(f"Saída:      {pasta_saida}\n\n")

    conteudo = conteudo_aprovado or build_content_from_root(pasta_raiz, log_errors, logger=file_logger)

    total_images = 0
    result_path = inserir_conteudo(modelo_path, conteudo, output_docx, meta=meta)

    # Conta imagens inseridas
    total_images = sum(1 for item in conteudo if isinstance(item, dict) and "imagem" in item)

    file_logger(f"[OK] Relatório gerado: {result_path}")
    file_logger(f"[OK] Total de imagens: {total_images}")

    return RunResult(
        output_docx=output_docx,
        log_process=log_process,
        log_errors=log_errors,
        total_images=total_images,
    )
