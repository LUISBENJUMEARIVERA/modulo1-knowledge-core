import sys
from pathlib import Path

# Inyectar la raíz del proyecto en sys.path para resolución limpia de módulos
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from src.chains.tasks import service
from src.core.config import config

st.set_page_config(
    page_title="Tecnoquímicas AI - Núcleo Semántico",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Tecnoquímicas S.A. — Núcleo de Conocimiento Semántico")
st.caption(f"Módulo 1: Pipeline de Ingesta y Sistema Q&A con LangChain y Ollama ({config.llm_model})")

# Pestañas para las 3 tareas requeridas en la rúbrica
tab_qa, tab_summary, tab_faq = st.tabs([
    "💬 Asistente Q&A", 
    "📑 Resumen Corporativo", 
    "❓ Preguntas Frecuentes (FAQ)"
])

# 1. Pestaña de Q&A interactivo
with tab_qa:
    st.markdown("### Asistente Grounded (Anti-Alucinaciones)")
    st.info("Este asistente responde basándose **únicamente** en la base de conocimiento extraída de Tecnoquímicas.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu consulta sobre Tecnoquímicas..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            for chunk in service.answer_question_stream(prompt):
                full_response += chunk
                response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 2. Pestaña de Resumen
with tab_summary:
    st.markdown("### Síntesis Ejecutiva de la Empresa")
    if st.button("Generar / Actualizar Resumen", key="btn_summary"):
        with st.spinner("Procesando síntesis con el LLM..."):
            st.write_stream(service.get_summary_stream())

# 3. Pestaña de FAQs
with tab_faq:
    st.markdown("### FAQs Generadas Automáticamente")
    if st.button("Generar / Actualizar FAQs", key="btn_faq"):
        with st.spinner("Extrayendo preguntas frecuentes del contexto..."):
            st.write_stream(service.get_faq_stream())

# Barra lateral informativa
with st.sidebar:
    st.header("Auditoría del Sistema")
    st.markdown("**Empresa:** Tecnoquímicas S.A.")
    st.markdown(f"**Motor:** Ollama `{config.llm_model}`")
    st.markdown(f"**Base Conocimiento:** `{len(service.context)}` caracteres")
    st.divider()
    st.caption("Arquitectura modular con Playwright, Trafilatura, LangChain LCEL y Streamlit.")