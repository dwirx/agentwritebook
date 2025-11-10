"""Interactive wizard untuk pemilihan konfigurasi buku."""

from typing import Dict, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


class InteractiveWizard:
    """Interactive wizard untuk setup pembuatan buku."""
    
    GENRE_TEMPLATES = {
        "fiction": {
            "fantasy": {
                "name": "Fantasy",
                "description": "Cerita dengan elemen magic, dunia fantasi, makhluk mistis",
                "examples": "Harry Potter, Lord of the Rings",
                "recommended_chapters": 15
            },
            "sci-fi": {
                "name": "Science Fiction",
                "description": "Cerita futuristik dengan teknologi canggih, eksplorasi luar angkasa",
                "examples": "Dune, Foundation",
                "recommended_chapters": 12
            },
            "mystery": {
                "name": "Mystery/Detective",
                "description": "Cerita misteri dengan investigasi dan plot twist",
                "examples": "Sherlock Holmes, Agatha Christie novels",
                "recommended_chapters": 10
            },
            "romance": {
                "name": "Romance",
                "description": "Cerita cinta dengan karakter development yang kuat",
                "examples": "Pride and Prejudice, The Notebook",
                "recommended_chapters": 12
            },
            "thriller": {
                "name": "Thriller/Suspense",
                "description": "Cerita penuh suspense dan ketegangan",
                "examples": "Gone Girl, The Girl with the Dragon Tattoo",
                "recommended_chapters": 14
            },
            "adventure": {
                "name": "Adventure",
                "description": "Petualangan seru dengan action dan eksplorasi",
                "examples": "Indiana Jones, Treasure Island",
                "recommended_chapters": 13
            }
        },
        "non_fiction": {
            "self-help": {
                "name": "Self-Help/Personal Development",
                "description": "Panduan pengembangan diri dan motivasi",
                "examples": "Atomic Habits, The 7 Habits",
                "recommended_chapters": 10
            },
            "business": {
                "name": "Business/Entrepreneurship",
                "description": "Strategi bisnis, manajemen, startup",
                "examples": "Good to Great, The Lean Startup",
                "recommended_chapters": 12
            },
            "technical": {
                "name": "Technical/Programming",
                "description": "Tutorial teknis, coding, teknologi",
                "examples": "Clean Code, Design Patterns",
                "recommended_chapters": 15
            },
            "education": {
                "name": "Educational/Tutorial",
                "description": "Materi pembelajaran dan panduan praktis",
                "examples": "Learning How to Learn",
                "recommended_chapters": 12
            },
            "health": {
                "name": "Health & Wellness",
                "description": "Kesehatan, fitness, nutrisi, mental health",
                "examples": "Why We Sleep, The Body Keeps the Score",
                "recommended_chapters": 10
            }
        }
    }
    
    def __init__(self):
        """Initialize wizard."""
        self.config = {}
    
    def run(self) -> Dict:
        """
        Jalankan interactive wizard.
        
        Returns:
            Dictionary berisi konfigurasi lengkap
        """
        console.print(Panel(
            "[bold cyan]Book Writing Agent - Interactive Mode[/bold cyan]\n\n"
            "Mari kita buat buku bersama! Saya akan menanyakan beberapa pertanyaan.",
            border_style="cyan"
        ))
        
        # Step 1: Pilih tipe buku
        self.config['book_type'] = self._choose_book_type()
        
        # Step 2: Pilih genre/kategori
        genre_info = self._choose_genre(self.config['book_type'])
        self.config['genre'] = genre_info['key']
        self.config['genre_info'] = genre_info
        
        # Step 3: Judul dan topik
        self._get_book_details()
        
        # Step 4: Konfigurasi chapter
        self._configure_chapters(genre_info['recommended_chapters'])
        
        # Step 5: Target audience
        self._choose_audience()
        
        # Step 6: Pilih models
        self._choose_models()
        
        # Step 7: Review & writing options
        self._configure_options()
        
        # Step 8: Konfirmasi
        self._show_summary()
        
        if Confirm.ask("\n[bold]Mulai menulis buku?[/bold]", default=True):
            console.print("\n[green]Memulai proses penulisan...[/green]\n")
            return self.config
        else:
            console.print("[yellow]Dibatalkan oleh user[/yellow]")
            return None
    
    def _choose_book_type(self) -> str:
        """Pilih tipe buku."""
        console.print("\n[bold]1. Pilih Tipe Buku[/bold]")
        console.print("  [cyan]1[/cyan]. Fiction (Fiksi)")
        console.print("  [cyan]2[/cyan]. Non-Fiction (Non-Fiksi)")
        
        choice = Prompt.ask(
            "Pilihan",
            choices=["1", "2"],
            default="1"
        )
        
        return "fiction" if choice == "1" else "non_fiction"
    
    def _choose_genre(self, book_type: str) -> Dict:
        """Pilih genre/kategori."""
        console.print(f"\n[bold]2. Pilih Genre/Kategori[/bold]")
        
        genres = self.GENRE_TEMPLATES[book_type]
        
        # Tampilkan dalam tabel
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Genre", style="green")
        table.add_column("Deskripsi")
        table.add_column("Contoh")
        
        genre_list = list(genres.items())
        for idx, (key, info) in enumerate(genre_list, 1):
            table.add_row(
                str(idx),
                info['name'],
                info['description'],
                info['examples']
            )
        
        console.print(table)
        
        choice_idx = IntPrompt.ask(
            "Pilih nomor genre",
            default=1
        )
        
        if 1 <= choice_idx <= len(genre_list):
            key, info = genre_list[choice_idx - 1]
            console.print(f"[green]✓[/green] Dipilih: {info['name']}")
            return {
                'key': key,
                'name': info['name'],
                'recommended_chapters': info['recommended_chapters']
            }
        else:
            console.print("[yellow]Pilihan tidak valid, menggunakan default[/yellow]")
            key, info = genre_list[0]
            return {
                'key': key,
                'name': info['name'],
                'recommended_chapters': info['recommended_chapters']
            }
    
    def _get_book_details(self):
        """Dapatkan detail buku."""
        console.print("\n[bold]3. Detail Buku[/bold]")
        
        self.config['topic'] = Prompt.ask(
            "[cyan]Judul atau topik buku[/cyan]",
            default="Petualangan Seru"
        )
        
        self.config['additional_info'] = Prompt.ask(
            "[cyan]Informasi tambahan (opsional)[/cyan]\nContoh: Setting, karakter, tone, dll",
            default=""
        )
    
    def _configure_chapters(self, recommended: int):
        """Konfigurasi jumlah chapter."""
        console.print(f"\n[bold]4. Konfigurasi Chapters[/bold]")
        console.print(f"[dim]Rekomendasi untuk genre ini: {recommended} chapters[/dim]")
        
        self.config['num_chapters'] = IntPrompt.ask(
            "Jumlah chapter",
            default=recommended
        )
        
        self.config['min_words_per_chapter'] = IntPrompt.ask(
            "Minimum kata per chapter",
            default=1500
        )
    
    def _choose_audience(self):
        """Pilih target audience."""
        console.print("\n[bold]5. Target Audience[/bold]")
        console.print("  1. General (Umum)")
        console.print("  2. Young Adult (Remaja)")
        console.print("  3. Children (Anak-anak)")
        console.print("  4. Professional (Profesional)")
        console.print("  5. Academic (Akademik)")
        console.print("  6. Custom")
        
        choice = Prompt.ask("Pilihan", choices=["1", "2", "3", "4", "5", "6"], default="1")
        
        audiences = {
            "1": "general",
            "2": "young_adult",
            "3": "children",
            "4": "professional",
            "5": "academic"
        }
        
        if choice == "6":
            self.config['target_audience'] = Prompt.ask("Masukkan target audience")
        else:
            self.config['target_audience'] = audiences[choice]
    
    def _choose_models(self):
        """Pilih models untuk setiap agent."""
        from ..utils.model_helper import model_helper
        
        console.print("\n[bold]6. Pilih Models[/bold]")
        
        console.print("  1. Gunakan model default (recommended)")
        console.print("  2. Pilih model dari rekomendasi (dengan info lengkap)")
        console.print("  3. Input manual model name")
        
        choice = Prompt.ask("Pilihan", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            # Default models
            self.config['models'] = {
                'planner': 'gemma3:latest',
                'writer': 'qwen2.5:3b',
                'reviewer': 'kimi-k2:1t-cloud'
            }
            console.print("[green]✓[/green] Menggunakan model default")
            
        elif choice == "2":
            # Interactive selection dengan info lengkap
            self.config['models'] = {}
            
            console.print("\n[cyan]Pilih model untuk setiap role:[/cyan]")
            
            # Planner
            planner_model = model_helper.select_model_interactive("planner")
            self.config['models']['planner'] = planner_model or 'gemma3:latest'
            
            # Writer
            writer_model = model_helper.select_model_interactive("writer")
            self.config['models']['writer'] = writer_model or 'qwen2.5:3b'
            
            # Reviewer
            reviewer_model = model_helper.select_model_interactive("reviewer")
            self.config['models']['reviewer'] = reviewer_model or 'kimi-k2:1t-cloud'
            
            console.print("\n[green]✓[/green] Model dipilih")
            
        else:
            # Manual input
            console.print("\n[dim]Masukkan nama model (atau tekan Enter untuk default)[/dim]")
            
            self.config['models'] = {
                'planner': Prompt.ask("Model untuk Planner", default="gemma3:latest"),
                'writer': Prompt.ask("Model untuk Writer", default="qwen2.5:3b"),
                'reviewer': Prompt.ask("Model untuk Reviewer", default="kimi-k2:1t-cloud")
            }
    
    def _configure_options(self):
        """Konfigurasi opsi review dan revision."""
        console.print("\n[bold]7. Opsi Penulisan[/bold]")
        
        # Pilihan bahasa
        console.print("\n[cyan]Pilih bahasa penulisan:[/cyan]")
        console.print("  1. Bahasa Indonesia")
        console.print("  2. English")
        
        lang_choice = Prompt.ask("Pilihan", choices=["1", "2"], default="1")
        self.config['language'] = "indonesian" if lang_choice == "1" else "english"
        
        lang_name = "Bahasa Indonesia" if lang_choice == "1" else "English"
        console.print(f"[green]✓[/green] Bahasa: {lang_name}")
        
        self.config['enable_review'] = Confirm.ask(
            "\nEnable review untuk setiap chapter?",
            default=True
        )
        
        if self.config['enable_review']:
            self.config['auto_revise'] = Confirm.ask(
                "Auto-revise chapter dengan score rendah?",
                default=False
            )
        else:
            self.config['auto_revise'] = False
        
        self.config['enable_streaming'] = Confirm.ask(
            "Enable streaming output (tampilkan proses real-time)?",
            default=True
        )
    
    def _show_summary(self):
        """Tampilkan ringkasan konfigurasi."""
        console.print("\n[bold cyan]Ringkasan Konfigurasi:[/bold cyan]")
        
        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Tipe Buku", self.config['book_type'])
        table.add_row("Genre", self.config['genre_info']['name'])
        table.add_row("Judul", self.config['topic'])
        table.add_row("Jumlah Chapter", str(self.config['num_chapters']))
        table.add_row("Min Words/Chapter", str(self.config['min_words_per_chapter']))
        table.add_row("Target Audience", self.config['target_audience'])
        table.add_row("Bahasa", "Indonesia" if self.config.get('language', 'indonesian') == 'indonesian' else "English")
        table.add_row("Review Enabled", "Ya" if self.config['enable_review'] else "Tidak")
        table.add_row("Auto Revise", "Ya" if self.config['auto_revise'] else "Tidak")
        table.add_row("Streaming", "Ya" if self.config['enable_streaming'] else "Tidak")
        
        console.print(table)


# Singleton instance
interactive_wizard = InteractiveWizard()

