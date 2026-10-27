"""Pruebas unitarias para la configuración del proyecto."""

from src.core.config import TecnoquimicasConfig, config


def test_config_defaults():
    # Arrange & Act
    cfg = TecnoquimicasConfig()

    # Assert
    assert "Tecnoquímicas" in cfg.empresa
    assert len(cfg.seed_urls) >= 2
    assert "tqconfiable.com" in cfg.allowed_domains
    assert "tqfarma.com" in cfg.allowed_domains
    assert ".pdf" in cfg.ignored_extensions
    assert ".jpg" in cfg.ignored_extensions
    assert cfg.max_pages > 0
    assert cfg.max_depth >= 1
    assert cfg.llm_model == "llama3.2"


def test_global_config_instance():
    # Arrange & Act & Assert
    assert isinstance(config, TecnoquimicasConfig)
    assert config.output_processed_file == "data/processed/knowledge_base.txt"
