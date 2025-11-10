"""Base agent class untuk semua agent."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..utils.ollama_client import ollama_client
from ..config.settings import model_config
from rich.console import Console
from rich.panel import Panel

console = Console()


class BaseAgent(ABC):
    """Base class untuk semua agent."""

    def __init__(self, model: str, role: str, temperature: float = 0.7):
        """
        Initialize base agent.

        Args:
            model: Nama model yang digunakan
            role: Role/tugas agent ini
            temperature: Temperature untuk generasi
        """
        self.model = model
        self.role = role
        self.temperature = temperature
        self.client = ollama_client

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Jalankan tugas agent.

        Args:
            **kwargs: Parameter yang dibutuhkan agent

        Returns:
            Hasil eksekusi agent
        """
        pass

    def chat(
        self,
        messages: list[Dict[str, str]],
        stream: bool = False,
        temperature: Optional[float] = None
    ) -> Dict:
        """
        Chat dengan model.

        Args:
            messages: List of messages
            stream: Apakah streaming
            temperature: Override temperature

        Returns:
            Response dari model
        """
        temp = temperature if temperature is not None else self.temperature

        return self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
            temperature=temp
        )

    def display_status(self, message: str, style: str = "info"):
        """
        Display status message dengan formatting.

        Args:
            message: Message to display
            style: Style (info, success, error, warning)
        """
        styles = {
            "info": "blue",
            "success": "green",
            "error": "red",
            "warning": "yellow"
        }
        color = styles.get(style, "blue")

        console.print(Panel(
            f"[{color}]{message}[/{color}]",
            title=f"[bold]{self.role.upper()}[/bold]",
            border_style=color
        ))

    def create_system_prompt(self, custom_instructions: str = "") -> str:
        """
        Buat system prompt untuk agent.

        Args:
            custom_instructions: Instruksi tambahan

        Returns:
            System prompt
        """
        base_prompt = f"Kamu adalah seorang {self.role} yang expert. "
        base_prompt += "Kamu harus menghasilkan output berkualitas tinggi. "
        base_prompt += custom_instructions

        return base_prompt
