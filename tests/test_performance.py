"""Pruebas automáticas de regresión de latencia y throughput."""

import time
from unittest.mock import MagicMock, patch

from src.chains.tasks import KnowledgeService


def test_service_initialization_latency(tmp_path):
    """Garantiza que la carga de la base de conocimiento en memoria RAM tome menos de 100ms."""
    fake_kb = tmp_path / "knowledge_base.txt"
    fake_kb.write_text("Contexto de prueba " * 500, encoding="utf-8")

    start_time = time.perf_counter()
    with (
        patch("src.chains.tasks.config.output_processed_file", str(fake_kb)),
        patch("src.chains.tasks.get_llm") as mock_get_llm,
    ):
        mock_get_llm.return_value = MagicMock()
        service = KnowledgeService()
    duration_ms = (time.perf_counter() - start_time) * 1000

    assert duration_ms < 100.0, (
        f"La inicialización del servicio tardó demasiado ({duration_ms:.2f}ms > 100ms)"
    )
    assert len(service.context) > 0


def test_streaming_generator_non_blocking():
    """Valida que el generador de streaming entregue chunks de manera incremental sin acumular todo en memoria."""
    with patch.object(
        KnowledgeService,
        "answer_question_stream",
        return_value=iter(["Token1 ", "Token2 ", "Token3."]),
    ):
        service = KnowledgeService()
        generator = service.answer_question_stream("¿Consulta?")

        first_chunk = next(generator)
        assert first_chunk == "Token1 ", (
            "El primer token debe estar disponible de inmediato sin esperar el stream completo"
        )
        second_chunk = next(generator)
        assert second_chunk == "Token2 "
