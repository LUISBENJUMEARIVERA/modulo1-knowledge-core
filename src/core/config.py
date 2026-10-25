from pydantic import BaseModel
from typing import List, Set

class TecnoquimicasConfig(BaseModel):
    empresa: str = "Tecnoquímicas S.A. (Grupo TQ)"
    seed_urls: List[str] = [
        "https://www.tqconfiable.com",
        "https://www.tqfarma.com"
    ]
    allowed_domains: Set[str] = {
        "tqconfiable.com",
        "www.tqconfiable.com",
        "tqfarma.com",
        "www.tqfarma.com"
    }
    ignored_extensions: Set[str] = {
        ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".mp4",
        ".mp3", ".zip", ".tar", ".gz", ".docx", ".xlsx", ".css", ".js"
    }
    max_pages: int = 25  # Límite óptimo para no saturar memoria en Módulo 1
    max_depth: int = 2
    output_raw_dir: str = "data/raw"
    output_processed_file: str = "data/processed/knowledge_base.txt"
    llm_model: str = "llama3.2"

config = TecnoquimicasConfig()