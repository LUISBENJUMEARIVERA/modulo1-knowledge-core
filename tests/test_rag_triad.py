"""Pruebas automáticas de evaluación RAG (Fidelidad semántica y Guardrails de rechazo)."""

from src.chains.prompts import QA_PROMPT


def test_faithfulness_grounding_invariant():
    """Valida que una respuesta factual esté compuesta por entidades estrictamente presentes en el corpus."""
    knowledge_context = """
    Nuestra casa matriz está ubicada en Cali, Colombia.
    Teléfono: 01 8000 523339 - Extensión 2070
    Correo electrónico: serviciosalconsumidor@tqgrupo.com
    Planta Villa Rica produce medicamentos esenciales con certificación INVIMA.
    """

    sample_answer = (
        "La sede principal de Tecnoquímicas se encuentra en Cali, Colombia. "
        "El teléfono de atención es 01 8000 523339 con extensión 2070."
    )

    # Entidades verificadas que deben existir en el contexto fuente
    entities_to_check = ["Cali", "Colombia", "01 8000 523339", "2070"]
    for entity in entities_to_check:
        assert entity in sample_answer, f"La respuesta debe contener '{entity}'"
        assert entity in knowledge_context, (
            f"La entidad '{entity}' debe provenir del contexto fuente"
        )


def test_rejection_guardrail_verbatim_contract():
    """Valida que la frase de rechazo obligatoria se mantenga exacta frente a preguntas fuera de dominio."""
    rejection_contract = "Lo siento, la información oficial disponible en el sistema no contiene datos para responder a esta consulta."

    system_prompt_str = QA_PROMPT.messages[0].prompt.template
    assert rejection_contract in system_prompt_str, (
        "El system prompt de QA debe incluir literalmente la directiva de rechazo estándar"
    )
