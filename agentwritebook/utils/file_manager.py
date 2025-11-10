"""File manager untuk menyimpan output buku dalam markdown."""

import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class FileManager:
    """Manager untuk menyimpan dan mengorganisir file output."""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize file manager.

        Args:
            output_dir: Directory untuk menyimpan output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def create_book_directory(self, book_title: str) -> Path:
        """
        Buat directory untuk buku baru.

        Args:
            book_title: Judul buku

        Returns:
            Path ke directory buku
        """
        # Sanitize title untuk nama folder
        safe_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')

        # Tambahkan timestamp untuk uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        book_dir = self.output_dir / f"{safe_title}_{timestamp}"
        book_dir.mkdir(exist_ok=True)

        return book_dir

    def save_outline(self, book_dir: Path, outline: Dict) -> Path:
        """
        Simpan outline buku.

        Args:
            book_dir: Directory buku
            outline: Dictionary berisi outline

        Returns:
            Path ke file outline
        """
        outline_path = book_dir / "00_outline.md"

        content = f"# Outline: {outline.get('title', 'Untitled')}\n\n"
        content += f"**Genre:** {outline.get('genre', 'N/A')}\n\n"
        content += f"**Target Audience:** {outline.get('target_audience', 'N/A')}\n\n"

        if 'synopsis' in outline:
            content += f"## Synopsis\n\n{outline['synopsis']}\n\n"

        if 'chapters' in outline:
            content += "## Chapters\n\n"
            for i, chapter in enumerate(outline['chapters'], 1):
                content += f"### Chapter {i}: {chapter.get('title', 'Untitled')}\n\n"
                content += f"{chapter.get('description', '')}\n\n"

        with open(outline_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return outline_path

    def save_chapter(
        self,
        book_dir: Path,
        chapter_number: int,
        chapter_title: str,
        content: str,
        metadata: Dict = None
    ) -> Path:
        """
        Simpan chapter buku.

        Args:
            book_dir: Directory buku
            chapter_number: Nomor chapter
            chapter_title: Judul chapter
            content: Konten chapter
            metadata: Metadata tambahan (word count, dll)

        Returns:
            Path ke file chapter
        """
        filename = f"{chapter_number:02d}_{chapter_title.replace(' ', '_')}.md"
        chapter_path = book_dir / filename

        markdown_content = f"# Chapter {chapter_number}: {chapter_title}\n\n"

        if metadata:
            markdown_content += "---\n"
            for key, value in metadata.items():
                markdown_content += f"**{key.replace('_', ' ').title()}:** {value}\n"
            markdown_content += "---\n\n"

        markdown_content += content

        with open(chapter_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return chapter_path

    def save_full_book(self, book_dir: Path, book_title: str) -> Path:
        """
        Gabungkan semua chapter menjadi satu file lengkap.

        Args:
            book_dir: Directory buku
            book_title: Judul buku

        Returns:
            Path ke file buku lengkap
        """
        full_book_path = book_dir / f"{book_title.replace(' ', '_')}_full.md"

        # Baca semua file chapter (yang dimulai dengan angka)
        chapters = sorted([f for f in book_dir.glob("[0-9]*.md")])

        with open(full_book_path, 'w', encoding='utf-8') as full_file:
            full_file.write(f"# {book_title}\n\n")
            full_file.write(f"_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
            full_file.write("---\n\n")

            for chapter_file in chapters:
                with open(chapter_file, 'r', encoding='utf-8') as cf:
                    content = cf.read()
                    full_file.write(content)
                    full_file.write("\n\n---\n\n")

        return full_book_path

    def save_metadata(self, book_dir: Path, metadata: Dict) -> Path:
        """
        Simpan metadata buku.

        Args:
            book_dir: Directory buku
            metadata: Dictionary metadata

        Returns:
            Path ke file metadata
        """
        metadata_path = book_dir / "metadata.md"

        content = "# Book Metadata\n\n"
        for key, value in metadata.items():
            content += f"**{key.replace('_', ' ').title()}:** {value}\n\n"

        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return metadata_path


# Singleton instance
file_manager = FileManager()
