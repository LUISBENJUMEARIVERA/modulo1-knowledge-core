import sys
from pathlib import Path

# Inyectar la raíz del proyecto en sys.path para resolución de módulos
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components
from src.chains.tasks import service
from src.core.config import config

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tecnoquímicas AI — Núcleo de Inteligencia",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# GESTIÓN DE ESTADO (DARK MODE EXCLUSIVO Y PERSISTENCIA TOTAL)
# -----------------------------------------------------------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = {
        "Consulta Principal": [
            {
                "role": "assistant",
                "content": "Bienvenido al Núcleo de Inteligencia de **Tecnoquímicas S.A.** Respondo inquietudes basándome exclusivamente en la base documental auditada de la empresa (plantas, marcas de consumo masivo, línea médica y certificaciones). ¿Qué información requieres verificar?",
            }
        ]
    }

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "Consulta Principal"

if st.session_state.current_chat_id not in st.session_state.conversations:
    st.session_state.current_chat_id = next(iter(st.session_state.conversations.keys()))

if "executive_summary_content" not in st.session_state:
    st.session_state.executive_summary_content = None

if "faq_content" not in st.session_state:
    st.session_state.faq_content = None

# -----------------------------------------------------------------------------
# DESIGN SYSTEM: DARK MODE NATIVO TECNOQUÍMICAS & ALINEACIÓN PRECISA
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
    --tq-bg: #071321;
    --tq-surface: #0C1E34;
    --tq-surface-hover: #122947;
    --tq-border: #1B3658;
    --tq-border-subtle: #152B46;
    --tq-text-primary: #F8FAFC;
    --tq-text-secondary: #94A3B8;
    --tq-brand-navy: #0A2540;
    --tq-chat-bg: #09192C;
    --tq-sidebar-bg: #050E1A;
    --tq-chat-container-bg: #08162A;
    --tq-cyan: #00A896;
    --tq-cyan-bright: #00C49F;
    --tq-cyan-surface: rgba(0, 168, 150, 0.12);
}

/* =========================================================================
   BLOQUEO TOTAL DE SCROLLBARS EN LA APLICACIÓN GLOBAL
   ========================================================================= */
html, body {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    background-color: var(--tq-bg) !important;
    color: var(--tq-text-primary) !important;
    height: 100vh !important;
    overflow: hidden !important;
}

.stAppViewContainer, .stAppViewContainer > section {
    height: 100vh !important;
    overflow: hidden !important;
}

.stAppViewBlockContainer {
    padding-top: 0.8rem !important;
    padding-bottom: 0.4rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

.material-symbols-rounded, .material-symbols-outlined, [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
}

header[data-testid="stHeader"] {
    display: none !important;
}

/* =========================================================================
   SIDEBAR: ALINEACIÓN SUPERIOR EXACTA CON EL HERO SECTION
   ========================================================================= */
section[data-testid="stSidebar"] {
    background-color: var(--tq-sidebar-bg) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

section[data-testid="stSidebar"] > div:first-child {
    height: 100vh !important;
    max-height: 100vh !important;
    padding-top: 0.8rem !important;
    padding-bottom: 0.8rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    gap: 12px !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
    position: absolute !important;
    top: 0.5rem !important;
    right: 0.5rem !important;
    z-index: 10 !important;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

.tq-sidebar-head {
    padding: 0 0 10px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 0 !important;
}

.tq-sidebar-head h2 {
    font-size: 1.22rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    color: #FFFFFF !important;
    line-height: 1.2;
}

.tq-sidebar-head p {
    font-size: 0.78rem;
    color: var(--tq-cyan-bright) !important;
    margin: 3px 0 0 0;
    font-weight: 600;
}

.tq-metric-tile {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 10px 14px;
}

.tq-metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #94A3B8 !important;
    display: flex;
    justify-content: space-between;
}

.tq-metric-number {
    font-size: 1.3rem;
    font-weight: 800;
    color: #FFFFFF !important;
    font-feature-settings: "tnum";
    margin: 2px 0;
}

.tq-metric-sub {
    font-size: 0.7rem;
    color: var(--tq-cyan-bright) !important;
}

.tq-sidebar-links {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 4px;
}

.tq-source-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 7px 12px;
    text-decoration: none !important;
    transition: all 0.2s ease;
}

.tq-source-link:hover {
    background: rgba(0, 168, 150, 0.18);
    border-color: var(--tq-cyan-bright);
    transform: translateX(3px);
}

.tq-source-link span {
    font-size: 0.78rem;
    font-weight: 600;
    color: #E2E8F0 !important;
}

/* =========================================================================
   HERO COMPACTO
   ========================================================================= */
.tq-hero {
    position: relative;
    border-radius: 12px;
    padding: 14px 22px;
    margin-bottom: 10px;
    border: 1px solid rgba(0, 168, 150, 0.35);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    background: linear-gradient(135deg, rgba(7, 19, 33, 0.94) 0%, rgba(10, 37, 64, 0.88) 55%, rgba(6, 23, 43, 0.96) 100%),
                url('https://images.unsplash.com/photo-1587854692152-cbe660dbde88?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.tq-hero-info h1 {
    color: #FFFFFF !important;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 0 0 2px 0;
}

.tq-hero-info p {
    color: #E2E8F0 !important;
    font-size: 0.8rem;
    line-height: 1.3;
    margin: 0;
    max-width: 650px;
}

.tq-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 168, 150, 0.28);
    border: 1px solid var(--tq-cyan-bright);
    color: #A7F3D0 !important;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 14px;
    margin-bottom: 2px;
}

.tq-hero-nav {
    display: flex;
    gap: 6px;
}

.tq-nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #FFFFFF !important;
    text-decoration: none !important;
    font-size: 0.74rem;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.tq-nav-pill:hover {
    background: rgba(0, 168, 150, 0.35);
    border-color: var(--tq-cyan-bright);
}

/* =========================================================================
   PESTAÑAS DE NAVEGACIÓN
   ========================================================================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 2px solid var(--tq-border);
    padding: 0;
    margin-bottom: 8px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: var(--tq-text-secondary) !important;
    background: var(--tq-surface) !important;
    border: 1px solid var(--tq-border) !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 7px 16px !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    color: #FFFFFF !important;
    background: var(--tq-cyan) !important;
    border-color: var(--tq-cyan) !important;
}

/* ENCABEZADOS DE PANELES */
.tq-chat-header-bar {
    background: var(--tq-surface);
    border: 1px solid var(--tq-border);
    border-radius: 8px;
    padding: 7px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.tq-chat-header-bar h3 {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--tq-text-primary);
    margin: 0;
}

/* BURBUJAS DE CHAT */
[data-testid="stChatMessage"] {
    background-color: var(--tq-surface) !important;
    border: 1px solid var(--tq-border) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    color: var(--tq-text-primary) !important;
}

[data-testid="stChatMessage"] * {
    color: var(--tq-text-primary) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) {
    background-color: var(--tq-chat-container-bg) !important;
    border: 1px solid var(--tq-border) !important;
    border-radius: 8px !important;
    overflow-x: hidden !important;
}

/* PANELES DE CONTENIDO EN TABS */
.tq-panel {
    background: var(--tq-surface);
    border: 1px solid var(--tq-border);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

.tq-panel h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--tq-text-primary);
    margin: 0 0 4px 0;
}

.tq-panel p {
    font-size: 0.82rem;
    color: var(--tq-text-secondary);
    margin: 0 0 10px 0;
}

.tq-markdown-container {
    background: var(--tq-surface-hover);
    border: 1px solid var(--tq-border);
    border-left: 4px solid var(--tq-cyan);
    border-radius: 8px;
    padding: 18px 24px;
    margin-top: 10px;
    max-height: 52vh;
    overflow-y: auto;
}

.tq-markdown-container h1, .tq-markdown-container h2, .tq-markdown-container h3 {
    color: var(--tq-cyan-bright) !important;
    margin-top: 10px;
    margin-bottom: 6px;
    font-weight: 700;
}

.tq-markdown-container strong {
    color: var(--tq-cyan-bright) !important;
}

.tq-markdown-container p, .tq-markdown-container li {
    font-size: 0.88rem !important;
    color: #E2E8F0 !important;
    line-height: 1.55 !important;
}

/* =========================================================================
   REDISEÑO DE BOTONES: INGENIERÍA FRONTEND DISTINTIVA (FRONTEND-DESIGN SKILL)
   - Gradiente de alta tecnología farmacéutica
   - Micro-interacción con resplandor cian reactivo
   - Sin sombras genéricas ("no AI slop"), tipografía con espaciado de precisión
   ========================================================================= */
.stButton > button {
    background: linear-gradient(135deg, #0A2540 0%, #0F3860 60%, #007A6C 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0, 196, 159, 0.45) !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 14px rgba(10, 37, 64, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0D3359 0%, #00A896 70%, #00C49F 100%) !important;
    border-color: #00E5BC !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 168, 150, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 8px rgba(0, 168, 150, 0.2) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SIDEBAR: ALINEADO ARRIBA AL NIVEL EXACTO DEL HERO SECTION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
    <div class="tq-sidebar-head">
        <h2>Tecnoquímicas S.A.</h2>
        <p>Núcleo Semántico Corporativo</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("✨ Nueva consulta", use_container_width=True):
        new_id = f"Consulta #{len(st.session_state.conversations) + 1}"
        st.session_state.conversations[new_id] = [
            {
                "role": "assistant",
                "content": f"Nueva sesión iniciada (**{new_id}**). ¿Qué consulta deseas formular sobre el portafolio de Tecnoquímicas?",
            }
        ]
        st.session_state.current_chat_id = new_id
        st.rerun()

    chat_names = list(st.session_state.conversations.keys())
    selected_chat = st.selectbox(
        "Seleccionar conversación activa:",
        options=chat_names,
        index=chat_names.index(st.session_state.current_chat_id),
        label_visibility="collapsed",
    )
    if selected_chat != st.session_state.current_chat_id:
        st.session_state.current_chat_id = selected_chat
        st.rerun()

    st.caption(
        f"Conversación activa: **{len(st.session_state.conversations[st.session_state.current_chat_id])}** mensajes."
    )

    context_length = len(service.context) if service.context else 0
    words_approx = len(service.context.split()) if service.context else 0

    st.markdown(
        f"""
    <div class="tq-metric-tile">
        <div class="tq-metric-label">
            <span>Base Semántica Indexada</span>
            <span>✓ Válido</span>
        </div>
        <div class="tq-metric-number">{context_length:,} <span style="font-size:0.7rem; font-weight:500; color:#94A3B8;">caracteres</span></div>
        <div class="tq-metric-sub">~{words_approx:,} palabras verificadas</div>
    </div>

    <div class="tq-metric-tile">
        <div class="tq-metric-label">
            <span>Motor de Inferencia</span>
            <span>LCEL</span>
        </div>
        <div class="tq-metric-number">{config.llm_model}</div>
        <div class="tq-metric-sub">Restricción anti-alucinaciones</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="tq-sidebar-links">
        <a href="https://www.tqconfiable.com" target="_blank" class="tq-source-link">
            <span>TQ Confiable (Corporativo)</span>
            <span style="color:var(--tq-cyan-bright);">↗</span>
        </a>
        <a href="https://www.tqfarma.com" target="_blank" class="tq-source-link">
            <span>TQ Farma (Línea Médica)</span>
            <span style="color:var(--tq-cyan-bright);">↗</span>
        </a>
        <a href="https://www.tqconfiable.com/marcas" target="_blank" class="tq-source-link">
            <span>Catálogo de Marcas</span>
            <span style="color:var(--tq-cyan-bright);">↗</span>
        </a>
        <a href="https://brgrupodesoluciones.com" target="_blank" class="tq-source-link" style="border-color: rgba(0, 168, 150, 0.4);">
            <span style="color: #00C49F !important;">BR Solutions Group</span>
            <span style="color: #00C49F;">⚡</span>
        </a>
    </div>
    """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# HERO SECTION COMPACTA
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="tq-hero">
    <div class="tq-hero-info">
        <div class="tq-status-badge">
            <span>● NÚCLEO RAG DOCUMENTADO</span>
            <span>|</span>
            <span>TECNOQUÍMICAS S.A.</span>
        </div>
        <h1>Inteligencia Semántica Farmacéutica</h1>
        <p>
            Sistema de consulta estratégica respaldado exclusivamente en datos auditados de Tecnoquímicas S.A.
            Trazabilidad completa en líneas terapéuticas, manufactura y operaciones comerciales.
        </p>
    </div>
    <div class="tq-hero-nav">
        <a href="https://www.tqconfiable.com/quienes-somos" target="_blank" class="tq-nav-pill">
            Empresa TQ ↗
        </a>
        <a href="https://www.tqfarma.com" target="_blank" class="tq-nav-pill">
            Línea Farma ↗
        </a>
        <a href="https://brgrupodesoluciones.com" target="_blank" class="tq-nav-pill" style="border-color: var(--tq-cyan-bright);">
            BR Solutions ↗
        </a>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES DE TRABAJO (3 TAREAS REQUERIDAS)
# -----------------------------------------------------------------------------
tab_qa, tab_summary, tab_faq = st.tabs(
    ["💬 Asistente Q&A Grounded", "📑 Resumen Ejecutivo", "❓ Preguntas Frecuentes"]
)

# -----------------------------------------------------------------------------
# 1. PESTAÑA Q&A: LAYOUT 50/50 ALINEADO EXACTO CON LA PARTE INFERIOR DEL INPUT
# -----------------------------------------------------------------------------
with tab_qa:
    col_chat, col_gallery = st.columns([1, 1], gap="medium")

    # MITAD IZQUIERDA: BLOQUE HEADER + VENTANA DE MENSAJES + INPUT TEXTUAL
    with col_chat:
        st.markdown(
            f"""
        <div class="tq-chat-header-bar">
            <div>
                <h3>Asistente de Consulta Grounded</h3>
                <span style="font-size:0.72rem; color:var(--tq-text-secondary);">
                    Hilo activo: <strong style="color:var(--tq-cyan);">{st.session_state.current_chat_id}</strong>
                </span>
            </div>
            <span style="background:var(--tq-cyan-surface); border:1px solid var(--tq-cyan); color:var(--tq-cyan); font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:4px;">
                Cero Alucinaciones
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        active_messages = st.session_state.conversations[st.session_state.current_chat_id]

        chat_container = st.container(height=425, border=True)
        with chat_container:
            for msg in active_messages:
                role = msg["role"]
                content = msg["content"]
                avatar_icon = "👤" if role == "user" else "🧬"
                with st.chat_message(role, avatar=avatar_icon):
                    st.markdown(content)

        if prompt := st.chat_input("Escribe tu consulta sobre Tecnoquímicas..."):
            active_messages.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)

                with st.chat_message("assistant", avatar="🧬"):
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk in service.answer_question_stream(prompt):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)

            active_messages.append({"role": "assistant", "content": full_response})
            st.rerun()

    # MITAD DERECHA: CARRUSEL VERTICAL CALIBRADO A 575px (ALTURA EXACTA AL BORDE INFERIOR DEL INPUT)
    with col_gallery:
        carousel_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8"/>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }
            body {
                background: transparent;
                padding: 0;
                overflow: hidden;
            }
            .card-wrapper {
                background: #0C1E34;
                border: 1px solid #1B3658;
                border-radius: 8px;
                padding: 14px 16px;
                height: 565px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 4px 16px rgba(0,0,0,0.15);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #1B3658;
                padding-bottom: 8px;
                height: 38px;
            }
            .header h3 {
                font-size: 0.95rem;
                font-weight: 800;
                color: #F8FAFC;
            }
            .badge-live {
                font-size: 0.68rem;
                font-weight: 700;
                background: rgba(0, 168, 150, 0.18);
                color: #00C49F;
                border: 1px solid #00A896;
                padding: 2px 8px;
                border-radius: 12px;
            }
            .slider-viewport {
                position: relative;
                width: 100%;
                height: 395px;
                border-radius: 8px;
                overflow: hidden;
                background: #02070E;
                margin: 8px 0;
            }
            .slide {
                position: absolute;
                inset: 0;
                opacity: 0;
                transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .slide.active {
                opacity: 1;
            }
            .slide img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .slide-overlay {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(180deg, transparent 0%, rgba(5, 14, 26, 0.95) 55%, rgba(5, 14, 26, 0.98) 100%);
                padding: 20px 16px 16px 16px;
            }
            .tag {
                font-size: 0.68rem;
                font-weight: 800;
                text-transform: uppercase;
                color: #00E5BC;
                letter-spacing: 0.05em;
            }
            .slide-title {
                font-size: 1.15rem;
                font-weight: 800;
                color: #FFFFFF;
                margin: 2px 0 4px 0;
            }
            .slide-desc {
                font-size: 0.78rem;
                color: #E2E8F0;
                line-height: 1.4;
            }
            .footer-row {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .dots-container {
                display: flex;
                justify-content: center;
                gap: 8px;
            }
            .dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #1B3658;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .dot.active {
                width: 22px;
                border-radius: 4px;
                background: #00A896;
            }
            .action-link {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #122947;
                border: 1px solid #1B3658;
                border-radius: 6px;
                padding: 10px 14px;
                text-decoration: none;
                color: #F8FAFC;
                font-size: 0.8rem;
                font-weight: 700;
                transition: all 0.2s ease;
            }
            .action-link:hover {
                border-color: #00A896;
                background: rgba(0, 168, 150, 0.15);
            }
        </style>
        </head>
        <body>
        <div class="card-wrapper">
            <div class="header">
                <h3>Plantas & Portafolio TQ</h3>
                <span class="badge-live">● Rotación Automática</span>
            </div>

            <div class="slider-viewport" id="viewport">
                <!-- Slide 0 -->
                <div class="slide active">
                    <img src="https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=1000&q=80" alt="Bonfiest Lua"/>
                    <div class="slide-overlay">
                        <span class="tag">Bienestar Digestivo</span>
                        <div class="slide-title">Bonfiest Lúa & Sal de Frutas</div>
                        <p class="slide-desc">Líderes indiscutibles en el mercado de antiácidos y digestivos efervescentes en Colombia y la región.</p>
                    </div>
                </div>

                <!-- Slide 1 -->
                <div class="slide">
                    <img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1000&q=80" alt="CureBand"/>
                    <div class="slide-overlay">
                        <span class="tag">Primeros Auxilios</span>
                        <div class="slide-title">CureBand Adhesivos</div>
                        <p class="slide-desc">Tecnología adhesiva hipoalergénica de alto rendimiento hospitalario y protección de heridas.</p>
                    </div>
                </div>

                <!-- Slide 2 -->
                <div class="slide">
                    <img src="https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=1000&q=80" alt="Yodora"/>
                    <div class="slide-overlay">
                        <span class="tag">Cuidado Personal</span>
                        <div class="slide-title">Yodora Desodorante</div>
                        <p class="slide-desc">Protección tradicional y confianza para el cuidado diario en millones de hogares con más de 70 años.</p>
                    </div>
                </div>

                <!-- Slide 3 -->
                <div class="slide">
                    <img src="https://images.unsplash.com/photo-1587854692152-cbe660dbde88?auto=format&fit=crop&w=1000&q=80" alt="TQ Farma"/>
                    <div class="slide-overlay">
                        <span class="tag">Prescripción Médica</span>
                        <div class="slide-title">TQ Farma Especialidades</div>
                        <p class="slide-desc">Plantas farmacéuticas certificadas Invima y FDA con líneas terapéuticas y cardiometabólicas de alta pureza.</p>
                    </div>
                </div>
            </div>

            <div class="footer-row">
                <div class="dots-container">
                    <div class="dot active" onclick="gotoSlide(0)"></div>
                    <div class="dot" onclick="gotoSlide(1)"></div>
                    <div class="dot" onclick="gotoSlide(2)"></div>
                    <div class="dot" onclick="gotoSlide(3)"></div>
                </div>
                <a href="https://www.tqconfiable.com" target="_blank" class="action-link" id="ext-link">
                    <span id="link-text">Ver catálogo en TQ Confiable</span>
                    <span style="color:#00C49F;">↗</span>
                </a>
            </div>
        </div>

        <script>
            const slides = document.querySelectorAll('.slide');
            const dots = document.querySelectorAll('.dot');
            const extLink = document.getElementById('ext-link');
            const linkText = document.getElementById('link-text');

            const linkData = [
                { text: "Ver Bonfiest en TQ Confiable", url: "https://www.tqconfiable.com" },
                { text: "Conocer apósitos CureBand", url: "https://www.tqconfiable.com" },
                { text: "Explorar portafolio Yodora", url: "https://www.tqconfiable.com" },
                { text: "Acceder al portal TQ Farma", url: "https://www.tqfarma.com" }
            ];

            let currentIndex = 0;
            let timer = null;

            function showSlide(index) {
                slides[currentIndex].classList.remove('active');
                dots[currentIndex].classList.remove('active');

                currentIndex = (index + slides.length) % slides.length;

                slides[currentIndex].classList.add('active');
                dots[currentIndex].classList.add('active');
                linkText.innerText = linkData[currentIndex].text;
                extLink.href = linkData[currentIndex].url;
            }

            function gotoSlide(index) {
                clearInterval(timer);
                showSlide(index);
                startAuto();
            }

            function startAuto() {
                timer = setInterval(() => {
                    showSlide(currentIndex + 1);
                }, 3800);
            }

            startAuto();
        </script>
        </body>
        </html>
        """
        components.html(carousel_html, height=575)

# -----------------------------------------------------------------------------
# 2. PESTAÑA DE RESUMEN EJECUTIVO (RENDERIZADO NATIVO MARKDOWN)
# -----------------------------------------------------------------------------
with tab_summary:
    st.markdown(
        """
    <div class="tq-panel">
        <h3>Síntesis Ejecutiva de Tecnoquímicas S.A.</h3>
        <p>
            Genera un informe condensado sobre la trayectoria, capacidad manufacturera y marcas insignia a partir del corpus extraído de los portales de TQ.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_btn_sum, _ = st.columns([1, 3])
    with col_btn_sum:
        btn_sum = st.button(
            "⚡ Generar síntesis ejecutiva", key="btn_summary_exec", use_container_width=True
        )

    if btn_sum:
        with st.spinner("Procesando síntesis corporativa con LangChain y Ollama..."):
            summary_buffer = ""
            for chunk in service.get_summary_stream():
                summary_buffer += chunk
            st.session_state.executive_summary_content = summary_buffer
        st.rerun()

    if st.session_state.executive_summary_content:
        st.markdown('<div class="tq-markdown-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.executive_summary_content)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. PESTAÑA DE PREGUNTAS FRECUENTES (RENDERIZADO NATIVO MARKDOWN)
# -----------------------------------------------------------------------------
with tab_faq:
    st.markdown(
        """
    <div class="tq-panel">
        <h3>Preguntas Frecuentes Automatizadas</h3>
        <p>
            Extracción estructurada de inquietudes frecuentes sobre laboratorios, plantas, distribución comercial y certificaciones Invima.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_btn_faq, _ = st.columns([1, 3])
    with col_btn_faq:
        btn_faq = st.button(
            "🔍 Extraer preguntas frecuentes", key="btn_faq_exec", use_container_width=True
        )

    if btn_faq:
        with st.spinner("Extrayendo preguntas y respuestas frecuentes del corpus..."):
            faq_buffer = ""
            for chunk in service.get_faq_stream():
                faq_buffer += chunk
            st.session_state.faq_content = faq_buffer
        st.rerun()

    if st.session_state.faq_content:
        st.markdown('<div class="tq-markdown-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.faq_content)
        st.markdown("</div>", unsafe_allow_html=True)
