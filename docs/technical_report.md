# Informe Técnico: Núcleo de Conocimiento Semántico y Sistema Q&A Grounded
**Organización Evaluada:** Tecnoquímicas S.A. (Grupo TQ)  
**Curso:** Técnicas Avanzadas de IA en Modelos de Lenguaje — Módulo 1  
**Stack Tecnológico:** Python 3.12, Astral `uv`, Playwright, Trafilatura, LangChain (LCEL), Ollama (`llama3.2`), Streamlit.

---

## 1. Descripción del Problema
Tecnoquímicas S.A. es una de las corporaciones farmacéuticas y de consumo masivo más influyentes del Valle del Cauca y Colombia. Con un portafolio diversificado que abarca salud humana, consumo masivo, salud animal y agro, la compañía gestiona un volumen crítico de interacciones informativas diarias a través de sus canales digitales.

Los sistemas tradicionales basados en árboles de decisión rígidos o bots de reglas presentan fallas de adaptabilidad lingüística, mientras que los modelos de lenguaje generales (LLMs sin anclaje) introducen riesgos severos de alucinación factual: invención de dosificaciones, cotizaciones no autorizadas o atribución errónea de sedes. Existe la necesidad imperativa de un canal de comunicación automatizado, auditable y fundamentado exclusivamente en la información oficial pública de la compañía.

## 2. Planteamiento de la Solución
Se diseñó un núcleo semántico desacoplado y modular fundamentado en la primera etapa de una arquitectura orientada a RAG (Retrieval-Augmented Generation). El sistema extrae el conocimiento corporativo de forma automatizada y lo consolida como fuente única de verdad en la memoria operativa del LLM mediante inyección estructurada de contexto en el *System Prompt*.

Se integró una política de **coerción negativa estricta (Zero-Hallucination Guardrail)** que fuerza al modelo a rechazar cualquier consulta carente de evidencia documental en el contexto, garantizando fidelidad factual absoluta.

## 3. Preparación de los Datos
Para evitar la fragilidad de los scrapers tradicionales acoplados a selectores CSS/DOM, se implementó un pipeline de ingesta resiliente:
* **Extracción Dinámica:** Empleo de `Playwright Async` con emulación de navegador headless Chromium para asegurar la resolución de JavaScript y eventos de renderizado en `tqconfiable.com` y `tqfarma.com`.
* **Procesamiento Semántico Agnóstico:** Implementación de `Trafilatura`, utilizando algoritmos de densidad textual (Text-to-Tag Ratio) para filtrar de forma automática menús, footers, scripts y banners sin requerir selectores estáticos.
* **Consolidación y Chunking:** El texto curado se estructuró en secciones delimitadas jerárquicamente por URL y título semántico, exportándose al artefacto único canónico `data/processed/knowledge_base.txt`.

## 4. Modelado y Proyección Arquitectónica

### Diseño del Prompt Engineering (Módulo 1)
Se implementaron tres cadenas orquestadas con LangChain Expression Language (LCEL):
1. **Síntesis Ejecutiva:** Prompt zero-shot parametrizado para condensar la identidad corporativa, líneas estratégicas e impacto social.
2. **Generador de FAQs:** Extracción inductiva de los 5 casos de consulta más representativos para usuarios de primer contacto.
3. **Q&A Grounded:** Delimitación explícita mediante etiquetas XML `<knowledge_base>` y directivas de rechazo deterministas:
   > *"Si la respuesta NO está en el contexto o no se deduce con certeza irrefutable, responde exactamente: 'Lo siento, la información disponible en el sistema no contiene datos para responder a esta consulta.'"*

### Especificaciones Proyectadas para el Módulo 2 (RAG Escalable)
* **Modelo de Embeddings:** `text-embedding-3-small` (OpenAI, 1536 dim) o `bge-m3` (Open Source local). Se seleccionan por su alta fidelidad semántica en idioma español y capacidad para procesar terminología médica y farmacológica densa.
* **Base de Datos Vectorial:** `Qdrant` desplegado en Docker. Se elige frente a bases tradicionales por su motor de indexación HNSW escrito en Rust, su soporte nativo para filtrado robusto por metadatos (payload filtering) y su capacidad de búsqueda híbrida (densa + dispersa BM25).
* **LLM Proyectado:** `Llama 3.3 70B` cuantizado localmente vía Ollama para entornos on-premise con privacidad de datos garantizada, con conmutación dinámica hacia `GPT-4o` vía API para escenarios de alta concurrencia.

## 5. Resultados y Discusión de Limitaciones

### Análisis del Benchmark (20 Pruebas)
La evaluación automatizada ejecutada sobre 20 preguntas demostró los siguientes comportamientos:
* **Consultas Factuales Directas (In-Scope):** Precisión del 100% en la recuperación de datos clave como la ciudad sede (Cali), la línea telefónica gratuita nacional (01 8000 523339) y las directrices de talento humano.
* **Robustez Semántica:** El modelo asimiló satisfactoriamente paráfrasis y formulaciones coloquiales manteniendo la exactitud de los datos.
* **Control de Alucinación (Out-of-Scope):** En el 100% de las consultas no documentadas (precios comerciales, composición de junta directiva no listada o comparaciones subjetivas de mercado), el sistema ejecutó el rechazo controlado predefinido sin inventar datos.

### Limitaciones Identificadas
1. **Límite de Context Window:** Al inyectar la base de conocimiento completa en el System Prompt, el costo computacional y el tiempo de Time-To-First-Token (TTFT) aumentan linealmente con el tamaño del corpus corporativo.
2. **Dependencia de Exhaustividad del Scraping:** Información crítica que resida en documentos PDF o portales protegidos por autenticación no forma parte del contexto actual.
3. **Mitigación para Módulo 2:** La transición a una arquitectura RAG formal con segmentación vectorial (`RecursiveCharacterTextSplitter`) y recuperación Top-K eliminará la restricción de ventana de contexto e incrementará la velocidad de respuesta.