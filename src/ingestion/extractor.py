import hashlib
import re

import trafilatura
from bs4 import BeautifulSoup


class ResilientExtractor:
    """Extractor semántico basado en densidad de texto y heurística agnóstica al DOM."""

    @staticmethod
    def compute_sha256(content: str) -> str:
        """Calcula el hash criptográfico SHA-256 para trazabilidad y deduplicación."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimación conservadora de tokens para LLM (~1.3 tokens por palabra)."""
        words = len(re.findall(r"\w+", text))
        return int(words * 1.3)

    @staticmethod
    def extract_title(html_content: str, default: str = "Documento Corporativo") -> str:
        """Extrae el título principal de la página desde la etiqueta <title> o <h1>."""
        soup = BeautifulSoup(html_content, "html.parser")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            if title:
                return title
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
            if title:
                return title
        return default

    @staticmethod
    def extract_clean_content(html_content: str, url: str = "") -> str:
        """Extrae texto de alta densidad descartando headers, scripts, footers y banners."""
        if not html_content:
            return ""

        # Intento 1: Extractor principal de densidad textual (Trafilatura)
        downloaded = trafilatura.extract(
            html_content,
            include_links=False,
            include_images=False,
            include_tables=True,
            output_format="txt",
            favor_precision=True,
        )

        if downloaded and len(downloaded.strip()) > 150:
            return downloaded.strip()

        # Intento 2 (Fallback): Limpieza heurística de Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 30]
        return "\n\n".join(lines)
