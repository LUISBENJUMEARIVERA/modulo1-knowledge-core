"""Pruebas automatizadas de Invariantes de Datos para la Arquitectura Medallion."""

import json
from pathlib import Path

from src.core.config import config

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_medallion_layer_hierarchy_sizes():
    """Invariante 1: Capa Bronze (HTML crudo) debe ser significativamente mayor que Capa Silver."""
    raw_dir = ROOT_DIR / config.output_raw_dir
    processed_file = ROOT_DIR / config.output_processed_file

    assert raw_dir.exists(), "El directorio Bronze (data/raw) debe existir"
    assert processed_file.exists(), (
        "El archivo Silver (data/processed/knowledge_base.txt) debe existir"
    )

    total_bronze_bytes = sum(f.stat().st_size for f in raw_dir.glob("*.html"))
    silver_bytes = processed_file.stat().st_size

    assert total_bronze_bytes > 0, "Capa Bronze no debe estar vacía"
    assert silver_bytes > 0, "Capa Silver no debe estar vacía"
    assert total_bronze_bytes > silver_bytes, (
        f"Bronze ({total_bronze_bytes} bytes) debe ser mayor que Silver ({silver_bytes} bytes)"
    )


def test_noise_reduction_threshold():
    """Invariante 2: La reducción de ruido HTML entre Bronze y Silver/Gold debe superar el 80%."""
    metrics_file = ROOT_DIR / config.output_gold_metrics
    assert metrics_file.exists(), "El archivo de métricas Gold debe existir"

    with open(metrics_file, encoding="utf-8") as f:
        metrics = json.load(f)

    reduction_pct = metrics.get("noise_reduction_ratio_pct", 0)
    assert reduction_pct >= 80.0, (
        f"La tasa de reducción de ruido ({reduction_pct}%) debe ser >= 80% para garantizar pureza semántica"
    )


def test_gold_cryptographic_uniqueness():
    """Invariante 3: En la capa Gold no deben existir duplicados de hash criptográfico SHA-256."""
    gold_file = ROOT_DIR / config.output_gold_jsonl
    assert gold_file.exists(), "El archivo Gold (corpus.jsonl) debe existir"

    hashes = []
    with open(gold_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                hashes.append(record["content_hash"])

    assert len(hashes) > 0, "La capa Gold debe contener registros"
    assert len(hashes) == len(set(hashes)), (
        f"Existen {len(hashes) - len(set(hashes))} hashes duplicados en la capa Gold"
    )


def test_gold_record_completeness():
    """Invariante 4: Cada documento Gold debe contener texto no trivial y metadatos válidos."""
    gold_file = ROOT_DIR / config.output_gold_jsonl

    with open(gold_file, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                continue
            doc = json.loads(line)
            assert len(doc["content"]) >= 50, (
                f"Línea {line_num}: Contenido demasiado corto ({len(doc['content'])} caracteres)"
            )
            assert doc["token_count"] >= 10, (
                f"Línea {line_num}: Estimación de tokens anormalmente baja"
            )
            assert doc["url"].startswith("http"), f"Línea {line_num}: URL no válida ({doc['url']})"
