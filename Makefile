# =============================================================================
# Módulo 1: Knowledge Core — automatización de tareas
# =============================================================================

.DEFAULT_GOAL := help
.PHONY: help install dev pre-commit-install pre-commit lint format format-check test check scrape app build clean

help: ## Muestra esta ayuda
	@python -c "import re; [print(f'  \033[36m{m.group(1):<18}\033[0m {m.group(2)}') for line in open('Makefile', encoding='utf-8') if (m := re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line))]"

install: ## Sincroniza el entorno virtual e instala dependencias
	uv sync

dev: install pre-commit-install ## Prepara el entorno de desarrollo (sync + hooks)

pre-commit-install: ## Instala los hooks de pre-commit en el repositorio local
	uv run pre-commit install

pre-commit: ## Ejecuta todos los hooks de pre-commit sobre el repositorio
	uv run pre-commit run --all-files

lint: ## Ejecuta Ruff (lint)
	uv run ruff check .

format: ## Formatea el código con Ruff
	uv run ruff format .

format-check: ## Verifica el formato sin modificarlo
	uv run ruff format --check .

test: ## Ejecuta las pruebas unitarias con pytest
	uv run pytest

scrape: ## Ejecuta el pipeline de scraping Medallion (Bronze -> Silver -> Gold)
	uv run python -m src.ingestion.crawler

app: ## Inicia la interfaz web Streamlit de grado farmacéutico
	uv run streamlit run app/main.py

check: lint format-check test ## Verificación completa (lint + formato + pruebas)

build: ## Construye el paquete (sdist + wheel)
	uv build

clean: ## Limpia cachés y artefactos temporales
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', 'dist', 'build', 'htmlcov', '.coverage'] if pathlib.Path(p).exists()]"
