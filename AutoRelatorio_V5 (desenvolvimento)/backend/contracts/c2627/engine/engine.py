# contracts/c2627/engine/engine.py — Contrato 2627
# Governador Valadares — Motor Tradicional
# Migração de generator.py + word_utils.py do V4

from core.contract_engine import ContractEngine, MetaField, ValidationResult
import os

class Contract2627Engine(ContractEngine):
    contract_id     = "2627"
    contract_name   = "Governador Valadares"
    template_file   = "MODELO-2627.docx"
    generation_mode = "tradicional"
    reading_modes   = ["disco", "app"]

    def get_meta_fields(self) -> list[MetaField]:
        # Chaves correspondem exatamente aos placeholders {{key}} no template .docx
        return [
            MetaField("nr_os",                   "Nº da OS",             "text", required=True,  example="1000"),
            MetaField("dt_atend",                "Data do Atendimento",  "date", required=True),
            MetaField("ag_cod",                  "Código da Agência",    "text", required=True,  example="2627-0"),
            MetaField("ag_nome",                 "Nome da Agência",      "text", required=True),
            MetaField("endereco",                "Endereço",             "text", required=False),
            MetaField("responsavel_dependencia", "Responsável",          "text", required=False),
            MetaField("dt_elab",                 "Data de Elaboração",   "date", auto_fill=True),
        ]

    def get_items(self) -> dict:
        import json, pathlib
        items_path = pathlib.Path(__file__).parent.parent / "items" / "items.json"
        if items_path.exists():
            with open(items_path, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def validate_folder(self, root_path: str) -> ValidationResult:
        errors, warnings = [], []
        if not os.path.isdir(root_path):
            errors.append(f"Pasta não encontrada: {root_path}")
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def scan(self, root_path: str, logger=None) -> list:
        from .scanner_2627 import build_content_from_root
        import tempfile, os
        log_path = os.path.join(tempfile.gettempdir(), "c2627_scan_errors.txt")
        return build_content_from_root(root_path, log_path, logger or (lambda _: None))

    def build_word(self, modelo_path: str, conteudo: list, output_path: str, meta: dict) -> str:
        from .word_builder_2627 import inserir_conteudo
        return inserir_conteudo(modelo_path, conteudo, output_path, meta)