from pydantic import BaseModel


class TecnoquimicasConfig(BaseModel):
    empresa: str = "Tecnoquímicas S.A. (Grupo TQ)"
    seed_urls: list[str] = ["https://www.tqconfiable.com", "https://www.tqfarma.com"]
    allowed_domains: set[str] = {
        "tqconfiable.com",
        "www.tqconfiable.com",
        "tqfarma.com",
        "www.tqfarma.com",
    }
    ignored_extensions: set[str] = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".mp4",
        ".mp3",
        ".zip",
        ".tar",
        ".gz",
        ".docx",
        ".xlsx",
        ".css",
        ".js",
    }
    max_pages: int = 25  # Límite óptimo para no saturar memoria en Módulo 1
    max_depth: int = 2
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 "
        "(compatible; TecnoquimicasBot/1.0; academic-eval)"
    )
    request_timeout_ms: int = 25000
    rate_limit_delay_ms: int = 1200

    # Capas de Almacenamiento (Medallion Architecture: Bronze -> Silver -> Gold)
    output_raw_dir: str = "data/raw"  # Bronze
    output_processed_file: str = "data/processed/knowledge_base.txt"  # Silver
    output_gold_dir: str = "data/gold"  # Gold
    output_gold_jsonl: str = "data/gold/corpus.jsonl"  # Gold
    output_gold_metrics: str = "data/gold/metrics.json"  # Gold Metrics

    llm_model: str = "llama3.2"


config = TecnoquimicasConfig()
