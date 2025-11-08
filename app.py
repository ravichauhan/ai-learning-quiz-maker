from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import QuizRequest, QuizResponse
from quiz_service import QuizService

app = FastAPI(title="AI Learning Quiz Maker", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

service: Optional[QuizService] = None


def get_service() -> QuizService:
    global service
    if service is None:
        try:
            service = QuizService()
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
    return service


@app.post("/quiz", response_model=QuizResponse)
async def create_quiz(payload: QuizRequest) -> QuizResponse:
    payload.educational_text = payload.educational_text.strip()
    if len(payload.educational_text) < 30:
        raise HTTPException(status_code=400, detail="Educational text is too short")

    difficulty = payload.difficulty.lower()
    if difficulty not in {"easy", "medium", "hard"}:
        raise HTTPException(status_code=400, detail="Difficulty must be easy, medium, or hard")

    topic = payload.topic.strip() if payload.topic else None

    service_instance = get_service()
    return service_instance.generate_quiz(
        text=payload.educational_text,
        difficulty=difficulty,
        topic=topic,
    )


@app.get("/")
async def root():
    return {
        "message": "POST /quiz with {educational_text, difficulty?, topic?}",
        "example": "Create 3 quiz questions from this educational text.",
    }
