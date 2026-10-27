"""Pruebas unitarias para utilidades del crawler y normalización."""

from urllib.parse import urlparse

from src.core.config import config


def is_valid_url(url: str) -> bool:
    """Helper emulado para probar el filtrado de dominios y extensiones."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    if domain not in config.allowed_domains:
        return False

    return all(not path.endswith(ext) for ext in config.ignored_extensions)


def test_valid_allowed_domains():
    assert is_valid_url("https://www.tqconfiable.com/quienes-somos")
    assert is_valid_url("https://tqconfiable.com/plantas")
    assert is_valid_url("https://www.tqfarma.com/productos")


def test_invalid_external_domain():
    assert not is_valid_url("https://www.google.com/search")
    assert not is_valid_url("https://www.pharma-competitor.com/catalog")


def test_ignored_binary_extensions():
    assert not is_valid_url("https://www.tqconfiable.com/brochure.pdf")
    assert not is_valid_url("https://www.tqconfiable.com/banner.jpg")
    assert not is_valid_url("https://www.tqconfiable.com/archive.zip")
    assert not is_valid_url("https://www.tqconfiable.com/script.js")
