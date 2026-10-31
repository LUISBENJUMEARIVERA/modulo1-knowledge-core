"""Prueba de integración end-to-end simulada del crawler y etapas de datos sin red externa."""

from src.ingestion.extractor import ResilientExtractor

MOCK_HTML_PORTAL = """
<!DOCTYPE html>
<html>
<head><title>Tecnoquímicas S.A. | Confiable</title></head>
<body>
<nav><a href="/">Inicio</a></nav>
<main>
    <h1>Compromiso con la Salud y el Bienestar</h1>
    <p>Tecnoquímicas S.A. es un laboratorio farmacéutico líder con sede principal en Cali, Colombia.</p>
    <p>Nuestra planta principal en Villa Rica cuenta con certificación BPM e INVIMA.</p>
</main>
<footer><p>© 2026 Tecnoquímicas</p></footer>
</body>
</html>
"""

MOCK_HTML_CONTACT = """
<!DOCTYPE html>
<html>
<head><title>Canales de Contacto | TQ</title></head>
<body>
<main>
    <h1>Atención al Consumidor</h1>
    <p>Línea gratuita de atención: 01 8000 523339 con extensión 2070.</p>
    <p>Correo de atención: serviciosalconsumidor@tqgrupo.com</p>
</main>
</body>
</html>
"""


def test_offline_crawler_extraction_flow(tmp_path):
    """Simula las 5 etapas del pipeline (Descubrir, Extraer, Limpiar, Deduplicar, Enriquecer) en aislamiento."""
    # 1. Descubrir & Extraer (Simulado)
    pages = [
        ("Portal Principal", "https://www.tqconfiable.com", MOCK_HTML_PORTAL),
        ("Canales y Sedes", "https://www.tqconfiable.com/contacto/", MOCK_HTML_CONTACT),
        # Duplicado intencional para verificar deduplicación
        ("Duplicado", "https://www.tqconfiable.com/copia", MOCK_HTML_PORTAL),
    ]

    bronze_dir = tmp_path / "raw"
    silver_dir = tmp_path / "processed"
    gold_dir = tmp_path / "gold"
    bronze_dir.mkdir()
    silver_dir.mkdir()
    gold_dir.mkdir()

    seen_hashes = set()
    gold_records = []
    total_raw_bytes = 0
    total_clean_bytes = 0

    for section, url, html in pages:
        raw_bytes = len(html.encode("utf-8"))
        total_raw_bytes += raw_bytes

        # Limpiar
        title = ResilientExtractor.extract_title(html, default=section)
        clean_text = ResilientExtractor.extract_clean_content(html, url)
        clean_bytes = len(clean_text.encode("utf-8"))

        # Deduplicar por SHA-256
        content_hash = ResilientExtractor.compute_sha256(clean_text)
        if content_hash in seen_hashes:
            continue
        seen_hashes.add(content_hash)
        total_clean_bytes += clean_bytes

        # Enriquecer
        tokens = ResilientExtractor.estimate_tokens(clean_text)
        gold_records.append(
            {
                "url": url,
                "title": title,
                "section": section,
                "content_hash": content_hash,
                "token_count": tokens,
                "content": clean_text,
            }
        )

    # Validaciones E2E
    assert len(gold_records) == 2, "El duplicado debió ser descartado exitosamente"
    assert total_raw_bytes > total_clean_bytes, "El HTML crudo debe ser mayor que el texto limpio"
    assert "01 8000 523339" in gold_records[1]["content"]
    assert "Villa Rica" in gold_records[0]["content"]
