"""Módulo 1: Knowledge Core — prueba de humo."""

from __future__ import annotations

import modulo1_knowledge_core


def test_el_paquete_expone_una_version() -> None:
    # Arrange / Act
    version = getattr(modulo1_knowledge_core, "__version__", None)

    # Assert
    assert version is not None
    assert isinstance(version, str)
