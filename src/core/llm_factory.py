from langchain_ollama import ChatOllama
from src.core.config import config


def get_llm(temperature: float = 0.1) -> ChatOllama:
    """Instancia y retorna el modelo de Ollama con baja temperatura para evitar alucinaciones."""
    return ChatOllama(model=config.llm_model, temperature=temperature)
