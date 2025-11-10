"""Orchestrator untuk mengoordinasikan semua agents."""

from typing import Dict, Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel

from .planner_agent import PlannerAgent
from .writer_agent import WriterAgent
from .reviewer_agent import ReviewerAgent
from ..utils.file_manager import file_manager

console = Console()


class BookOrchestrator:
    """Orchestrator untuk proses penulisan buku."""

    def __init__(self):
        """Initialize orchestrator dengan semua agents."""
        self.planner = PlannerAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()
        self.file_manager = file_manager

    def create_book(
        self,
        topic: str,
        book_type: str,
        num_chapters: int = 10,
        target_audience: str = "general",
        additional_info: str = "",
        min_words_per_chapter: int = 1500,
        enable_review: bool = True,
        auto_revise: bool = False
    ) -> Dict:
        """
        Buat buku lengkap dari awal hingga akhir.

        Args:
            topic: Topik atau judul buku
            book_type: Tipe buku (fiction/non_fiction)
            num_chapters: Jumlah chapter
            target_audience: Target pembaca
            additional_info: Informasi tambahan
            min_words_per_chapter: Minimum kata per chapter
            enable_review: Enable review untuk setiap chapter
            auto_revise: Auto revisi jika score rendah

        Returns:
            Dictionary berisi informasi buku dan path
        """
        console.print(Panel(
            f"[bold cyan]Memulai proses penulisan buku[/bold cyan]\n"
            f"Topik: {topic}\n"
            f"Tipe: {book_type}\n"
            f"Chapters: {num_chapters}",
            title="Book Generation",
            border_style="cyan"
        ))

        # Step 1: Buat outline
        console.print("\n[bold]Step 1: Membuat Outline[/bold]")
        outline = self.planner.execute(
            topic=topic,
            book_type=book_type,
            num_chapters=num_chapters,
            target_audience=target_audience,
            additional_info=additional_info
        )

        # Buat direktori untuk buku
        book_title = outline.get('title', topic)
        book_dir = self.file_manager.create_book_directory(book_title)

        # Simpan outline
        outline_path = self.file_manager.save_outline(book_dir, outline)
        console.print(f"[green]✓[/green] Outline disimpan: {outline_path}")

        # Step 2: Tulis semua chapter
        console.print("\n[bold]Step 2: Menulis Chapters[/bold]")
        chapters = outline.get('chapters', [])

        chapter_results = []
        failed_chapters = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task(
                "[cyan]Menulis chapters...",
                total=len(chapters)
            )

            for chapter_info in chapters:
                chapter_num = chapter_info.get('number', 0)
                chapter_title = chapter_info.get('title', 'Untitled')

                try:
                    # Tulis chapter
                    chapter_result = self.writer.execute(
                        chapter_info=chapter_info,
                        book_context=outline,
                        min_words=min_words_per_chapter
                    )

                    # Review jika diaktifkan
                    if enable_review:
                        review_result = self.reviewer.execute(
                            content=chapter_result['content'],
                            chapter_info=chapter_info,
                            book_context=outline
                        )

                        chapter_result['review'] = review_result

                        # Auto revise jika score rendah dan diaktifkan
                        if auto_revise and review_result.get('needs_revision', False):
                            console.print(
                                f"[yellow]Chapter {chapter_num} perlu revisi, menulis ulang...[/yellow]"
                            )
                            # Tulis ulang dengan feedback
                            chapter_result = self._revise_chapter(
                                chapter_info,
                                outline,
                                review_result,
                                min_words_per_chapter
                            )

                    # Simpan chapter
                    chapter_path = self.file_manager.save_chapter(
                        book_dir=book_dir,
                        chapter_number=chapter_num,
                        chapter_title=chapter_title,
                        content=chapter_result['content'],
                        metadata={
                            'word_count': chapter_result.get('word_count', 0),
                            'review_score': chapter_result.get('review', {}).get('overall_score', 'N/A')
                        }
                    )

                    chapter_results.append({
                        'number': chapter_num,
                        'title': chapter_title,
                        'path': chapter_path,
                        'word_count': chapter_result.get('word_count', 0),
                        'score': chapter_result.get('review', {}).get('overall_score', None)
                    })

                    console.print(f"[green]✓[/green] Chapter {chapter_num} selesai")

                except Exception as e:
                    console.print(f"[red]✗[/red] Error pada Chapter {chapter_num}: {e}")
                    failed_chapters.append({
                        'number': chapter_num,
                        'title': chapter_title,
                        'error': str(e)
                    })

                progress.update(task, advance=1)

        # Step 3: Gabungkan menjadi buku lengkap
        console.print("\n[bold]Step 3: Menyusun Buku Lengkap[/bold]")
        full_book_path = self.file_manager.save_full_book(book_dir, book_title)
        console.print(f"[green]✓[/green] Buku lengkap disimpan: {full_book_path}")

        # Simpan metadata
        total_words = sum(r['word_count'] for r in chapter_results)
        avg_score = sum(r['score'] for r in chapter_results if r['score']) / len(chapter_results) if chapter_results else 0

        metadata = {
            'title': book_title,
            'type': book_type,
            'total_chapters': len(chapters),
            'completed_chapters': len(chapter_results),
            'failed_chapters': len(failed_chapters),
            'total_words': total_words,
            'average_review_score': round(avg_score, 2),
            'target_audience': target_audience
        }

        metadata_path = self.file_manager.save_metadata(book_dir, metadata)

        # Summary
        console.print(Panel(
            f"[bold green]Buku Selesai![/bold green]\n\n"
            f"Judul: {book_title}\n"
            f"Chapters: {len(chapter_results)}/{len(chapters)}\n"
            f"Total Words: {total_words:,}\n"
            f"Average Score: {avg_score:.1f}/10\n\n"
            f"Lokasi: {book_dir}",
            title="Summary",
            border_style="green"
        ))

        if failed_chapters:
            console.print("\n[yellow]Chapters yang gagal:[/yellow]")
            for fc in failed_chapters:
                console.print(f"  - Chapter {fc['number']}: {fc['title']} ({fc['error']})")

        return {
            'success': True,
            'book_title': book_title,
            'book_dir': str(book_dir),
            'full_book_path': str(full_book_path),
            'chapter_results': chapter_results,
            'failed_chapters': failed_chapters,
            'metadata': metadata
        }

    def _revise_chapter(
        self,
        chapter_info: Dict,
        book_context: Dict,
        review_result: Dict,
        min_words: int
    ) -> Dict:
        """Revisi chapter berdasarkan feedback review."""
        # Untuk saat ini, tulis ulang dengan temperature yang berbeda
        # Di versi yang lebih advanced, bisa include feedback dalam prompt
        revised_writer = WriterAgent()
        revised_writer.temperature = 0.9  # Lebih kreatif untuk revisi

        return revised_writer.execute(
            chapter_info=chapter_info,
            book_context=book_context,
            min_words=min_words
        )

    def create_outline_only(
        self,
        topic: str,
        book_type: str,
        num_chapters: int = 10,
        target_audience: str = "general",
        additional_info: str = ""
    ) -> Dict:
        """
        Buat outline saja tanpa menulis chapter.

        Args:
            topic: Topik buku
            book_type: Tipe buku
            num_chapters: Jumlah chapter
            target_audience: Target audience
            additional_info: Info tambahan

        Returns:
            Dictionary berisi outline dan path
        """
        console.print("[bold cyan]Membuat outline buku...[/bold cyan]")

        outline = self.planner.execute(
            topic=topic,
            book_type=book_type,
            num_chapters=num_chapters,
            target_audience=target_audience,
            additional_info=additional_info
        )

        book_title = outline.get('title', topic)
        book_dir = self.file_manager.create_book_directory(book_title)
        outline_path = self.file_manager.save_outline(book_dir, outline)

        console.print(f"[green]✓[/green] Outline disimpan: {outline_path}")

        return {
            'success': True,
            'outline': outline,
            'outline_path': str(outline_path),
            'book_dir': str(book_dir)
        }

    def write_single_chapter(
        self,
        chapter_info: Dict,
        book_context: Dict,
        output_path: Optional[Path] = None,
        min_words: int = 1500,
        enable_review: bool = True
    ) -> Dict:
        """
        Tulis satu chapter saja.

        Args:
            chapter_info: Info chapter
            book_context: Context buku
            output_path: Path output (optional)
            min_words: Minimum words
            enable_review: Enable review

        Returns:
            Dictionary berisi chapter result
        """
        chapter_num = chapter_info.get('number', 1)
        chapter_title = chapter_info.get('title', 'Untitled')

        console.print(f"[bold cyan]Menulis Chapter {chapter_num}: {chapter_title}[/bold cyan]")

        # Tulis chapter
        result = self.writer.execute(
            chapter_info=chapter_info,
            book_context=book_context,
            min_words=min_words
        )

        # Review jika diaktifkan
        if enable_review:
            review = self.reviewer.execute(
                content=result['content'],
                chapter_info=chapter_info,
                book_context=book_context
            )
            result['review'] = review

        # Simpan jika ada output path
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            console.print(f"[green]✓[/green] Chapter disimpan: {output_path}")

        return result


# Singleton instance
orchestrator = BookOrchestrator()
