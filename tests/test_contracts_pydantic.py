"""Pruebas de validación estricta de esquemas de datos con Pydantic v2."""

import json
import re
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl, field_validator

ROOT_DIR = Path(__file__).resolve().parent.parent


class GoldDocumentSchema(BaseModel):
    """Contrato estricto para los documentos normalizados en Capa Gold."""

    url: HttpUrl
    title: str = Field(min_length=3)
    section: str = Field(min_length=2)
    crawled_at: datetime
    content_hash: str
    char_count: int = Field(gt=0)
    token_count: int = Field(gt=0)
    content: str = Field(min_length=40)

    @field_validator("content_hash")
    @classmethod
    def validate_sha256(cls, v: str) -> str:
        if not re.match(r"^[a-f0-9]{64}$", v.lower()):
            raise ValueError(f"El hash '{v}' no es un SHA-256 hexadecimal válido de 64 caracteres.")
        return v.lower()


def test_validate_all_gold_records_against_pydantic_schema():
    """Valida que el 100% de los documentos en corpus.jsonl satisfagan el contrato Pydantic v2."""
    gold_path = ROOT_DIR / "data" / "gold" / "corpus.jsonl"
    assert gold_path.exists(), "El corpus Gold debe existir"

    validated_count = 0
    with open(gold_path, encoding="utf-8") as f:
        for _idx, line in enumerate(f, start=1):
            if not line.strip():
                continue
            data = json.loads(line)
            # Validación mediante instanciación de modelo Pydantic v2
            record = GoldDocumentSchema.model_validate(data)
            assert str(record.url).startswith("http")
            assert len(record.content_hash) == 64
            validated_count += 1

    assert validated_count >= 5, (
        f"Se esperaban al menos 5 documentos validados, se encontraron {validated_count}"
    )
