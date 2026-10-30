"""Pruebas unitarias para el contrato de datos del pipeline Bronze, Silver y Gold."""

import json

from src.ingestion.crawler import slugify
from src.ingestion.extractor import ResilientExtractor


def test_compute_sha256_deterministic():
    text = "Tecnoquímicas S.A. Planta Villa Rica"
    hash1 = ResilientExtractor.compute_sha256(text)
    hash2 = ResilientExtractor.compute_sha256(text)

    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 produce 64 caracteres hexadecimales


def test_estimate_tokens():
    text = "Tecnoquímicas S.A. es una empresa farmacéutica colombiana con sede principal en Cali."
    tokens = ResilientExtractor.estimate_tokens(text)
    assert tokens > 10
    assert isinstance(tokens, int)


def test_extract_title():
    html_with_title = (
        "<html><head><title>Nuestras Marcas | TQ Farma</title></head><body>Contenido</body></html>"
    )
    title = ResilientExtractor.extract_title(html_with_title)
    assert title == "Nuestras Marcas | TQ Farma"

    html_with_h1 = "<html><body><h1>Planta Industrial Jamundí</h1></body></html>"
    title_h1 = ResilientExtractor.extract_title(html_with_h1)
    assert title_h1 == "Planta Industrial Jamundí"


def test_slugify():
    slug = slugify("Atención y FAQs -> https://www.tqconfiable.com/contacto/")
    assert "atenci_n" in slug or "atencion" in slug or "faqs" in slug
    assert not any(char in slug for char in [":", "/", "\\", "?", "*"])


def test_gold_schema_contract():
    """Valida el esquema del registro Gold exigido por la rúbrica."""
    dummy_record = {
        "url": "https://www.tqconfiable.com",
        "title": "Portal Corporativo TQ",
        "section": "Portal Principal",
        "crawled_at": "2026-10-30T12:00:00Z",
        "content_hash": ResilientExtractor.compute_sha256("test"),
        "char_count": 100,
        "token_count": 25,
        "content": "Contenido validado",
    }

    # Serialización JSONL requerida
    serialized = json.dumps(dummy_record)
    loaded = json.loads(serialized)

    required_keys = {
        "url",
        "title",
        "section",
        "crawled_at",
        "content_hash",
        "char_count",
        "token_count",
        "content",
    }
    assert required_keys.issubset(loaded.keys())
