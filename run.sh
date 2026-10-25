#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  Iniciando Tecnoquimicas AI - Núcleo Semántico (Mód 1) "
echo "========================================================"
echo ""

# 1. Verificar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo "[INFO] uv no detectado. Instalando uv (Astral)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.local/bin/env" 2>/dev/null || true
fi

# 2. Sincronizar dependencias
echo "[1/3] Sincronizando entorno y dependencias..."
uv sync --quiet
uv run playwright install chromium > /dev/null 2>&1

# 3. Descargar modelo en Ollama
echo "[2/3] Verificando modelo llama3.2 en Ollama..."
if command -v ollama &> /dev/null; then
    ollama pull llama3.2
else
    echo "[ADVERTENCIA] Ollama no detectado en PATH. Asegúrate de iniciarlo manualmente."
fi

# 4. Lanzar Streamlit
echo "[3/3] Desplegando interfaz web..."
uv run streamlit run app/main.py
