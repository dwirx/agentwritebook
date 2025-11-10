"""Main CLI interface untuk Book Writing Agent."""

import typer
from typing import Optional
from rich.console import Console
from rich import print as rprint

from .agents.orchestrator import orchestrator
from .config.settings import model_config

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
            auto_revise=auto_revise
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
def show_models():
    """
    Tampilkan model yang dikonfigurasi.
    """
    console.print("\n[bold]Model Configuration:[/bold]\n")
    console.print(f"Main Model (Planner): [cyan]{model_config.main_model}[/cyan]")
    console.print(f"Fast Model: [cyan]{model_config.fast_model}[/cyan]")
    console.print(f"Creative Model (Writer): [cyan]{model_config.creative_model}[/cyan]")
    console.print(f"Detail Model: [cyan]{model_config.detail_model}[/cyan]")
    console.print(f"Judge Model (Reviewer): [cyan]{model_config.judge_model}[/cyan]")
    console.print(f"Embedding Model: [cyan]{model_config.embedding_model}[/cyan]")


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

[bold]Model yang Digunakan:[/bold]
• Planner: Membuat struktur dan outline buku
• Writer: Menulis konten chapter yang engaging
• Reviewer: Quality control dan feedback

[bold]Commands:[/bold]
• create  - Buat buku lengkap
• outline - Buat outline saja
• models  - Lihat konfigurasi model
• info    - Tampilkan info ini

[bold]Contoh Penggunaan:[/bold]
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
