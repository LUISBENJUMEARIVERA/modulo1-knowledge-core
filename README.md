# 🧬 Tecnoquímicas AI — Enterprise Web Scraper & Cognitive RAG Knowledge Studio

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain LCEL](https://img.shields.io/badge/orchestration-LangChain%20LCEL-1C3C3C.svg)](https://python.langchain.com/)
[![Playwright](https://img.shields.io/badge/crawler-Playwright%20Async-2EAD33.svg)](https://playwright.dev/)
[![Ollama](https://img.shields.io/badge/inference-Ollama%20llama3.2-black.svg)](https://ollama.com/)
[![Streamlit UI](https://img.shields.io/badge/ui-Streamlit%20Dark-FF4B4B.svg)](https://streamlit.io/)

> **Language / Idioma:** **English (Default)** | [🇪🇸 Leer en Español](#-versión-en-español)

---

## 🇬🇧 English Version (Default)

An enterprise-grade, resilient web crawling, semantic extraction, and grounded Q&A intelligence platform built for **Tecnoquímicas S.A. (TQ Group)**. Designed under pharmaceutical rigor to ensure zero hallucinations and absolute document traceability.

### 🏛 System Architecture
* **Dynamic Headless Ingestion:** Asynchronous crawler orchestrated with **Playwright**, handling full client-side JavaScript hydration, dynamic rendering, and SPA navigation.
* **Agnostic & Self-Healing Extraction:** Text-density heuristic extraction using **Trafilatura** to isolate high-value clinical and corporate content without relying on brittle CSS selectors.
* **Declarative Orchestration:** Strict type-safe pipelines built with **LangChain LCEL (LangChain Expression Language)** delivering:
  1. *Executive Corporate Synthesis.*
  2. *Automated Pharmaceutical FAQ Mining.*
  3. *Zero-Shot Grounded Q&A Assistant with Strict Negative Coercion (anti-hallucination).*
* **Local Sovereign Inference:** Powered by open-source `llama3.2` executed on **Ollama** for full data privacy and low-latency token streaming.
* **Pharmaceutical-Grade UI (Dark Mode):** Interactive studio built with **Streamlit** following Anthropic's `frontend-design` principles:
  - 50/50 dual-column viewport layout aligned with the input box.
  - Gemini-style fixed height message container (`height=425`) with internal scrollbar.
  - Auto-rotating dynamic image carousel (every 3.8s) featuring flagship TQ products and certified manufacturing facilities.
  - Multi-session chat thread manager with state persistence across tabs.
* **Benchmark & Evaluation Harness:** Automated testing framework auditing 20 test cases (*In-Scope*, *Complex Cross-Domain*, and *Adversarial Out-of-Scope*).

---

### ⚡ Quickstart (One-Liner / Copy & Paste)

Copy and run the following in your terminal to clone, automatically provision dependencies, download the model, and launch the studio:

#### Windows (PowerShell / Command Prompt):
```powershell
git clone https://github.com/LUISBENJUMEARIVERA/scrapping.git && cd scrapping && .\run.bat
```

#### macOS / Linux:
```bash
git clone https://github.com/LUISBENJUMEARIVERA/scrapping.git && cd scrapping && chmod +x run.sh && ./run.sh
```

---

### 📂 Repository Structure

```text
scrapping/
├── .agents/
│   └── skills/
│       └── frontend-design/      # Anthropic official frontend design skill
├── app/
│   └── main.py                   # High-end pharmaceutical dark-mode Streamlit UI
├── data/
│   ├── processed/                # Normalized semantic knowledge corpus
│   └── raw/                      # Extracted raw HTML/Text payloads
├── src/
│   ├── chains/
│   │   ├── prompts.py            # LangChain LCEL prompts with negative coercion
│   │   └── tasks.py              # Knowledge streaming service
│   ├── core/
│   │   ├── benchmark_runner.py   # 20-case automated evaluation suite
│   │   ├── config.py             # Domain policies, depth, and crawler configuration
│   │   └── llm_factory.py        # Ollama llama3.2 connector
│   └── ingestion/
│       ├── crawler.py            # Playwright async crawler
│       └── extractor.py          # Trafilatura agnostic heuristic extractor
├── pyproject.toml                # Dependencies managed by Astral uv
├── run.bat                       # Windows one-click launcher
└── run.sh                        # Linux / macOS launcher
```

---

<br>

---

## 🇪🇸 Versión en Español

Sistema empresarial de ingesta web resiliente, modelado semántico y arquitectura de consulta Q&A anclada (*grounded*) sobre **Tecnoquímicas S.A. (Grupo TQ)**, desarrollado bajo estándares de rigor farmacéutico para garantizar cero alucinaciones y estricta trazabilidad documental.

### 🏛 Arquitectura de la Solución
* **Ingesta Dinámica:** Motor asíncrono con **Playwright** que resuelve la hidratación de JavaScript y Single Page Applications.
* **Extracción Agnóstica (Self-Healing):** Algoritmos de densidad textual con **Trafilatura** que aíslan el contenido central sin depender de selectores CSS frágiles.
* **Orquestación Declarativa:** Pipelines tipados con **LangChain LCEL** cubriendo tres tareas esenciales:
  1. *Resumen Corporativo Ejecutivo.*
  2. *Preguntas Frecuentes (FAQ) Dinámicas.*
  3. *Asistente Q&A Grounded con Coerción Negativa Estricta.*
* **Inferencia Local:** Modelo open-source `llama3.2` vía **Ollama**, asegurando privacidad y latencias mínimas.
* **Interfaz de Grado Farmacéutico (Dark Mode):** Dashboard interactivo en **Streamlit** aplicando la skill oficial de Anthropic `frontend-design`:
  - Distribución simétrica 50/50 con alineación milimétrica con la barra de entrada.
  - Contenedor de chat tipo Gemini (`height=425`) con scroll interno.
  - Carrusel automático de imágenes (cada 3.8s) con marcas insignias y complejos industriales TQ.
  - Gestor multi-sesión de conversaciones con persistencia entre pestañas.
* **Evaluación Sistemática:** Arnés de pruebas automatizado con una matriz de 20 casos (*In-Scope*, *Complex Semantic* y *Out-of-Scope Adversarial*).

---

### ⚡ Inicio Rápido (Copiar y Pegar)

#### En Windows (PowerShell / CMD):
```powershell
git clone https://github.com/LUISBENJUMEARIVERA/scrapping.git && cd scrapping && .\run.bat
```

#### En macOS y Linux:
```bash
git clone https://github.com/LUISBENJUMEARIVERA/scrapping.git && cd scrapping && chmod +x run.sh && ./run.sh
```

---

### 🌐 Portales Oficiales Vinculados
* [Tecnoquímicas Confiable (Corporativo)](https://www.tqconfiable.com)
* [TQ Farma (Línea Médica Especializada)](https://www.tqfarma.com)
* [Catálogo de Marcas TQ](https://www.tqconfiable.com/marcas)
* [BR Solutions Group](https://brgrupodesoluciones.com)
