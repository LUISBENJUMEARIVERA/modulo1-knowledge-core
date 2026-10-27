import json
import os
import sys
import time
from pathlib import Path

# Resolver la ruta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from rich.console import Console
from rich.table import Table
from src.chains.tasks import service

console = Console()


def run_benchmark():
    json_path = os.path.join(ROOT_DIR, "data", "evaluation", "test_questions.json")
    results_md_path = os.path.join(ROOT_DIR, "data", "evaluation", "benchmark_results.md")

    if not os.path.exists(json_path):
        console.print(f"[red]No se encontró el archivo: {json_path}[/red]")
        return

    with open(json_path, encoding="utf-8") as f:
        questions = json.load(f)

    console.print(
        f"[bold cyan]Iniciando Benchmark de {len(questions)} Preguntas con Ollama...[/bold cyan]\n"
    )

    results = []
    table = Table(title="Resultados del Benchmark — Tecnoquímicas AI (Módulo 1)")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Categoría", width=16)
    table.add_column("Pregunta", width=35)
    table.add_column("Latencia (s)", justify="right", width=12)
    table.add_column("Estado", width=16)

    # Patrones y marcadores semánticos de rechazo estricto
    refusal_markers = [
        "no_contiene_datos",
        "no contiene datos",
        "no contiene información",
        "no se encuentra",
        "no está disponible",
        "no dispongo",
        "no se menciona",
        "no especifica",
        "no incluye información",
        "lo siento",
        "no tengo acceso",
        "no es posible determinar",
        "no se proporciona",
    ]

    for item in questions:
        q_id = item["id"]
        cat = item["category"]
        q_text = item["question"]

        start_time = time.time()
        # Consumir el stream completo de la cadena LCEL
        response_chunks = list(service.answer_question_stream(q_text))
        latency = round(time.time() - start_time, 2)
        full_answer = "".join(response_chunks).strip()

        # Evaluación semántica de guardrail anti-alucinación
        answer_lower = full_answer.lower()
        is_refusal = any(marker in answer_lower for marker in refusal_markers)

        if cat == "out_of_scope":
            status = "[green]Rechazo Correcto[/green]" if is_refusal else "[red]Alucinación[/red]"
        else:
            status = "[green]Respondida[/green]" if not is_refusal else "[yellow]Sin Datos[/yellow]"

        table.add_row(str(q_id), cat, q_text[:32] + "...", f"{latency}s", status)
        results.append(
            {
                "id": q_id,
                "category": cat,
                "question": q_text,
                "answer": full_answer,
                "latency_seconds": latency,
                "refusal_triggered": is_refusal,
            }
        )

    console.print(table)

    # Exportar resultados estructurados en Markdown para el informe técnico
    with open(results_md_path, "w", encoding="utf-8") as f:
        f.write("# Matriz de Evaluación Factual y Anti-Alucinación (20 Casos)\n\n")
        f.write(
            "| ID | Categoría | Pregunta | Respuesta del Sistema | Latencia | ¿Activó Rechazo? |\n"
        )
        f.write("|:---|:---|:---|:---|:---:|:---:|\n")
        for r in results:
            clean_ans = r["answer"].replace("\n", " ")
            f.write(
                f"| {r['id']} | {r['category']} | {r['question']} | {clean_ans} | {r['latency_seconds']}s | {r['refusal_triggered']} |\n"
            )

    console.print(f"\n[bold green]Reporte exportado exitosamente a: {results_md_path}[/bold green]")


if __name__ == "__main__":
    run_benchmark()
