# CONSTITUTION — Módulo 1: Knowledge Core

> **Verdad central del proyecto.** Este documento define el propósito, el stack, la
> estructura, las convenciones y el flujo de trabajo de `Módulo 1: Knowledge Core`. Si algo aquí
> contradice al código, el código manda **y este archivo se actualiza**.

> ⚠️ **Directiva de mantenimiento:** cada vez que se realicen cambios significativos
> (nuevas funcionalidades, cambios arquitectónicos, adición de clases/módulos o ajustes
> de tecnologías), **se debe actualizar este archivo en el mismo commit** para mantener
> la verdad central del proyecto bien documentada.

---

## 0. Identidad del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | Módulo 1: Knowledge Core |
| **Descripción** | Núcleo de Inteligencia y Extracción de Conocimiento de Tecnoquímicas S.A. con LCEL y Web Scraping |
| **Repositorio** | https://github.com/LUISBENJUMEARIVERA/scrapping |
| **Autoría** | Luis Benjumea — luisantoniobenjumeaia@gmail.com |
| **Licencia** | MIT |
| **Rama principal** | `main` |
| **Estado** | Producción / Certificado (100% Benchmark & Tests) ✅ |

## 1. Propósito y no-propósito

### Propósito

Proveer a Tecnoquímicas S.A. de un núcleo soberano, reproducible y auditable de extracción web (Playwright + Trafilatura) y consulta inteligente de conocimiento corporativo mediante cadenas LCEL (LangChain Expression Language) y modelos locales (Ollama `llama3.2`), asegurando 100% de veracidad factual y cero alucinaciones farmacéuticas.

### No-propósito

- No es un chatbot generalista de entretenimiento ni un motor de búsqueda web abierta.
- No responde consultas especulativas, precios en comercios externos, ni opiniones sobre competidores ajenos a Tecnoquímicas (aplica protocolo estricto de rechazo Out-of-Scope).
- No transmite datos sensibles ni propiedad intelectual a APIs en la nube pública; prioriza inferencia local soberana.
- No gestiona pasarelas de pago ni pedidos de distribución farmacéutica transaccional.

## 2. Alcance

### Dentro del alcance

- **Rastreo Web Asíncrono:** Crawling de portales oficiales (`tqconfiable.com`, `tqfarma.com`) con Playwright Chromium y control de profundidad.
- **Extracción Resiliente:** Limpieza semántica de HTML con `trafilatura` y fallback heurístico con `BeautifulSoup4`.
- **Persistencia de Datos Medallion:** Almacenamiento en tres capas (Bronze en `data/raw/`, Silver en `data/processed/` y Gold estructurado en `data/gold/corpus.jsonl` con metadatos: URL, título, fecha, hash SHA-256 y tokens, además de `metrics.json`).
- **Cadenas LCEL:** Resumen Ejecutivo Corporativo (`SUMMARY_PROMPT`), Generación de 5 FAQs operativas (`FAQ_PROMPT`) y Motor Q&A con rechazo calibrado y cita verificada de fuentes (`QA_PROMPT`).
- **Interfaz Streamlit:** Dashboard farmacéutico grado producción (Cold Slate, Cobalt Blue `#002F6C`, Crimson Accent `#D32F2F`) con streaming reactivo de tokens.
- **Aseguramiento de Calidad:** Benchmark evaluativo con métricas cuantitativas (`data/evaluation/benchmark_results.md`) y suite de pruebas unitarias (`pytest`).
- **Arquitectura Viva:** Especificación formal del sistema en `docs/SDD.md` y diagrama interactivo Archify en `docs/arquitectura.html`.

### Fuera del alcance (por ahora)

- Integración con base de datos vectorial distribuida externa (planificada para fases posteriores con Qdrant / Chroma).
- Autenticación SSO empresarial mediante Active Directory corporativo.
- Transcripción de contenido multimedia (audio/video).

## 3. Stack técnico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.12+ (fijado en `.python-version`) |
| **Gestor de paquetes y entorno** | [`uv`](https://docs.astral.sh/uv/) (Astral) |
| **Build backend** | `uv_build` (src-layout) |
| **Paquete Python** | `modulo1_knowledge_core` |
| **Orquestación LLM** | LangChain Core + LCEL (`langchain-core`, `langchain-ollama`) |
| **Motor de Inferencia** | Ollama (`llama3.2`) en entorno local |
| **Web Scraping** | Playwright Chromium, BeautifulSoup4, Trafilatura |
| **Frontend / UI** | Streamlit con inyección CSS corporativa y streaming |
| **Testing** | [`pytest`](https://docs.pytest.org/) con fixtures y mocks aislados |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) (Astral) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) (higiene, ruff, uv-lock) |
| **CI/CD** | [GitHub Actions](.github/workflows/ci.yml) |
| **Diagramas de arquitectura** | [Archify](https://github.com/tt-a1i/archify) (HTML interactivo en `docs/arquitectura.html`) |
| **Gobernanza GitHub** | Dependabot, Issue templates, Pull Request template, Labels |

> ⚠️ **Regla dura:** toda gestión de dependencias y entornos pasa por `uv`. Está
> **prohibido** `pip` y `requirements.txt`. El archivo `uv.lock` **sí se versiona**.

## 4. Estructura del repositorio

```text
scrapping/
├── .github/                         # gobernanza GitHub
│   ├── ISSUE_TEMPLATE/              # plantillas de issues (bug, feature, spike)
│   ├── workflows/                   # CI automatizado y sincronizador de etiquetas
│   ├── dependabot.yml               # actualización de dependencias
│   ├── labels.yml                   # catálogo declarativo de etiquetas
│   └── pull_request_template.md     # plantilla estandarizada de PR
├── .opencode/rules/tgrep.md         # regla de indexación para agentes
├── app/
│   └── main.py                      # interfaz gráfica Streamlit farmacéutica
├── data/
│   ├── evaluation/                  # preguntas de test y resultados de benchmark
│   ├── processed/                   # knowledge_base.txt (corpus depurado)
│   └── raw/                         # snapshots HTML del crawler
├── docs/
│   ├── SDD.md                       # Software Design Description (IEEE 1016)
│   ├── technical_report.md          # reporte técnico de implementación
│   ├── arquitectura.json            # especificación fuente de arquitectura (Archify)
│   ├── arquitectura.html            # diagrama interactivo autocontenido
│   └── arquitectura.visual-check.*  # capturas y verificación visual en navegador
├── src/
│   ├── chains/                      # plantillas de prompts y servicio LCEL
│   ├── core/                        # configuración, fábrica LLM y runner de benchmark
│   ├── ingestion/                   # crawler asíncrono y extractor resiliente
│   └── modulo1_knowledge_core/      # entry point del paquete
├── tests/                           # suite completa de pruebas unitarias (pytest)
├── AGENTS.md                        # contexto operativo para agentes LLM
├── CONSTITUTION.md                  # este documento — fuente única de verdad
├── CONTRIBUTING.md                  # guía de contribución
├── CODE_OF_CONDUCT.md               # código de conducta
├── LICENSE                          # licencia MIT
├── Makefile                         # automatización de comandos (make check, make dev)
├── pyproject.toml                   # metadatos, herramientas (Ruff, pytest) y dependencias
├── README.md                        # documentación de bienvenida y presentación
├── run.bat                          # ejecutor de despliegue para Windows
├── run.sh                           # ejecutor de despliegue para Unix/macOS
├── uv.lock                          # lockfile determinista de uv
├── .editorconfig                    # formato homogéneo entre editores
├── .gitignore                       # exclusión estricta de artefactos
├── .pre-commit-config.yaml          # hooks de calidad pre-commit
└── .python-version                  # versión de Python fijada (3.12)
```

## 5. Convenciones de código

- **Estilo:** [PEP 8](https://peps.python.org/pep-0008/), impuesto por **Ruff** (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones de tipos estándar de Python 3.12 (`list[str]`, `set[str]`, `dict`).
- **Nomenclatura:** `snake_case` (funciones/variables), `PascalCase` (clases), `UPPER_CASE` (constantes de prompts).
- **Docstrings:** en módulos, clases y funciones públicas describiendo parámetros y retornos.
- **Pruebas:** `pytest` con el patrón **AAA** (*Arrange · Act · Assert*), mocks de I/O y cero dependencias de hardware.
- **Idioma:** Documentación, UI y commits en español; identificadores de código en inglés técnico.
- **Reglas del dominio farmacéutico:**
  - Respuestas al usuario sustentadas 100% en `<knowledge_base>`.
  - Cero respuestas basadas en conjeturas sobre posología o contraindicaciones médicas no presentes en el corpus.
  - Rechazo exacto y cortés ante preguntas fuera de alcance (OOS).

## 6. Calidad y automatización

| Herramienta | Rol | Comando |
|-------------|-----|---------|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint | `make lint` (`uv run ruff check .`) |
| Ruff | Formato | `make format` (`uv run ruff format .`) |
| `pytest` | Pruebas unitarias | `make test` (`uv run pytest`) |
| `pre-commit` | Hooks antes de cada commit | `make pre-commit` (`uv run pre-commit run --all-files`) |
| GitHub Actions | CI (pre-commit + pruebas) | `.github/workflows/ci.yml` |

- Ningún commit se salta los hooks (`--no-verify` está prohibido salvo causa justificada y documentada).
- La **CI debe estar en verde** antes de fusionar un Pull Request.
- Toda dependencia nueva entra con `uv add` / `uv add --dev` (nunca editando `uv.lock` a mano).

## 7. Repositorio y Git

- **Remoto (HTTPS):** `https://github.com/LUISBENJUMEARIVERA/scrapping.git`
- **Remoto (SSH):** `git@github.com:LUISBENJUMEARIVERA/scrapping.git`
- **Rama principal:** `main`
- **Estrategia de ramas:** `feat/...`, `fix/...`, `docs/...`, `refactor/...`, `test/...`, `chore/...`; integración vía Pull Request.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) —
  `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`, `chore:`.

## 8. Flujo diario (commit + push)

```bash
# 1. Ver cambios
git status

# 2. Verificación completa (lint + formato + pruebas)
make check

# 3. Agregar y commitear (los hooks se ejecutan solos)
git add -A
git commit -m "tipo: mensaje descriptivo"

# 4. Subir a GitHub
git push origin main
```

## 9. Historial de decisiones técnicas

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 2026-10-27 | Adoptar `uv` como gestor único de entornos y dependencias | Velocidad extrema y reproducibilidad determinista con `uv.lock`. |
| 2026-10-27 | Adoptar Ruff (lint + formato) y pre-commit | Garantizar calidad continua de código en local y en CI. |
| 2026-10-27 | Adoptar Conventional Commits y gobernanza GitHub | Trazabilidad estructurada de cambios y plantillas de PR/Issues. |
| 2026-10-27 | Redacción de SDD formal bajo estándar IEEE 1016 (`docs/SDD.md`) | Documentación de diseño de software rigurosa y auditable. |
| 2026-10-27 | Integración de diagrama de arquitectura interactivo con Archify | Mapa vivo navegable con verificación automática en navegador real (`docs/arquitectura.html`). |
| 2026-10-27 | Implementación de suite de pruebas unitarias con Pytest (15 pruebas) | Cobertura de configuración, extracción, prompts, cadenas y crawler sin depender de red externa. |
| 2026-10-27 | Protocolo de rechazo calibrado en `QA_PROMPT` | 0% alucinaciones en preguntas farmacéuticas fuera de dominio. |

## 10. Notas y roadmap

- [x] Adoptar estándar `jan-project-standard` completo.
- [x] Redactar SDD exhaustivo (`docs/SDD.md`).
- [x] Generar y verificar diagrama de arquitectura con Archify (`docs/arquitectura.html`).
- [x] Implementar suite unitaria de pytest con patrón AAA (15 pruebas pasando).
- [x] Configurar pre-commit hooks (Ruff, uv-lock, higiene de archivos).
- [x] Configurar gobernanza GitHub (.github con PR template, Issue templates, dependabot, labels, CI workflow).
- [ ] Módulo 2: Integración de Vector Store persistente (Qdrant / Chroma) para búsqueda semántica híbrida.
