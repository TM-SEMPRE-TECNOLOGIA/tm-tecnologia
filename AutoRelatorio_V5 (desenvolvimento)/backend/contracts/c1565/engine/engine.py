# contracts/c1565/engine/engine.py — Contrato 1565
# São José do Rio Preto / Ribeirão Preto — Motor SP2 (Memória de Cálculo)
# Migração direta de generator_sp2.py + word_utils_sp2.py do V4
# com interface ContractEngine.

import json, pathlib
from core.contract_engine import ContractEngine, MetaField, ValidationResult

ITEMS_PATH = pathlib.Path(__file__).parent.parent / "items" / "items.json"

class Contract1565Engine(ContractEngine):
    contract_id     = "1565"
    contract_name   = "São José do Rio Preto / Ribeirão Preto"
    template_file   = "MODELO-1565.docx"
    generation_mode = "sp2"
    reading_modes   = ["disco"]

    def get_meta_fields(self) -> list[MetaField]:
        # Chaves correspondem exatamente aos placeholders {{key}} no template .docx
        return [
            MetaField("nr_os",                   "Nº da OS",             "text",  required=True,  example="1753"),
            MetaField("dt_atend",                "Data do Atendimento",  "date",  required=True),
            MetaField("ag_cod",                  "Código da Agência",    "text",  required=True,  example="1234-5"),
            MetaField("ag_nome",                 "Nome da Agência",      "text",  required=True,  example="Agência Centro"),
            MetaField("endereco",                "Endereço",             "text",  required=False, example="Rua das Flores, 100"),
            MetaField("responsavel_dependencia", "Responsável",          "text",  required=False, example="Mat. 12345 — João Silva"),
            MetaField("dt_elab",                 "Data de Elaboração",   "date",  auto_fill=True),
        ]

    def get_items(self) -> dict:
        with open(ITEMS_PATH, encoding="utf-8") as f:
            return json.load(f)

    def validate_folder(self, root_path: str) -> ValidationResult:
        import os
        errors, warnings = [], []
        if not os.path.isdir(root_path):
            errors.append(f"Pasta não encontrada: {root_path}")
            return ValidationResult(valid=False, errors=errors)
        # Verifica se há pelo menos uma subpasta numerada
        subdirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        if not subdirs:
            warnings.append("Nenhuma subpasta encontrada. Certifique-se de que a estrutura está correta.")
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def scan(self, root_path: str, logger=None) -> list:
        from .scanner_1565 import build_content_sp2
        return build_content_sp2(root_path, logger=logger)

    def build_word(self, modelo_path: str, conteudo: list, output_path: str, meta: dict) -> str:
        from .word_builder_1565 import inserir_conteudo_sp2
        return inserir_conteudo_sp2(modelo_path, conteudo, output_path, meta)
