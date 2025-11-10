"""Writer agent untuk menulis konten chapter."""

from typing import Dict, Optional
from .base_agent import BaseAgent
from ..config.settings import model_config


class WriterAgent(BaseAgent):
    """Agent untuk menulis konten chapter."""

    def __init__(self, model: Optional[str] = None):
        """
        Initialize writer agent.

        Args:
            model: Model yang digunakan (default: creative_model)
        """
        super().__init__(
            model=model or model_config.creative_model,
            role="Content Writer",
            temperature=0.85  # Lebih kreatif untuk writing
        )

    def execute(
        self,
        chapter_info: Dict,
        book_context: Dict,
        writing_style: str = "engaging",
        min_words: int = 1500
    ) -> Dict:
        """
        Tulis konten chapter.

        Args:
            chapter_info: Informasi chapter dari outline
            book_context: Context buku (title, genre, synopsis, dll)
            writing_style: Style penulisan (engaging, formal, casual, dll)
            min_words: Minimum jumlah kata

        Returns:
            Dictionary berisi konten chapter dan metadata
        """
        chapter_num = chapter_info.get('number', 1)
        chapter_title = chapter_info.get('title', 'Untitled')

        self.display_status(
            f"Menulis Chapter {chapter_num}: {chapter_title}",
            style="info"
        )

        # Tentukan jenis buku
        book_type = book_context.get('genre', '').lower()
        is_fiction = 'fiction' in book_type or book_type == 'fiction'

        if is_fiction:
            content = self._write_fiction_chapter(
                chapter_info, book_context, writing_style, min_words
            )
        else:
            content = self._write_nonfiction_chapter(
                chapter_info, book_context, writing_style, min_words
            )

        # Hitung statistik
        word_count = len(content.split())
        char_count = len(content)

        self.display_status(
            f"Chapter {chapter_num} selesai! ({word_count} kata)",
            style="success"
        )

        return {
            "chapter_number": chapter_num,
            "chapter_title": chapter_title,
            "content": content,
            "word_count": word_count,
            "char_count": char_count
        }

    def _write_fiction_chapter(
        self,
        chapter_info: Dict,
        book_context: Dict,
        writing_style: str,
        min_words: int
    ) -> str:
        """Tulis chapter untuk buku fiksi."""
        system_prompt = self.create_system_prompt(
            f"Kamu adalah seorang novelis berbakat dengan {writing_style} writing style. "
            "Tugasmu adalah menulis chapter yang immersive dengan dialog yang natural, "
            "deskripsi yang vivid, dan pacing yang baik. "
            "Gunakan 'show, don't tell' dan buat pembaca terlibat secara emosional."
        )

        # Ambil informasi dari context
        title = book_context.get('title', '')
        synopsis = book_context.get('synopsis', '')
        characters = book_context.get('main_characters', [])
        setting = book_context.get('setting', '')

        chapter_num = chapter_info.get('number', 1)
        chapter_title = chapter_info.get('title', '')
        description = chapter_info.get('description', '')
        key_events = chapter_info.get('key_events', [])

        # Format karakter
        char_info = ""
        if characters:
            char_info = "\nKarakter Utama:\n"
            for char in characters[:3]:  # Ambil 3 karakter utama
                char_info += f"- {char.get('name', '')}: {char.get('description', '')}\n"

        user_prompt = f"""
Tulis Chapter {chapter_num} dari novel berikut:

INFORMASI BUKU:
Judul: {title}
Synopsis: {synopsis}
Setting: {setting}
{char_info}

CHAPTER INFO:
Judul Chapter: {chapter_title}
Deskripsi: {description}
Key Events: {', '.join(key_events) if key_events else 'Dikembangkan sesuai alur cerita'}

INSTRUKSI PENULISAN:
1. Tulis minimal {min_words} kata
2. Gunakan {writing_style} style
3. Buat dialog yang natural dan meaningful
4. Deskripsi yang vivid tapi tidak berlebihan
5. Maintain pacing yang baik
6. Tunjukkan emosi karakter melalui actions dan dialog
7. End dengan hook yang membuat pembaca ingin lanjut ke chapter berikutnya

Jangan menulis "Chapter X:" atau judul chapter di awal - langsung mulai cerita.
Tulis dalam bahasa Indonesia yang baik dan menarik.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages, temperature=0.85)
        content = response['message']['content']

        return content.strip()

    def _write_nonfiction_chapter(
        self,
        chapter_info: Dict,
        book_context: Dict,
        writing_style: str,
        min_words: int
    ) -> str:
        """Tulis chapter untuk buku non-fiksi."""
        system_prompt = self.create_system_prompt(
            f"Kamu adalah seorang penulis non-fiksi berpengalaman dengan {writing_style} writing style. "
            "Tugasmu adalah menulis konten yang informatif, jelas, terstruktur dengan baik, "
            "dan mudah dipahami. Gunakan contoh konkret dan actionable insights."
        )

        # Ambil informasi dari context
        title = book_context.get('title', '')
        synopsis = book_context.get('synopsis', '')
        category = book_context.get('category', '')

        chapter_num = chapter_info.get('number', 1)
        chapter_title = chapter_info.get('title', '')
        description = chapter_info.get('description', '')
        key_points = chapter_info.get('key_points', [])
        learning_objectives = chapter_info.get('learning_objectives', '')

        user_prompt = f"""
Tulis Chapter {chapter_num} dari buku non-fiksi berikut:

INFORMASI BUKU:
Judul: {title}
Kategori: {category}
Tentang: {synopsis}

CHAPTER INFO:
Judul Chapter: {chapter_title}
Deskripsi: {description}
Key Points: {', '.join(key_points) if key_points else 'Dikembangkan sesuai topik'}
Learning Objectives: {learning_objectives}

INSTRUKSI PENULISAN:
1. Tulis minimal {min_words} kata
2. Gunakan {writing_style} style
3. Struktur yang jelas dengan sub-headings jika perlu
4. Berikan contoh konkret dan real-world applications
5. Gunakan bullets atau numbered lists untuk clarity
6. Sertakan actionable takeaways
7. Mulai dengan opening yang menarik perhatian
8. Akhiri dengan summary atau call-to-action

Format:
- Gunakan markdown untuk formatting (##, ###, **, -, dll)
- Jangan menulis "Chapter X:" atau judul chapter di awal - langsung mulai konten
- Tulis dalam bahasa Indonesia yang profesional namun mudah dipahami

Tulis konten yang valuable dan implementable!
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages, temperature=0.8)
        content = response['message']['content']

        return content.strip()

    def expand_section(
        self,
        original_content: str,
        section_to_expand: str,
        additional_context: str = ""
    ) -> str:
        """
        Expand bagian tertentu dari chapter.

        Args:
            original_content: Konten chapter original
            section_to_expand: Bagian yang ingin di-expand
            additional_context: Context tambahan

        Returns:
            Expanded content
        """
        self.display_status("Memperluas section...", style="info")

        system_prompt = self.create_system_prompt(
            "Tugasmu adalah memperluas dan memperkaya bagian tertentu dari teks "
            "sambil menjaga konsistensi dengan keseluruhan konten."
        )

        user_prompt = f"""
KONTEN ORIGINAL:
{original_content[:500]}...

BAGIAN YANG PERLU DIPERLUAS:
{section_to_expand}

CONTEXT TAMBAHAN:
{additional_context}

Tulis versi yang lebih detail dan kaya dari bagian tersebut.
Jaga konsistensi tone dan style dengan konten original.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages)
        return response['message']['content'].strip()
