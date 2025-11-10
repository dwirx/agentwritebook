"""Wrapper untuk Ollama client dengan konfigurasi custom."""

from ollama import Client
from typing import Dict, List, Optional, Generator
from ..config.settings import ollama_config


class OllamaClient:
    """Custom Ollama client dengan konfigurasi."""

    def __init__(self):
        """Initialize Ollama client."""
        self.client = Client(host=ollama_config.base_url)

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict | Generator:
        """
        Chat dengan model.

        Args:
            model: Nama model yang digunakan
            messages: List of messages (role, content)
            stream: Apakah menggunakan streaming
            temperature: Temperature untuk generasi (0.0-1.0)
            **kwargs: Parameter tambahan untuk Ollama

        Returns:
            Response dari Ollama atau Generator jika streaming
        """
        options = {
            "temperature": temperature,
            **kwargs.get("options", {})
        }

        try:
            response = self.client.chat(
                model=model,
                messages=messages,
                stream=stream,
                options=options
            )
            return response
        except Exception as e:
            print(f"Error dalam chat: {e}")
            raise

    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict | Generator:
        """
        Generate text dari prompt.

        Args:
            model: Nama model yang digunakan
            prompt: Prompt untuk generate
            stream: Apakah menggunakan streaming
            temperature: Temperature untuk generasi (0.0-1.0)
            **kwargs: Parameter tambahan untuk Ollama

        Returns:
            Response dari Ollama atau Generator jika streaming
        """
        options = {
            "temperature": temperature,
            **kwargs.get("options", {})
        }

        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=stream,
                options=options
            )
            return response
        except Exception as e:
            print(f"Error dalam generate: {e}")
            raise

    def list_models(self) -> List[str]:
        """List semua model yang tersedia."""
        try:
            models = self.client.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []


# Singleton instance
ollama_client = OllamaClient()
