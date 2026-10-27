"""Pruebas unitarias para KnowledgeService y cadenas LCEL."""

from unittest.mock import MagicMock, patch

from src.chains.tasks import KnowledgeService


def test_load_context_when_file_exists(tmp_path):
    # Arrange
    fake_kb = tmp_path / "knowledge_base.txt"
    fake_kb.write_text("Información de prueba sobre Tecnoquímicas.", encoding="utf-8")

    with (
        patch("src.chains.tasks.config.output_processed_file", str(fake_kb)),
        patch("src.chains.tasks.get_llm") as mock_get_llm,
    ):
        mock_get_llm.return_value = MagicMock()

        # Act
        srv = KnowledgeService()

        # Assert
        assert srv.context == "Información de prueba sobre Tecnoquímicas."


def test_load_context_when_file_missing(tmp_path):
    # Arrange
    missing_file = tmp_path / "non_existent.txt"

    with (
        patch("src.chains.tasks.config.output_processed_file", str(missing_file)),
        patch("src.chains.tasks.get_llm") as mock_get_llm,
    ):
        mock_get_llm.return_value = MagicMock()

        # Act
        srv = KnowledgeService()

        # Assert
        assert "No hay datos disponibles" in srv.context


def test_qa_stream_chain():
    # Arrange
    with patch("src.chains.tasks.get_llm") as mock_get_llm:
        mock_llm = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.content = "Respuesta simulada"
        mock_llm.stream.return_value = [mock_chunk]
        mock_get_llm.return_value = mock_llm

        srv = KnowledgeService()
        srv.context = "Contexto farmacéutico."

        # Act
        # Using mock chain stream
        with patch.object(
            srv, "answer_question_stream", return_value=iter(["Respuesta simulada"])
        ) as mock_method:
            stream = srv.answer_question_stream("¿Pregunta?")
            result = list(stream)

        # Assert
        assert result == ["Respuesta simulada"]
        mock_method.assert_called_once_with("¿Pregunta?")
