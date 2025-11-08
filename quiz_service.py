import json
import os
from typing import List, Optional

from fastapi import HTTPException
from openai import OpenAI

from models import QuizQuestion, QuizResponse
from prompts import build_prompt


class QuizService:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def generate_quiz(self, text: str, difficulty: str, topic: Optional[str]) -> QuizResponse:
        prompt = build_prompt(text=text, difficulty=difficulty, topic=topic)
        try:
            completion = self.client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                temperature=0.4,
            )
        except Exception as exc:  # pragma: no cover - external API call
            raise HTTPException(status_code=502, detail=str(exc)) from exc

        raw_output = completion.output[0].content[0].text.strip()
        try:
            parsed: List[dict] = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=502, detail=f"Invalid AI response: {exc}") from exc

        questions = [QuizQuestion(**item) for item in parsed]
        if len(questions) != 3:
            raise HTTPException(status_code=502, detail="AI did not return exactly 3 questions")

        return QuizResponse(difficulty=difficulty, topic=topic, questions=questions)
