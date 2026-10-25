import trafilatura
from bs4 import BeautifulSoup

class ResilientExtractor:
    """Extractor semántico basado en densidad de texto y heurística agnóstica al DOM."""
    
    @staticmethod
    def extract_clean_content(html_content: str, url: str = "") -> str:
        # Intento 1: Extractor principal de densidad textual (elimina headers, footers y banners automáticamente)
        downloaded = trafilatura.extract(
            html_content,
            include_links=False,
            include_images=False,
            include_tables=True,
            output_format='txt',
            favor_precision=True
        )
        
        if downloaded and len(downloaded.strip()) > 150:
            return downloaded.strip()
        
        # Intento 2 (Fallback): Limpieza heurística de Beautiful Soup si el texto es muy corto o estructurado en tablas
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
            
        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 30]
        return "\n\n".join(lines)