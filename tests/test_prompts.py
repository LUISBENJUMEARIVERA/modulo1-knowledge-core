"""Pruebas unitarias para las plantillas de prompts LCEL."""

from src.chains.prompts import FAQ_PROMPT, QA_PROMPT, SUMMARY_PROMPT


def test_summary_prompt_formatting():
    # Arrange
    sample_context = "Tecnoquímicas produce medicamentos y productos de higiene."

    # Act
    formatted = SUMMARY_PROMPT.format(context=sample_context)

    # Assert
    assert sample_context in formatted
    assert "resumen ejecutivo" in formatted.lower() or "informe" in formatted.lower()


def test_faq_prompt_formatting():
    # Arrange
    sample_context = "Planta Villa Rica certificada con normas INVIMA y FDA."

    # Act
    formatted = FAQ_PROMPT.format(context=sample_context)

    # Assert
    assert sample_context in formatted
    assert "frecuentes" in formatted.lower() or "faq" in formatted.lower()


def test_qa_prompt_formatting():
    # Arrange
    sample_context = "MK es la marca de genéricos de Tecnoquímicas."
    sample_question = "¿Cuáles son las marcas de medicamentos?"

    # Act
    qa_formatted = QA_PROMPT.format(context=sample_context, question=sample_question)

    # Assert
    assert sample_context in qa_formatted
    assert sample_question in qa_formatted
    assert "asistente virtual corporativo" in qa_formatted.lower()
    assert "knowledge_base" in qa_formatted.lower()
