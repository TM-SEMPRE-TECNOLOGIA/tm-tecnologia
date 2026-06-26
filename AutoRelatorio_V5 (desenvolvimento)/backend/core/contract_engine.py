# core/contract_engine.py — AutoRelatório V5
# Interface base para todos os 9 motores de contrato
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class MetaField:
    key: str
    label: str
    type: str           # "text" | "date" | "select"
    required: bool = True
    auto_fill: bool = False
    example: str = ""
    options: list[str] = field(default_factory=list)

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

class ContractEngine(ABC):
    """Interface que todo motor de contrato deve implementar."""

    contract_id: str        # ex: "1565"
    contract_name: str      # ex: "São José do Rio Preto / Ribeirão Preto"
    template_file: str      # nome do .docx em /template/
    reading_modes: list     # ["disco"] ou ["disco", "app"]
    generation_mode: str    # "tradicional" | "sp" | "sp2"

    @abstractmethod
    def scan(self, root_path: str, logger=None) -> list[Any]:
        """Varre a pasta raiz e retorna array de conteúdo."""

    @abstractmethod
    def build_word(self, modelo_path: str, conteudo: list, output_path: str, meta: dict) -> str:
        """Gera o .docx final. Retorna path do arquivo gerado."""

    @abstractmethod
    def get_items(self) -> dict:
        """Banco de itens: {chave: {id, desc, un}}"""

    @abstractmethod
    def get_meta_fields(self) -> list[MetaField]:
        """Campos do formulário de cabeçalho para este contrato."""

    @abstractmethod
    def validate_folder(self, root_path: str) -> ValidationResult:
        """Valida a estrutura de pastas antes do scan."""
