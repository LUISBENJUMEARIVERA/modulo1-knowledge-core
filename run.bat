@echo off
setlocal
echo ========================================================
echo   Iniciando Tecnoquimicas AI - Nucleo Semantico (Mod 1)
echo ========================================================
echo.

:: 1. Verificar si uv esta instalado
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] uv no detectado. Instalando uv (Astral)...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

:: 2. Sincronizar dependencias
echo [1/3] Sincronizando entorno virtual y dependencias...
call uv sync --quiet
call uv run playwright install chromium >nul 2>&1

:: 3. Asegurar modelo en Ollama
echo [2/3] Verificando modelo llama3.2 en Ollama...
where ollama >nul 2>&1
if %ERRORLEVEL% equ 0 (
    ollama pull llama3.2
) else (
    echo [ADVERTENCIA] Ollama no encontrado en el PATH. Asegurate de tenerlo corriendo.
)

:: 4. Lanzar la interfaz en Streamlit
echo [3/3] Desplegando aplicacion web...
echo Servidor listo en http://localhost:8501
call uv run streamlit run app/main.py

pause