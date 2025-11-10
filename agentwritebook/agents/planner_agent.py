"""Planner agent untuk membuat outline buku."""

import json
from typing import Dict, List
from .base_agent import BaseAgent
from ..config.settings import model_config


class PlannerAgent(BaseAgent):
    """Agent untuk membuat outline dan struktur buku."""

    def __init__(self):
        """Initialize planner agent dengan model yang sesuai."""
        super().__init__(
            model=model_config.main_model,
            role="Book Planner",
            temperature=0.8  # Lebih kreatif untuk planning
        )

    def execute(
        self,
        topic: str,
        book_type: str,
        num_chapters: int = 10,
        target_audience: str = "general",
        additional_info: str = ""
    ) -> Dict:
        """
        Buat outline buku.

        Args:
            topic: Topik atau judul buku
            book_type: Tipe buku (fiction/non_fiction)
            num_chapters: Jumlah chapter yang diinginkan
            target_audience: Target pembaca
            additional_info: Informasi tambahan

        Returns:
            Dictionary berisi outline lengkap
        """
        self.display_status(
            f"Membuat outline untuk buku tentang: {topic}",
            style="info"
        )

        # Buat prompt sesuai tipe buku
        if book_type == "fiction":
            outline = self._create_fiction_outline(
                topic, num_chapters, target_audience, additional_info
            )
        else:
            outline = self._create_nonfiction_outline(
                topic, num_chapters, target_audience, additional_info
            )

        self.display_status("Outline berhasil dibuat!", style="success")
        return outline

    def _create_fiction_outline(
        self,
        topic: str,
        num_chapters: int,
        target_audience: str,
        additional_info: str
    ) -> Dict:
        """Buat outline untuk buku fiksi."""
        system_prompt = self.create_system_prompt(
            "Kamu adalah seorang penulis fiksi berpengalaman. "
            "Tugasmu adalah membuat outline cerita yang menarik dengan "
            "plot yang solid, karakter yang kuat, dan pacing yang baik."
        )

        user_prompt = f"""
Buat outline lengkap untuk sebuah novel fiksi dengan detail berikut:

Topik/Tema: {topic}
Jumlah Chapter: {num_chapters}
Target Pembaca: {target_audience}
Informasi Tambahan: {additional_info}

Output harus dalam format JSON dengan struktur:
{{
    "title": "Judul Buku yang Menarik",
    "genre": "Genre cerita",
    "target_audience": "{target_audience}",
    "synopsis": "Synopsis cerita (2-3 paragraf)",
    "main_characters": [
        {{"name": "Nama", "role": "Role", "description": "Deskripsi karakter"}}
    ],
    "setting": "Setting utama cerita",
    "themes": ["tema1", "tema2"],
    "chapters": [
        {{
            "number": 1,
            "title": "Judul Chapter",
            "description": "Apa yang terjadi di chapter ini",
            "key_events": ["event1", "event2"],
            "character_development": "Perkembangan karakter"
        }}
    ]
}}

Pastikan outline memiliki:
1. Beginning yang engaging
2. Middle dengan conflict dan tension
3. Climax yang powerful
4. Resolution yang satisfying
5. Character arc yang jelas
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages)
        content = response['message']['content']

        # Parse JSON dari response
        try:
            # Cari JSON dalam response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                outline = json.loads(json_str)
            else:
                raise ValueError("JSON tidak ditemukan dalam response")
        except (json.JSONDecodeError, ValueError) as e:
            # Jika parsing gagal, buat struktur default
            self.display_status(
                f"Warning: Gagal parse JSON ({e}), membuat struktur default",
                style="warning"
            )
            outline = self._create_default_fiction_outline(
                topic, num_chapters, target_audience
            )

        return outline

    def _create_nonfiction_outline(
        self,
        topic: str,
        num_chapters: int,
        target_audience: str,
        additional_info: str
    ) -> Dict:
        """Buat outline untuk buku non-fiksi."""
        system_prompt = self.create_system_prompt(
            "Kamu adalah seorang penulis non-fiksi berpengalaman. "
            "Tugasmu adalah membuat outline buku yang terstruktur dengan baik, "
            "informatif, dan mudah dipahami."
        )

        user_prompt = f"""
Buat outline lengkap untuk sebuah buku non-fiksi dengan detail berikut:

Topik: {topic}
Jumlah Chapter: {num_chapters}
Target Pembaca: {target_audience}
Informasi Tambahan: {additional_info}

Output harus dalam format JSON dengan struktur:
{{
    "title": "Judul Buku yang Informatif",
    "genre": "non-fiction",
    "category": "Kategori buku (self-help, business, education, dll)",
    "target_audience": "{target_audience}",
    "synopsis": "Deskripsi buku dan apa yang akan dipelajari pembaca",
    "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"],
    "chapters": [
        {{
            "number": 1,
            "title": "Judul Chapter",
            "description": "Apa yang dibahas di chapter ini",
            "key_points": ["poin1", "poin2", "poin3"],
            "learning_objectives": "Apa yang akan dipelajari"
        }}
    ]
}}

Pastikan outline:
1. Terstruktur secara logis dari basic ke advanced
2. Setiap chapter membangun pengetahuan dari chapter sebelumnya
3. Ada contoh praktis atau case study
4. Ada actionable insights
5. Conclusion yang merangkum semua
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages)
        content = response['message']['content']

        # Parse JSON dari response
        try:
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                outline = json.loads(json_str)
            else:
                raise ValueError("JSON tidak ditemukan dalam response")
        except (json.JSONDecodeError, ValueError) as e:
            self.display_status(
                f"Warning: Gagal parse JSON ({e}), membuat struktur default",
                style="warning"
            )
            outline = self._create_default_nonfiction_outline(
                topic, num_chapters, target_audience
            )

        return outline

    def _create_default_fiction_outline(
        self,
        topic: str,
        num_chapters: int,
        target_audience: str
    ) -> Dict:
        """Buat default outline untuk fiksi jika parsing gagal."""
        chapters = []
        for i in range(1, num_chapters + 1):
            chapters.append({
                "number": i,
                "title": f"Chapter {i}",
                "description": f"Chapter {i} tentang {topic}",
                "key_events": [],
                "character_development": ""
            })

        return {
            "title": topic,
            "genre": "fiction",
            "target_audience": target_audience,
            "synopsis": f"Sebuah cerita tentang {topic}",
            "main_characters": [],
            "setting": "",
            "themes": [],
            "chapters": chapters
        }

    def _create_default_nonfiction_outline(
        self,
        topic: str,
        num_chapters: int,
        target_audience: str
    ) -> Dict:
        """Buat default outline untuk non-fiksi jika parsing gagal."""
        chapters = []
        for i in range(1, num_chapters + 1):
            chapters.append({
                "number": i,
                "title": f"Chapter {i}: {topic}",
                "description": f"Pembahasan tentang aspek {i} dari {topic}",
                "key_points": [],
                "learning_objectives": ""
            })

        return {
            "title": topic,
            "genre": "non-fiction",
            "category": "general",
            "target_audience": target_audience,
            "synopsis": f"Buku ini membahas tentang {topic}",
            "key_takeaways": [],
            "chapters": chapters
        }
