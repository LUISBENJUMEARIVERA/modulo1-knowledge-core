import asyncio
import os

from playwright.async_api import async_playwright
from rich.console import Console
from src.core.config import config
from src.ingestion.extractor import ResilientExtractor

console = Console()

# Conjunto seleccionado de URLs con la mayor densidad de respuestas factuales de TQ
CURATED_TQ_URLS = [
    ("Atención y FAQs", "https://www.tqconfiable.com/contacto/preguntas-frecuentes/"),
    ("Canales y Sedes", "https://www.tqconfiable.com/contacto/"),
    ("Portal Principal", "https://www.tqconfiable.com"),
    ("Gente y Talento", "https://www.tqconfiable.com/asi-cambiamos-al-mundo/mundo/gente/"),
    (
        "Comunidad y Sostenibilidad",
        "https://www.tqconfiable.com/asi-cambiamos-al-mundo/mundo/comunidad/",
    ),
    ("División Farma e Historia", "https://www.tqfarma.com/quienes-somos"),
    ("Marcas y Portafolio", "https://www.tqfarma.com/nuestras-marcas"),
    ("Salud Humana y Productos", "https://www.tqfarma.com/salud-humana"),
]


async def build_curated_knowledge_base():
    os.makedirs(config.output_raw_dir, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    extracted_sections = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        console.print(
            "[bold cyan]Extrayendo núcleos de información estratégicos de Tecnoquímicas...[/bold cyan]\n"
        )

        for section_title, url in CURATED_TQ_URLS:
            console.print(f"[yellow]Extrayendo:[/yellow] {section_title} -> {url}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                await page.wait_for_timeout(1200)

                html = await page.content()
                clean_text = ResilientExtractor.extract_clean_content(html, url)

                if clean_text and len(clean_text) > 60:
                    doc = f"=== SECCIÓN: {section_title} | FUENTE: {url} ===\n{clean_text}\n"
                    extracted_sections.append(doc)
                    console.print(f"  [green]✔ Extraídos {len(clean_text)} caracteres[/green]")
                else:
                    console.print(f"  [yellow]⚠ Contenido reducido en: {url}[/yellow]")
            except Exception as e:
                console.print(f"  [red]✖ Error extrayendo {url}: {e}[/red]")

        await browser.close()

    # Consolidar base de conocimiento
    final_kb = "\n\n" + ("=" * 50 + "\n\n").join(extracted_sections)
    with open(config.output_processed_file, "w", encoding="utf-8") as f:
        f.write(final_kb)

    console.print(
        f"\n[bold green]Base de conocimiento consolidada con {len(extracted_sections)} fuentes en: {config.output_processed_file}[/bold green]"
    )


if __name__ == "__main__":
    asyncio.run(build_curated_knowledge_base())
