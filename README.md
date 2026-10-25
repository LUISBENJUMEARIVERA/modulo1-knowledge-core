# 💊 Tecnoquímicas AI — Núcleo de Conocimiento Semántico (Módulo 1)

Sistema de ingesta de datos resiliente, modelado semántico y arquitectura Q&A anclada (*grounded*) sobre **Tecnoquímicas S.A. (Grupo TQ)**, desarrollado para el **Módulo 1: Creación de la Base de Conocimiento Semántico y Sistema Q&A**.

---

## 🏛 Arquitectura de la Solución
* **Ingesta Dinámica:** Motor asíncrono con **Playwright** que resuelve la hidratación de JavaScript y Single Page Applications.
* **Extracción Agnóstica (Self-Healing):** Algoritmos de densidad textual con **Trafilatura** que aíslan el contenido central sin depender de selectores CSS o etiquetas frágiles del DOM.
* **Orquestación Declarativa:** Pipelines tipados con **LangChain LCEL** cubriendo las tres tareas requeridas:
  1. *Resumen Corporativo Ejecutivo.*
  2. *Preguntas Frecuentes (FAQ) Dinámicas.*
  3. *Asistente Q&A Grounded con Coerción Negativa Estricta.*
* **Inferencia Local:** Modelo open-source `llama3.2` vía **Ollama**, garantizando privacidad y latencias sub-segundo.
* **Interfaz de Demostración:** Micro-dashboard interactivo en **Streamlit** con soporte de streaming token a token.
* **Evaluación Sistemática:** Arnés de pruebas automatizado con una matriz de 20 casos (*In-Scope*, *Complex Semantic* y *Out-of-Scope Adversarial*).

---


## ⚡ Inicio Rápido (One-Liner / Copiar y Pegar)

Copia y pega el siguiente bloque en tu terminal para clonar, configurar todo automáticamente y abrir la app:

### En Windows (PowerShell / CMD):
```powershell
git clone [https://github.com/LUISBENJUMEARIVERA/modulo1-knowledge-core.git](https://github.com/LUISBENJUMEARIVERA/modulo1-knowledge-core.git) && cd modulo1-knowledge-core && .\run.bat
### en macOS y linux
git clone [https://github.com/LUISBENJUMEARIVERA/modulo1-knowledge-core.git](https://github.com/LUISBENJUMEARIVERA/modulo1-knowledge-core.git) && cd modulo1-knowledge-core && chmod +x run.sh && ./run.sh