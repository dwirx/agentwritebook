"""Reviewer agent untuk quality control dan feedback."""

from typing import Dict, List
from .base_agent import BaseAgent
from ..config.settings import model_config


class ReviewerAgent(BaseAgent):
    """Agent untuk mereview dan memberikan feedback pada konten."""

    def __init__(self):
        """Initialize reviewer agent dengan judge model."""
        super().__init__(
            model=model_config.judge_model,
            role="Content Reviewer",
            temperature=0.3  # Lebih objektif untuk review
        )

    def execute(
        self,
        content: str,
        chapter_info: Dict,
        book_context: Dict,
        criteria: List[str] = None
    ) -> Dict:
        """
        Review konten chapter.

        Args:
            content: Konten yang akan direview
            chapter_info: Info chapter
            book_context: Context buku
            criteria: Kriteria review (optional)

        Returns:
            Dictionary berisi score, feedback, dan suggestions
        """
        chapter_num = chapter_info.get('number', 1)
        chapter_title = chapter_info.get('title', 'Untitled')

        self.display_status(
            f"Mereview Chapter {chapter_num}: {chapter_title}",
            style="info"
        )

        # Default criteria jika tidak disediakan
        if criteria is None:
            book_type = book_context.get('genre', '').lower()
            if 'fiction' in book_type:
                criteria = [
                    "story_engagement",
                    "character_development",
                    "dialogue_quality",
                    "pacing",
                    "writing_style"
                ]
            else:
                criteria = [
                    "clarity",
                    "information_quality",
                    "structure",
                    "actionability",
                    "writing_style"
                ]

        review_result = self._perform_review(
            content, chapter_info, book_context, criteria
        )

        overall_score = review_result.get('overall_score', 0)
        status = "success" if overall_score >= 7 else "warning"

        self.display_status(
            f"Review selesai! Score: {overall_score}/10",
            style=status
        )

        return review_result

    def _perform_review(
        self,
        content: str,
        chapter_info: Dict,
        book_context: Dict,
        criteria: List[str]
    ) -> Dict:
        """Perform review berdasarkan criteria."""
        system_prompt = self.create_system_prompt(
            "Kamu adalah seorang editor dan kritikus profesional. "
            "Tugasmu adalah memberikan review yang konstruktif, objektif, dan actionable. "
            "Berikan score berdasarkan kriteria yang jelas dan feedback yang specific."
        )

        # Format criteria
        criteria_text = "\n".join([f"- {c.replace('_', ' ').title()}" for c in criteria])

        # Batasi content untuk review (ambil sample jika terlalu panjang)
        content_sample = content[:3000] + "..." if len(content) > 3000 else content

        user_prompt = f"""
Review chapter berikut dan berikan penilaian berdasarkan kriteria yang ditentukan.

INFORMASI BUKU:
Judul: {book_context.get('title', '')}
Genre: {book_context.get('genre', '')}

CHAPTER INFO:
Nomor: {chapter_info.get('number', '')}
Judul: {chapter_info.get('title', '')}

KONTEN:
{content_sample}

KRITERIA REVIEW:
{criteria_text}

INSTRUKSI:
Berikan review dalam format berikut:

## Overall Assessment
[Penilaian umum tentang chapter ini]

## Scores (1-10)
{chr(10).join([f'- {c.replace("_", " ").title()}: [score]/10' for c in criteria])}
- Overall Score: [score]/10

## Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

## Areas for Improvement
- [Area 1]: [Specific suggestion]
- [Area 2]: [Specific suggestion]

## Specific Feedback
[Feedback detail dan constructive criticism]

## Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]

Berikan penilaian yang objektif dan konstruktif!
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages, temperature=0.3)
        feedback_text = response['message']['content']

        # Parse scores dari feedback
        scores = self._parse_scores(feedback_text, criteria)

        return {
            "overall_score": scores.get('overall_score', 7.0),
            "criteria_scores": scores.get('criteria_scores', {}),
            "feedback": feedback_text,
            "needs_revision": scores.get('overall_score', 7.0) < 7.0
        }

    def _parse_scores(self, feedback_text: str, criteria: List[str]) -> Dict:
        """Parse scores dari feedback text."""
        scores = {
            "criteria_scores": {},
            "overall_score": 7.0
        }

        lines = feedback_text.split('\n')
        for line in lines:
            # Cari overall score
            if 'overall score' in line.lower():
                try:
                    # Ekstrak angka dari line
                    parts = line.split(':')
                    if len(parts) > 1:
                        score_part = parts[1].strip()
                        score_str = ''.join(c for c in score_part if c.isdigit() or c == '.')
                        if score_str:
                            score = float(score_str.split('/')[0])
                            scores['overall_score'] = min(10.0, max(1.0, score))
                except (ValueError, IndexError):
                    pass

            # Cari criteria scores
            for criterion in criteria:
                criterion_name = criterion.replace('_', ' ').lower()
                if criterion_name in line.lower():
                    try:
                        parts = line.split(':')
                        if len(parts) > 1:
                            score_part = parts[1].strip()
                            score_str = ''.join(c for c in score_part if c.isdigit() or c == '.')
                            if score_str:
                                score = float(score_str.split('/')[0])
                                scores['criteria_scores'][criterion] = min(10.0, max(1.0, score))
                    except (ValueError, IndexError):
                        pass

        return scores

    def quick_check(self, content: str, check_type: str = "grammar") -> Dict:
        """
        Quick check untuk aspek tertentu.

        Args:
            content: Konten yang akan dicek
            check_type: Tipe check (grammar, consistency, flow)

        Returns:
            Dictionary berisi hasil check
        """
        self.display_status(f"Melakukan {check_type} check...", style="info")

        prompts = {
            "grammar": "Check grammar, spelling, dan punctuation. List semua error yang ditemukan.",
            "consistency": "Check konsistensi nama, tempat, timeline, dan fakta. List semua inkonsistensi.",
            "flow": "Check flow dan coherence. Identifikasi bagian yang awkward atau tidak smooth."
        }

        system_prompt = self.create_system_prompt(
            f"Tugasmu adalah melakukan {check_type} check yang teliti."
        )

        # Batasi content
        content_sample = content[:2000] + "..." if len(content) > 2000 else content

        user_prompt = f"""
{prompts.get(check_type, prompts['grammar'])}

KONTEN:
{content_sample}

Format output:
## Issues Found
- [Issue 1]
- [Issue 2]

## Severity: [High/Medium/Low]

## Suggestions
- [Suggestion 1]
- [Suggestion 2]
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.chat(messages, temperature=0.2)

        return {
            "check_type": check_type,
            "result": response['message']['content'],
            "passed": "severity: low" in response['message']['content'].lower() or
                     "no issues" in response['message']['content'].lower()
        }
