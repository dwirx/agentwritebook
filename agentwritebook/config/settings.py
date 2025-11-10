"""Konfigurasi untuk Ollama dan model yang digunakan."""

from pydantic import BaseModel
from typing import Literal


class OllamaConfig(BaseModel):
    """Konfigurasi untuk Ollama client."""

    base_url: str = "http://172.29.176.1:11434"
    timeout: int = 300  # 5 menit timeout


class ModelConfig(BaseModel):
    """Konfigurasi model yang tersedia."""

    # Model utama untuk berbagai tugas
    main_model: str = "gemma3:latest"
    fast_model: str = "gemma3:1b"
    creative_model: str = "qwen2.5:3b"
    detail_model: str = "qwen3:1.7b"
    judge_model: str = "kimi-k2:1t-cloud"
    embedding_model: str = "granite-embedding:latest"


class BookType(str):
    """Tipe buku yang bisa ditulis."""

    FICTION = "fiction"
    NON_FICTION = "non_fiction"


class AgentRole(str):
    """Role untuk setiap agent."""

    PLANNER = "planner"  # Membuat outline
    WRITER = "writer"    # Menulis konten
    REVIEWER = "reviewer"  # Review kualitas
    EDITOR = "editor"    # Edit dan polish


# Singleton instances
ollama_config = OllamaConfig()
model_config = ModelConfig()
