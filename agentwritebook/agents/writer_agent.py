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
        min_words: int = 1500,
        enable_streaming: bool = False,
        language: str = "indonesian"
    ) -> Dict:
        """
        Tulis konten chapter.

        Args:
            chapter_info: Informasi chapter dari outline
            book_context: Context buku (title, genre, synopsis, dll)
            writing_style: Style penulisan (engaging, formal, casual, dll)
            min_words: Minimum jumlah kata
            enable_streaming: Enable streaming output

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
                chapter_info, book_context, writing_style, min_words, enable_streaming, language
            )
        else:
            content = self._write_nonfiction_chapter(
                chapter_info, book_context, writing_style, min_words, enable_streaming, language
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
        min_words: int,
        enable_streaming: bool = False,
        language: str = "indonesian"
    ) -> str:
        """Tulis chapter untuk buku fiksi."""
        
        # Language-specific system prompts
        if language.lower() in ["english", "en", "inggris"]:
            system_prompt = self.create_system_prompt(
                f"You are a talented novelist with an {writing_style} writing style. "
                "Your task is to write an immersive chapter with natural dialogue, "
                "vivid descriptions, and good pacing. "
                "Use 'show, don't tell' technique and engage readers emotionally. "
                "Write professionally with rich vocabulary and compelling narrative flow."
            )
            lang_instruction = "Write in fluent, professional English with rich vocabulary and engaging narrative."
        else:
            system_prompt = self.create_system_prompt(
                f"Kamu adalah seorang novelis berbakat dengan {writing_style} writing style. "
                "Tugasmu adalah menulis chapter yang immersive dengan dialog yang natural, "
                "deskripsi yang vivid, dan pacing yang baik. "
                "Gunakan 'show, don't tell' dan buat pembaca terlibat secara emosional. "
                "Tulis dengan profesional menggunakan kosakata yang kaya dan alur naratif yang menarik."
            )
            lang_instruction = "Tulis dalam bahasa Indonesia yang fasih dan profesional dengan kosakata kaya dan narasi yang engaging."

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

        if language.lower() in ["english", "en", "inggris"]:
            user_prompt = f"""
Write Chapter {chapter_num} of the following novel:

BOOK INFORMATION:
Title: {title}
Synopsis: {synopsis}
Setting: {setting}
{char_info}

CHAPTER INFO:
Chapter Title: {chapter_title}
Description: {description}
Key Events: {', '.join(key_events) if key_events else 'Develop according to story flow'}

WRITING INSTRUCTIONS:
1. Write minimum {min_words} words
2. Use {writing_style} style
3. Create natural and meaningful dialogue that reveals character
4. Use vivid, sensory descriptions (show, don't tell)
5. Maintain good pacing with balance between action, dialogue, and description
6. Show character emotions through actions, thoughts, and dialogue
7. Include internal character thoughts and motivations
8. Use varied sentence structures for rhythm
9. Build tension and conflict naturally
10. End with a compelling hook that makes readers want to continue
11. Use literary devices: metaphors, symbolism, foreshadowing where appropriate
12. Create immersive atmosphere with sensory details

QUALITY STANDARDS:
- Rich, varied vocabulary
- Smooth narrative flow
- Consistent character voice
- Clear scene transitions
- Emotional depth and nuance
- Professional literary quality

Don't write "Chapter X:" or chapter title at the beginning - start the story directly.
{lang_instruction}
"""
        else:
            user_prompt = f"""
Tulis Chapter {chapter_num} dari novel berikut:

INFORMASI BUKU:
Judul: {title}
Synopsis: {synopsis}
Setting: {setting}
{char_info}

INFO CHAPTER:
Judul Chapter: {chapter_title}
Deskripsi: {description}
Key Events: {', '.join(key_events) if key_events else 'Dikembangkan sesuai alur cerita'}

INSTRUKSI PENULISAN:
1. Tulis minimal {min_words} kata
2. Gunakan {writing_style} style
3. Buat dialog yang natural dan meaningful yang mengungkapkan karakter
4. Gunakan deskripsi yang vivid dan sensorik (show, don't tell)
5. Jaga pacing yang baik dengan keseimbangan action, dialog, dan deskripsi
6. Tunjukkan emosi karakter melalui actions, pikiran, dan dialog
7. Sertakan pikiran internal dan motivasi karakter
8. Gunakan variasi struktur kalimat untuk ritme yang baik
9. Bangun tension dan conflict secara natural
10. Akhiri dengan hook yang kuat agar pembaca ingin lanjut
11. Gunakan perangkat sastra: metafora, simbolisme, foreshadowing yang tepat
12. Ciptakan atmosfer immersive dengan detail sensorik

STANDAR KUALITAS:
- Kosakata kaya dan bervariasi
- Alur narasi yang smooth
- Konsistensi karakter
- Transisi scene yang jelas
- Kedalaman dan nuansa emosional
- Kualitas literari profesional

Jangan menulis "Chapter X:" atau judul chapter di awal - langsung mulai cerita.
{lang_instruction}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        if enable_streaming:
            content = self.chat_stream(messages, temperature=0.85, display_live=True)
        else:
            response = self.chat(messages, temperature=0.85)
            content = response['message']['content']

        return content.strip()

    def _write_nonfiction_chapter(
        self,
        chapter_info: Dict,
        book_context: Dict,
        writing_style: str,
        min_words: int,
        enable_streaming: bool = False,
        language: str = "indonesian"
    ) -> str:
        """Tulis chapter untuk buku non-fiksi."""
        
        # Language-specific system prompts
        if language.lower() in ["english", "en", "inggris"]:
            system_prompt = self.create_system_prompt(
                f"You are an experienced non-fiction writer with an {writing_style} writing style. "
                "Your task is to write informative, clear, well-structured content that's easy to understand. "
                "Use concrete examples, actionable insights, and evidence-based information. "
                "Write professionally with authority and credibility."
            )
            lang_instruction = "Write in clear, professional English with precise terminology and well-structured explanations."
        else:
            system_prompt = self.create_system_prompt(
                f"Kamu adalah seorang penulis non-fiksi berpengalaman dengan {writing_style} writing style. "
                "Tugasmu adalah menulis konten yang informatif, jelas, terstruktur dengan baik, "
                "dan mudah dipahami. Gunakan contoh konkret, actionable insights, dan informasi berbasis bukti. "
                "Tulis dengan profesional, kredibel, dan authoritative."
            )
            lang_instruction = "Tulis dalam bahasa Indonesia yang jelas dan profesional dengan terminologi tepat dan penjelasan terstruktur."

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

        if enable_streaming:
            content = self.chat_stream(messages, temperature=0.8, display_live=True)
        else:
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
