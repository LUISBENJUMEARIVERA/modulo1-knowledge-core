import asyncio
import json
import os
import re
from datetime import UTC, datetime
from urllib.robotparser import RobotFileParser

from playwright.async_api import async_playwright
from rich.console import Console
from src.core.config import config
from src.ingestion.extractor import ResilientExtractor

console = Console()

# Conjunto estratégico de URLs factuales de Tecnoquímicas S.A.
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


def slugify(text: str) -> str:
    """Convierte un título o URL en un nombre seguro de archivo."""
    clean = re.sub(r"[^\w\-_]", "_", text.lower())
    return re.sub(r"_+", "_", clean).strip("_")[:50]


def check_robots_policy(url: str, user_agent: str = "*") -> bool:
    """Verifica si la URL está permitida por robots.txt de forma respetuosa."""
    try:
        import ssl
        import urllib.request
        from urllib.parse import urlparse

        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(
            robots_url,
            headers={"User-Agent": config.user_agent},
        )
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            content = resp.read().decode("utf-8", errors="ignore")

        rp = RobotFileParser()
        rp.parse(content.splitlines())
        can_fetch = rp.can_fetch(user_agent, url)
        return can_fetch if can_fetch is not None else True
    except Exception:
        # En caso de timeout, SSL corporativo o ausencia de robots.txt, permitir acceso de cortesía
        return True


async def build_curated_knowledge_base():
    """Ejecuta el pipeline de scraping en capas: Bronze -> Silver -> Gold."""
    os.makedirs(config.output_raw_dir, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs(config.output_gold_dir, exist_ok=True)

    extracted_sections: list[str] = []
    gold_records: list[dict] = []
    seen_hashes: set[str] = set()

    total_raw_bytes = 0
    total_clean_bytes = 0
    discarded_duplicates = 0

    console.print(
        "[bold cyan]Iniciando Pipeline de Scraping Medallion (Bronze -> Silver -> Gold)...[/bold cyan]\n"
    )
    console.print(f"[dim]User-Agent: {config.user_agent}[/dim]")
    console.print(
        f"[dim]Rate limit: {config.rate_limit_delay_ms}ms | Timeout: {config.request_timeout_ms}ms[/dim]\n"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=config.user_agent)
        page = await context.new_page()

        for section_title, url in CURATED_TQ_URLS:
            slug = slugify(f"{section_title}_{url}")
            console.print(f"[yellow]1. Descubrir:[/yellow] {section_title} -> {url}")

            # Etapa 1: Respetar directivas robots.txt
            is_allowed = check_robots_policy(url)
            if not is_allowed:
                console.print(f"  [red][!] Bloqueado por robots.txt: {url}[/red]")
                continue

            try:
                # Etapa 2: Extraer HTML crudo con Playwright (Capa Bronze)
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=config.request_timeout_ms,
                )
                await page.wait_for_timeout(config.rate_limit_delay_ms)

                html_content = await page.content()
                raw_size = len(html_content.encode("utf-8"))
                total_raw_bytes += raw_size

                # Guardar en Capa Bronze
                bronze_path = os.path.join(config.output_raw_dir, f"{slug}.html")
                with open(bronze_path, "w", encoding="utf-8") as f_bronze:
                    f_bronze.write(html_content)

                # Etapa 3: Limpiar y aislar contenido de alta densidad (Capa Silver)
                page_title = ResilientExtractor.extract_title(html_content, default=section_title)
                clean_text = ResilientExtractor.extract_clean_content(html_content, url)
                clean_size = len(clean_text.encode("utf-8"))
                total_clean_bytes += clean_size

                if not clean_text or len(clean_text) < 60:
                    console.print(f"  [yellow][!] Contenido reducido o vacio en: {url}[/yellow]")
                    continue

                # Etapa 4: Deduplicar mediante hash criptográfico SHA-256
                content_hash = ResilientExtractor.compute_sha256(clean_text)
                if content_hash in seen_hashes:
                    discarded_duplicates += 1
                    console.print(
                        f"  [yellow][!] Duplicado exacto descartado (Hash: {content_hash[:8]}...)[/yellow]"
                    )
                    continue
                seen_hashes.add(content_hash)

                # Guardar archivo individual Silver
                silver_path = os.path.join("data/processed", f"{slug}.txt")
                with open(silver_path, "w", encoding="utf-8") as f_silver:
                    f_silver.write(clean_text)

                doc_entry = f"=== SECCIÓN: {section_title} | FUENTE: {url} ===\n{clean_text}\n"
                extracted_sections.append(doc_entry)

                # Etapa 5: Enriquecer con metadatos estructurados (Capa Gold)
                crawled_timestamp = datetime.now(UTC).isoformat()
                token_count = ResilientExtractor.estimate_tokens(clean_text)

                gold_record = {
                    "url": url,
                    "title": page_title,
                    "section": section_title,
                    "crawled_at": crawled_timestamp,
                    "content_hash": content_hash,
                    "char_count": len(clean_text),
                    "token_count": token_count,
                    "content": clean_text,
                }
                gold_records.append(gold_record)

                console.print(
                    f"  [green][OK] Bronze -> Silver -> Gold completado[/green] "
                    f"({len(clean_text)} chars, ~{token_count} tokens, Hash: {content_hash[:8]}...)"
                )

            except Exception as e:
                console.print(f"  [red]✖ Error extrayendo {url}: {e}[/red]")

        await browser.close()

    # 1. Consolidar Base de Conocimiento Silver monolítica (para backward-compatibility con LLM)
    final_kb = "\n\n" + ("=" * 50 + "\n\n").join(extracted_sections)
    with open(config.output_processed_file, "w", encoding="utf-8") as f:
        f.write(final_kb)

    # 2. Consolidar Capa Gold (JSONL estructurado)
    with open(config.output_gold_jsonl, "w", encoding="utf-8") as f_gold:
        for record in gold_records:
            f_gold.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 3. Guardar métricas auditables para la UI de Streamlit y evaluación
    noise_discarded_bytes = max(0, total_raw_bytes - total_clean_bytes)
    total_tokens = sum(r["token_count"] for r in gold_records)
    total_chars = sum(r["char_count"] for r in gold_records)

    metrics_payload = {
        "stages": ["Descubrir", "Extraer", "Limpiar", "Deduplicar", "Enriquecer"],
        "total_urls_target": len(CURATED_TQ_URLS),
        "total_pages_scraped": len(gold_records),
        "total_tokens": total_tokens,
        "total_characters": total_chars,
        "total_raw_bytes": total_raw_bytes,
        "total_clean_bytes": total_clean_bytes,
        "noise_discarded_bytes": noise_discarded_bytes,
        "noise_reduction_ratio_pct": round(
            (noise_discarded_bytes / max(1, total_raw_bytes)) * 100, 1
        ),
        "discarded_duplicates": discarded_duplicates,
        "unique_documents": len(gold_records),
        "last_crawled_at": datetime.now(UTC).isoformat(),
        "storage_layers": {
            "bronze": config.output_raw_dir,
            "silver": config.output_processed_file,
            "gold": config.output_gold_jsonl,
        },
    }

    with open(config.output_gold_metrics, "w", encoding="utf-8") as f_metrics:
        json.dump(metrics_payload, f_metrics, indent=2, ensure_ascii=False)

    console.print(
        f"\n[bold green]Pipeline finalizado con éxito.[/bold green]\n"
        f"• Capa Bronze: {config.output_raw_dir}\n"
        f"• Capa Silver: {config.output_processed_file}\n"
        f"• Capa Gold: {config.output_gold_jsonl}\n"
        f"• Métricas: {config.output_gold_metrics} (Tokens: ~{total_tokens:,}, Descartes: {noise_discarded_bytes / 1024:.1f} KB)\n"
    )


if __name__ == "__main__":
    asyncio.run(build_curated_knowledge_base())
