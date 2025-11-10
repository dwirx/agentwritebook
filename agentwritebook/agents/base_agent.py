"""Base agent class untuk semua agent."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import sys
from ..utils.ollama_client import ollama_client
from ..config.settings import model_config
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

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
    ):
        """
        Chat dengan model.

        Args:
            messages: List of messages
            stream: Apakah streaming
            temperature: Override temperature

        Returns:
            Response dari model atau Generator jika streaming
        """
        temp = temperature if temperature is not None else self.temperature

        return self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
            temperature=temp
        )
    
    def chat_stream(
        self,
        messages: list[Dict[str, str]],
        temperature: Optional[float] = None,
        display_live: bool = True,
        show_progress: bool = True
    ) -> str:
        """
        Chat dengan streaming dan display real-time.

        Args:
            messages: List of messages
            temperature: Override temperature
            display_live: Apakah menampilkan output secara live
            show_progress: Show progress indicators

        Returns:
            Complete response text
        """
        temp = temperature if temperature is not None else self.temperature
        
        try:
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=temp
            )
            
            full_response = ""
            word_count = 0
            char_count = 0
            
            if display_live and show_progress:
                console.print(f"\n[bold cyan]🤖 {self.model}[/bold cyan] [dim]sedang menulis...[/dim]")
                console.print("[dim]" + "─" * 70 + "[/dim]\n")
            
            # Use sys.stdout for immediate output
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    full_response += content
                    char_count += len(content)
                    
                    if display_live:
                        # Print directly to stdout for immediate display
                        sys.stdout.write(content)
                        sys.stdout.flush()  # Force immediate output
            
            if display_live:
                # Count final words
                word_count = len(full_response.split())
                
                # New line and completion message
                sys.stdout.write('\n')
                sys.stdout.flush()
                
                if show_progress:
                    console.print(f"\n[dim]{'─' * 70}[/dim]")
                    console.print(f"[green]✓[/green] [bold]Selesai![/bold] "
                                f"[cyan]{word_count}[/cyan] kata "
                                f"[dim]({char_count} karakter)[/dim]")
                
            return full_response
            
        except Exception as e:
            console.print(f"\n[red]✗ Error saat streaming: {e}[/red]")
            # Fallback to non-streaming
            console.print("[yellow]⚠ Beralih ke mode non-streaming...[/yellow]")
            try:
                response = self.chat(messages, stream=False, temperature=temp)
                return response['message']['content']
            except Exception as e2:
                console.print(f"[red]✗ Error fallback: {e2}[/red]")
                return ""

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
