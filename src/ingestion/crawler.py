import asyncio
import os
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from rich.console import Console
from src.core.config import config
from src.ingestion.extractor import ResilientExtractor

console = Console()

class AutonomousSpider:
    def __init__(self):
        self.visited = set()
        self.queue = asyncio.Queue()
        self.extracted_docs = []

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc.lower() not in config.allowed_domains:
            return False
        
        path = parsed.path.lower()
        if any(path.endswith(ext) for ext in config.ignored_extensions):
            return False
            
        forbidden_keywords = ["politica-de-cookies", "terminos-y-condiciones", "wp-content", "wp-json", "author"]
        if any(keyword in path for keyword in forbidden_keywords):
            return False

        return True

    def clean_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")

    async def crawl(self):
        os.makedirs(config.output_raw_dir, exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

        # Páginas prioritarias que garantizan cobertura factual de las 20 preguntas
        priority_urls = [
            "https://www.tqconfiable.com/contacto/preguntas-frecuentes/",
            "https://www.tqconfiable.com/contacto/",
            "https://www.tqconfiable.com",
            "https://www.tqconfiable.com/asi-cambiamos-al-mundo/mundo/gente/",
            "https://www.tqfarma.com/quienes-somos",
            "https://www.tqfarma.com/nuestras-marcas",
            "https://www.tqfarma.com/salud-humana",
            "https://www.tqfarma.com/consumo"
        ]

        # Encolar prioritarias con profundidad 0
        for url in priority_urls:
            await self.queue.put((self.clean_url(url), 0))

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            console.print("[bold yellow]Iniciando ingesta estructurada y descubrimiento guiado...[/bold yellow]\n")

            while not self.queue.empty() and len(self.visited) < config.max_pages:
                current_url, depth = await self.queue.get()

                if current_url in self.visited or depth > config.max_depth:
                    continue

                self.visited.add(current_url)
                console.print(f"[cyan][{len(self.visited)}/{config.max_pages}][Profundidad {depth}][/cyan] Extrayendo: {current_url}")

                try:
                    await page.goto(current_url, wait_until="domcontentloaded", timeout=25000)
                    await page.wait_for_timeout(1000)

                    html = await page.content()

                    clean_text = ResilientExtractor.extract_clean_content(html, current_url)
                    if clean_text and len(clean_text) > 80:
                        section_name = current_url.split("/")[-1].replace("-", " ").capitalize() or "Principal"
                        doc_chunk = f"=== FUENTE: {current_url} | SECCIÓN: {section_name} ===\n{clean_text}\n"
                        self.extracted_docs.append(doc_chunk)
                        console.print(f"  [green]✔ Extraídos {len(clean_text)} caracteres útiles[/green]")

                    # Descubrimiento de nuevos enlaces
                    if depth < config.max_depth:
                        soup = BeautifulSoup(html, "html.parser")
                        for a_tag in soup.find_all("a", href=True):
                            absolute_url = urljoin(current_url, a_tag["href"])
                            cleaned = self.clean_url(absolute_url)
                            if self.is_valid_url(cleaned) and cleaned not in self.visited:
                                await self.queue.put((cleaned, depth + 1))

                except Exception as e:
                    console.print(f"  [red]✖ Error en {current_url}: {e}[/red]")

            await browser.close()

        # Guardar la base de conocimiento consolidada
        final_kb = "\n\n" + ("="*50 + "\n\n").join(self.extracted_docs)
        with open(config.output_processed_file, "w", encoding="utf-8") as f:
            f.write(final_kb)

        console.print(f"\n[bold green]Ingesta completada: {len(self.extracted_docs)} documentos consolidados en {config.output_processed_file}[/bold green]")

if __name__ == "__main__":
    spider = AutonomousSpider()
    asyncio.run(spider.crawl())