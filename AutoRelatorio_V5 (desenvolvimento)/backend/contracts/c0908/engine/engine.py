# contracts/c0908/engine/engine.py — Contrato 0908
# São José dos Campos — Motor SP
# Migração de generator_sp.py + word_utils_sp.py do V4

from core.contract_engine import ContractEngine, MetaField, ValidationResult
import os

class Contract0908Engine(ContractEngine):
    contract_id     = "0908"
    contract_name   = "São José dos Campos"
    template_file   = "MODELO-0908.docx"
    generation_mode = "sp"
    reading_modes   = ["disco", "app"]

    def get_meta_fields(self) -> list[MetaField]:
        # Chaves correspondem exatamente aos placeholders {{key}} no template .docx
        return [
            MetaField("nr_os",                   "Nº da OS",             "text", required=True,  example="2001"),
            MetaField("dt_atend",                "Data do Atendimento",  "date", required=True),
            MetaField("ag_cod",                  "Código da Agência",    "text", required=True,  example="0908-1"),
            MetaField("ag_nome",                 "Nome da Agência",      "text", required=True),
            MetaField("endereco",                "Endereço",             "text", required=False),
            MetaField("responsavel_dependencia", "Responsável",          "text", required=False),
            MetaField("dt_elab",                 "Data de Elaboração",   "date", auto_fill=True),
        ]

    def get_items(self) -> dict:
        import json, pathlib
        items_path = pathlib.Path(__file__).parent.parent / "items" / "items.json"
        with open(items_path, encoding="utf-8") as f:
            return json.load(f)

    def validate_folder(self, root_path: str) -> ValidationResult:
        errors, warnings = [], []
        if not os.path.isdir(root_path):
            errors.append(f"Pasta não encontrada: {root_path}")
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def scan(self, root_path: str, logger=None) -> list:
        from .scanner_0908 import build_content_sp
        return build_content_sp(root_path, logger=logger)

    def build_word(self, modelo_path: str, conteudo: list, output_path: str, meta: dict) -> str:
        from .word_builder_0908 import inserir_conteudo_sp
        return inserir_conteudo_sp(modelo_path, conteudo, output_path, meta)
