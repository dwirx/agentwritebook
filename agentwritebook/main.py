"""Main CLI interface untuk Book Writing Agent."""

import typer
from typing import Optional
from rich.console import Console
from rich import print as rprint

from .agents.orchestrator import orchestrator
from .config.settings import model_config
from .utils.interactive_wizard import interactive_wizard
from .utils.model_helper import model_helper

app = typer.Typer(
    name="writebook",
    help="AI Agent untuk menulis buku fiksi dan non-fiksi menggunakan Ollama",
    add_completion=False
)

console = Console()


@app.command("create")
def create_book(
    topic: str = typer.Argument(..., help="Topik atau judul buku"),
    book_type: str = typer.Option(
        "fiction",
        "--type",
        "-t",
        help="Tipe buku: fiction atau non_fiction"
    ),
    chapters: int = typer.Option(
        10,
        "--chapters",
        "-c",
        help="Jumlah chapter yang diinginkan"
    ),
    audience: str = typer.Option(
        "general",
        "--audience",
        "-a",
        help="Target audience (general, young_adult, children, professional, dll)"
    ),
    min_words: int = typer.Option(
        1500,
        "--min-words",
        "-w",
        help="Minimum kata per chapter"
    ),
    enable_review: bool = typer.Option(
        True,
        "--review/--no-review",
        help="Enable review untuk setiap chapter"
    ),
    auto_revise: bool = typer.Option(
        False,
        "--auto-revise",
        help="Otomatis revisi chapter dengan score rendah"
    ),
    enable_streaming: bool = typer.Option(
        False,
        "--stream",
        help="Enable streaming output untuk melihat proses real-time"
    ),
    language: str = typer.Option(
        "indonesian",
        "--language",
        "--lang",
        "-l",
        help="Bahasa penulisan: indonesian atau english"
    ),
    additional_info: Optional[str] = typer.Option(
        None,
        "--info",
        "-i",
        help="Informasi tambahan tentang buku"
    )
):
    """
    Buat buku lengkap dari awal hingga akhir.

    Contoh:
        writebook create "Petualangan di Dunia Fantasi" --type fiction --chapters 12

        writebook create "Panduan Python untuk Pemula" --type non_fiction --chapters 15 --min-words 2000
    """
    # Validasi book type
    if book_type not in ["fiction", "non_fiction"]:
        console.print("[red]Error: book_type harus 'fiction' atau 'non_fiction'[/red]")
        raise typer.Exit(1)

    try:
        result = orchestrator.create_book(
            topic=topic,
            book_type=book_type,
            num_chapters=chapters,
            target_audience=audience,
            additional_info=additional_info or "",
            min_words_per_chapter=min_words,
            enable_review=enable_review,
            auto_revise=auto_revise,
            enable_streaming=enable_streaming,
            language=language
        )

        if result['success']:
            console.print("\n[bold green]Sukses![/bold green]")
            console.print(f"Buku tersimpan di: [cyan]{result['book_dir']}[/cyan]")
            console.print(f"File lengkap: [cyan]{result['full_book_path']}[/cyan]")
        else:
            console.print("[red]Gagal membuat buku.[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("outline")
def create_outline(
    topic: str = typer.Argument(..., help="Topik atau judul buku"),
    book_type: str = typer.Option(
        "fiction",
        "--type",
        "-t",
        help="Tipe buku: fiction atau non_fiction"
    ),
    chapters: int = typer.Option(
        10,
        "--chapters",
        "-c",
        help="Jumlah chapter yang diinginkan"
    ),
    audience: str = typer.Option(
        "general",
        "--audience",
        "-a",
        help="Target audience"
    ),
    additional_info: Optional[str] = typer.Option(
        None,
        "--info",
        "-i",
        help="Informasi tambahan"
    )
):
    """
    Buat outline buku saja tanpa menulis chapter.

    Contoh:
        writebook outline "Misteri di Kota Tua" --type fiction --chapters 15
    """
    if book_type not in ["fiction", "non_fiction"]:
        console.print("[red]Error: book_type harus 'fiction' atau 'non_fiction'[/red]")
        raise typer.Exit(1)

    try:
        result = orchestrator.create_outline_only(
            topic=topic,
            book_type=book_type,
            num_chapters=chapters,
            target_audience=audience,
            additional_info=additional_info or ""
        )

        if result['success']:
            console.print("\n[bold green]Outline berhasil dibuat![/bold green]")
            console.print(f"Tersimpan di: [cyan]{result['outline_path']}[/cyan]")
        else:
            console.print("[red]Gagal membuat outline.[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("models")
def show_models(
    show_available: bool = typer.Option(
        False,
        "--available",
        "-a",
        help="Tampilkan semua model yang tersedia di Ollama"
    ),
    show_recommended: bool = typer.Option(
        False,
        "--recommended",
        "-r",
        help="Tampilkan model yang direkomendasikan"
    )
):
    """
    Tampilkan informasi model.
    
    Tanpa flag: Tampilkan konfigurasi model saat ini
    --available: Tampilkan semua model yang tersedia
    --recommended: Tampilkan model yang direkomendasikan
    
    Contoh:
        writebook models
        writebook models --available
        writebook models --recommended
    """
    if show_available:
        model_helper.list_all_models_with_info()
        return
    
    if show_recommended:
        console.print("\n[bold cyan]Model yang Direkomendasikan:[/bold cyan]")
        model_helper.show_recommended_models()
        return
    
    # Default: tampilkan konfigurasi saat ini
    console.print("\n[bold]Model Configuration (Current):[/bold]\n")
    console.print(f"Main Model (Planner): [cyan]{model_config.main_model}[/cyan]")
    console.print(f"Fast Model: [cyan]{model_config.fast_model}[/cyan]")
    console.print(f"Creative Model (Writer): [cyan]{model_config.creative_model}[/cyan]")
    console.print(f"Detail Model: [cyan]{model_config.detail_model}[/cyan]")
    console.print(f"Judge Model (Reviewer): [cyan]{model_config.judge_model}[/cyan]")
    console.print(f"Embedding Model: [cyan]{model_config.embedding_model}[/cyan]")
    
    console.print("\n[dim]Tip: Gunakan --available untuk melihat model yang tersedia[/dim]")
    console.print("[dim]     Gunakan --recommended untuk melihat rekomendasi[/dim]")


@app.command("add-model")
def add_model(
    model_name: str = typer.Argument(..., help="Nama model Ollama"),
    role: str = typer.Option(
        ...,
        "--role",
        "-r",
        help="Role: planner, writer, atau reviewer"
    ),
    size: str = typer.Option(
        "Unknown",
        "--size",
        "-s",
        help="Ukuran model (contoh: ~12GB)"
    ),
    speed: str = typer.Option(
        "Unknown",
        "--speed",
        help="Kecepatan: Very Fast, Fast, Medium, Slow, Very Slow"
    ),
    quality: str = typer.Option(
        "Unknown",
        "--quality",
        "-q",
        help="Kualitas: Good, High, Very High, Exceptional"
    )
):
    """
    Tambahkan custom model ke daftar rekomendasi.
    
    Model yang ditambahkan akan muncul di interactive mode dan model selection.
    
    Contoh:
        writebook add-model gpt-oss:20b-cloud --role writer --size "~12GB" --speed Medium --quality "Very High"
        
        writebook add-model deepseek-v3.1:671b-cloud --role writer --size "~400GB" --speed "Very Slow" --quality Exceptional
    """
    try:
        success = model_helper.add_custom_model(
            model_name=model_name,
            role=role,
            size=size,
            speed=speed,
            quality=quality
        )
        
        if success:
            console.print("\n[green]Model berhasil ditambahkan![/green]")
            console.print(f"\nUntuk menggunakan model ini:")
            console.print(f"1. Pastikan model sudah di-pull: [cyan]ollama pull {model_name}[/cyan]")
            console.print(f"2. Pilih model di interactive mode atau gunakan --model di command line")
        else:
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("select-model")
def select_model_command(
    role: str = typer.Argument(..., help="Role: planner, writer, atau reviewer")
):
    """
    Pilih model untuk role tertentu secara interaktif.
    
    Menampilkan semua model yang direkomendasikan untuk role tersebut
    dengan info lengkap (size, speed, quality, status).
    
    Contoh:
        writebook select-model planner
        writebook select-model writer
        writebook select-model reviewer
    """
    try:
        if role not in ["planner", "writer", "reviewer"]:
            console.print("[red]Error: Role harus 'planner', 'writer', atau 'reviewer'[/red]")
            raise typer.Exit(1)
        
        selected = model_helper.select_model_interactive(role)
        
        if selected:
            console.print(f"\n[bold green]Model terpilih untuk {role}: {selected}[/bold green]")
            console.print("\n[dim]Catatan: Untuk menggunakan model ini, jalankan command create/interactive[/dim]")
        else:
            console.print("[yellow]Tidak ada model yang dipilih[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Dibatalkan[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("interactive")
def interactive_mode():
    """
    Mode interaktif untuk membuat buku dengan wizard step-by-step.
    
    Mode ini akan memandu Anda melalui proses pembuatan buku dengan:
    - Pemilihan genre/kategori dari template
    - Konfigurasi jumlah chapter dan kata
    - Pemilihan model custom (opsional)
    - Live streaming output untuk melihat proses real-time
    
    Contoh:
        writebook interactive
    """
    console.print("\n[bold cyan]Selamat datang di Interactive Mode![/bold cyan]\n")
    
    try:
        # Jalankan wizard
        config = interactive_wizard.run()
        
        if not config:
            console.print("[yellow]Proses dibatalkan.[/yellow]")
            return
        
        # Jalankan pembuatan buku dengan config dari wizard
        result = orchestrator.create_book(
            topic=config['topic'],
            book_type=config['book_type'],
            num_chapters=config['num_chapters'],
            target_audience=config['target_audience'],
            additional_info=config.get('additional_info', ''),
            min_words_per_chapter=config['min_words_per_chapter'],
            enable_review=config['enable_review'],
            auto_revise=config['auto_revise'],
            enable_streaming=config.get('enable_streaming', False),
            custom_models=config.get('models'),
            language=config.get('language', 'indonesian')
        )
        
        if result['success']:
            console.print("\n[bold green]✓ Buku berhasil dibuat![/bold green]")
            console.print(f"Lokasi: [cyan]{result['book_dir']}[/cyan]")
            console.print(f"File lengkap: [cyan]{result['full_book_path']}[/cyan]")
        else:
            console.print("[red]Gagal membuat buku.[/red]")
            raise typer.Exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Dibatalkan oleh user.[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("info")
def show_info():
    """
    Tampilkan informasi tentang aplikasi.
    """
    info_text = """
[bold cyan]Book Writing Agent[/bold cyan]

AI Agent untuk menulis buku fiksi dan non-fiksi menggunakan Ollama.

[bold]Fitur:[/bold]
• Membuat outline buku otomatis
• Menulis chapter dengan berbagai style
• Review dan quality control
• Support fiksi dan non-fiksi
• Output dalam format Markdown
• Mode interaktif dengan wizard
• Streaming output real-time

[bold]Model yang Digunakan:[/bold]
• Planner: Membuat struktur dan outline buku
• Writer: Menulis konten chapter yang engaging
• Reviewer: Quality control dan feedback

[bold]Commands:[/bold]
• interactive - Mode interaktif dengan wizard (RECOMMENDED)
• create      - Buat buku lengkap
• outline     - Buat outline saja
• models      - Lihat konfigurasi model
• info        - Tampilkan info ini

[bold]Contoh Penggunaan:[/bold]
  writebook interactive                                    (Mode interaktif - mudah!)
  writebook create "Judul Buku" --type fiction --chapters 12
  writebook outline "Judul Buku" --type non_fiction
    """
    rprint(info_text)


@app.callback()
def main():
    """
    Book Writing Agent - AI untuk menulis buku menggunakan Ollama.
    """
    pass


if __name__ == "__main__":
    app()
