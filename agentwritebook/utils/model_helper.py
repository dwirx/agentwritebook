"""Helper untuk model selection dan management."""

from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from ..utils.ollama_client import ollama_client

console = Console()


class ModelHelper:
    """Helper class untuk model operations."""
    
    RECOMMENDED_MODELS = {
        "planner": [
            {"name": "gemma3:latest", "size": "~9GB", "speed": "Medium", "quality": "High"},
            {"name": "llama3.2:latest", "size": "~4GB", "speed": "Fast", "quality": "Medium"},
            {"name": "qwen2.5:7b", "size": "~4.7GB", "speed": "Medium", "quality": "High"},
            {"name": "gpt-oss:20b-cloud", "size": "~12GB", "speed": "Medium", "quality": "Very High"},
            {"name": "glm-4.6:cloud", "size": "~3GB", "speed": "Fast", "quality": "High"},
        ],
        "writer": [
            {"name": "qwen2.5:3b", "size": "~2GB", "speed": "Very Fast", "quality": "Good"},
            {"name": "gemma3:latest", "size": "~9GB", "speed": "Medium", "quality": "High"},
            {"name": "llama3.2:3b", "size": "~2GB", "speed": "Fast", "quality": "Good"},
            {"name": "gpt-oss:20b-cloud", "size": "~12GB", "speed": "Medium", "quality": "Very High"},
            {"name": "gpt-oss:120b-cloud", "size": "~75GB", "speed": "Slow", "quality": "Exceptional"},
            {"name": "deepseek-v3.1:671b-cloud", "size": "~400GB", "speed": "Very Slow", "quality": "Exceptional"},
        ],
        "reviewer": [
            {"name": "kimi-k2:1t-cloud", "size": "~700MB", "speed": "Very Fast", "quality": "Good"},
            {"name": "qwen2.5:3b", "size": "~2GB", "speed": "Very Fast", "quality": "Good"},
            {"name": "gemma3:latest", "size": "~9GB", "speed": "Medium", "quality": "High"},
            {"name": "glm-4.6:cloud", "size": "~3GB", "speed": "Fast", "quality": "High"},
            {"name": "gpt-oss:20b-cloud", "size": "~12GB", "speed": "Medium", "quality": "Very High"},
        ]
    }
    
    # Custom models yang ditambahkan user
    CUSTOM_MODELS = {
        "planner": [],
        "writer": [],
        "reviewer": []
    }
    
    def __init__(self):
        """Initialize model helper."""
        self.client = ollama_client
    
    def get_available_models(self) -> List[str]:
        """
        Dapatkan list model yang tersedia di Ollama.
        
        Returns:
            List model names
        """
        try:
            return self.client.list_models()
        except Exception as e:
            console.print(f"[yellow]Warning: Gagal mendapatkan list model: {e}[/yellow]")
            return []
    
    def check_model_availability(self, model_name: str) -> bool:
        """
        Cek apakah model tersedia.
        
        Args:
            model_name: Nama model
            
        Returns:
            True jika tersedia
        """
        available = self.get_available_models()
        return model_name in available
    
    def show_recommended_models(self, role: str = None):
        """
        Tampilkan rekomendasi model.
        
        Args:
            role: Role agent (planner/writer/reviewer), None untuk semua
        """
        if role and role in self.RECOMMENDED_MODELS:
            self._display_role_models(role)
        else:
            # Tampilkan semua
            for role_name in ["planner", "writer", "reviewer"]:
                console.print(f"\n[bold cyan]{role_name.upper()}[/bold cyan]")
                self._display_role_models(role_name)
    
    def _display_role_models(self, role: str):
        """Display models untuk specific role."""
        models = self.RECOMMENDED_MODELS.get(role, [])
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Model", style="green")
        table.add_column("Size")
        table.add_column("Speed")
        table.add_column("Quality")
        table.add_column("Available", style="dim")
        
        available_models = self.get_available_models()
        
        for model in models:
            is_available = model['name'] in available_models
            status = "✓" if is_available else "✗"
            
            table.add_row(
                model['name'],
                model['size'],
                model['speed'],
                model['quality'],
                status
            )
        
        console.print(table)
    
    def validate_models(self, models: Dict[str, str]) -> Dict[str, bool]:
        """
        Validasi ketersediaan models.
        
        Args:
            models: Dict of role -> model_name
            
        Returns:
            Dict of role -> is_available
        """
        results = {}
        for role, model_name in models.items():
            results[role] = self.check_model_availability(model_name)
        
        return results
    
    def suggest_alternative(self, model_name: str, role: str) -> Optional[str]:
        """
        Suggest alternative model jika model tidak tersedia.
        
        Args:
            model_name: Model yang tidak tersedia
            role: Role agent
            
        Returns:
            Alternative model name atau None
        """
        available_models = self.get_available_models()
        recommended = self.RECOMMENDED_MODELS.get(role, [])
        
        # Cari model yang tersedia dari rekomendasi
        for model in recommended:
            if model['name'] in available_models and model['name'] != model_name:
                return model['name']
        
        # Jika tidak ada dari rekomendasi, ambil model pertama yang tersedia
        if available_models:
            return available_models[0]
        
        return None
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """
        Dapatkan informasi tentang model.
        
        Args:
            model_name: Nama model
            
        Returns:
            Dict berisi info model atau None
        """
        # Cari di rekomendasi
        for role, models in self.RECOMMENDED_MODELS.items():
            for model in models:
                if model['name'] == model_name:
                    return {
                        **model,
                        'role': role,
                        'available': self.check_model_availability(model_name)
                    }
        
        # Jika tidak di rekomendasi, cek availability saja
        if self.check_model_availability(model_name):
            return {
                'name': model_name,
                'available': True,
                'role': 'unknown',
                'size': 'Unknown',
                'speed': 'Unknown',
                'quality': 'Unknown'
            }
        
        return None
    
    def list_all_models_with_info(self):
        """Tampilkan semua model yang tersedia dengan info."""
        available = self.get_available_models()
        
        if not available:
            console.print("[yellow]Tidak ada model yang tersedia.[/yellow]")
            console.print("[dim]Jalankan 'ollama pull <model-name>' untuk download model.[/dim]")
            return
        
        console.print(f"\n[bold]Model yang Tersedia ({len(available)}):[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Model Name", style="green")
        table.add_column("Recommended For", style="dim")
        
        for idx, model_name in enumerate(available, 1):
            # Cari role yang merekomendasikan model ini
            roles = []
            for role, models in self.RECOMMENDED_MODELS.items():
                if any(m['name'] == model_name for m in models):
                    roles.append(role.capitalize())
            
            role_str = ", ".join(roles) if roles else "-"
            table.add_row(str(idx), model_name, role_str)
        
        console.print(table)
    
    def add_custom_model(
        self, 
        model_name: str, 
        role: str, 
        size: str = "Unknown",
        speed: str = "Unknown",
        quality: str = "Unknown"
    ) -> bool:
        """
        Tambahkan custom model ke rekomendasi.
        
        Args:
            model_name: Nama model
            role: Role agent (planner/writer/reviewer)
            size: Size model
            speed: Kecepatan (Very Fast/Fast/Medium/Slow/Very Slow)
            quality: Kualitas (Good/High/Very High/Exceptional)
            
        Returns:
            True jika berhasil
        """
        if role not in ["planner", "writer", "reviewer"]:
            console.print(f"[red]Error: Role harus 'planner', 'writer', atau 'reviewer'[/red]")
            return False
        
        # Check apakah sudah ada
        existing = self.RECOMMENDED_MODELS[role]
        if any(m['name'] == model_name for m in existing):
            console.print(f"[yellow]Model {model_name} sudah ada di {role}[/yellow]")
            return False
        
        # Tambahkan ke recommended models
        new_model = {
            "name": model_name,
            "size": size,
            "speed": speed,
            "quality": quality
        }
        
        self.RECOMMENDED_MODELS[role].append(new_model)
        self.CUSTOM_MODELS[role].append(new_model)
        
        console.print(f"[green]✓[/green] Model {model_name} ditambahkan ke {role}")
        return True
    
    def get_all_models_for_role(self, role: str) -> List[Dict]:
        """
        Dapatkan semua model untuk role tertentu.
        
        Args:
            role: Role agent
            
        Returns:
            List of model dicts
        """
        return self.RECOMMENDED_MODELS.get(role, [])
    
    def select_model_interactive(self, role: str) -> Optional[str]:
        """
        Pilih model secara interaktif dengan prompt.
        
        Args:
            role: Role agent
            
        Returns:
            Model name atau None
        """
        from rich.prompt import Prompt, IntPrompt
        
        models = self.get_all_models_for_role(role)
        available = self.get_available_models()
        
        console.print(f"\n[bold cyan]Pilih Model untuk {role.upper()}:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Model", style="green")
        table.add_column("Size")
        table.add_column("Speed")
        table.add_column("Quality")
        table.add_column("Status", style="dim")
        
        for idx, model in enumerate(models, 1):
            is_available = model['name'] in available
            status = "✓ Ready" if is_available else "✗ Not installed"
            status_style = "green" if is_available else "yellow"
            
            table.add_row(
                str(idx),
                model['name'],
                model['size'],
                model['speed'],
                model['quality'],
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        console.print(table)
        
        choice = IntPrompt.ask(
            "\nPilih nomor model (atau 0 untuk skip)",
            default=1
        )
        
        if choice == 0:
            return None
        
        if 1 <= choice <= len(models):
            selected = models[choice - 1]
            
            # Check availability
            if selected['name'] not in available:
                console.print(f"\n[yellow]Warning: Model {selected['name']} belum terinstall[/yellow]")
                console.print(f"[dim]Jalankan: ollama pull {selected['name']}[/dim]")
                
                confirm = Prompt.ask("Tetap gunakan model ini?", choices=["y", "n"], default="n")
                if confirm == "n":
                    return None
            
            console.print(f"[green]✓[/green] Dipilih: {selected['name']}")
            return selected['name']
        
        return None


# Singleton instance
model_helper = ModelHelper()

