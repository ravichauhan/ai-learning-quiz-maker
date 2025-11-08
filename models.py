from typing import List, Optional

from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    educational_text: str = Field(
        ..., min_length=30, description="Content to convert into quiz questions"
    )
    difficulty: str = Field(
        "medium", description="easy, medium, or hard tone for the questions"
    )
    topic: Optional[str] = Field(None, description="Optional topic hint (e.g., biology, history)")


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    difficulty: str
    topic: Optional[str]
    questions: List[QuizQuestion]
