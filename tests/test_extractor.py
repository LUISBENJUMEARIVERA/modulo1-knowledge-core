"""Pruebas unitarias para el extractor resiliente de contenido."""

from src.ingestion.extractor import ResilientExtractor


def test_extract_clean_content_trafilatura(sample_html: str):
    # Arrange & Act
    extracted = ResilientExtractor.extract_clean_content(sample_html, url="https://www.tqfarma.com")

    # Assert
    assert extracted is not None
    assert len(extracted) > 50
    assert "Villa Rica" in extracted
    assert "Tecnoquímicas" in extracted
    # Debería ignorar script y estilo
    assert "console.log" not in extracted
    assert "font-family" not in extracted


def test_extract_clean_content_fallback(sample_short_html: str):
    # Arrange & Act
    extracted = ResilientExtractor.extract_clean_content(sample_short_html, url="https://test.com")

    # Assert
    assert extracted is not None
    assert "fallback heuristico" in extracted
    assert "Ignored Nav" not in extracted


def test_extract_empty_html():
    # Arrange & Act
    extracted = ResilientExtractor.extract_clean_content("", url="https://test.com")

    # Assert
    assert extracted == ""
