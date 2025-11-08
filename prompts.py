from textwrap import dedent
from typing import Optional


def build_prompt(text: str, difficulty: str, topic: Optional[str]) -> str:
    topic_line = f"Topic focus: {topic}." if topic else ""
    template = f"""\
    Create 3 quiz questions from this educational text.

    Requirements:
    - Difficulty: {difficulty}.
    - Output must be JSON with this schema:
      [
        {{
          "question": "...",
          "options": ["A", "B", "C", "D"],
          "answer": "...",
          "explanation": "..."
        }},
        ... 3 total items ...
      ]
    - Each option should be concise and mutually exclusive.
    - Provide a one-sentence explanation referencing the source text.
    {topic_line}

    Educational text:
    {text}
    """
    return dedent(template)
