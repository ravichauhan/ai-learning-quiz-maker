# AI Learning Quiz Maker

Turns any educational passage into three multiple-choice questions using the OpenAI API.

## Features
- `/quiz` endpoint validates difficulty (easy/medium/hard) and optional topic hints.
- Service layer (`quiz_service.py`) handles prompt construction, OpenAI calls, and JSON parsing.
- Each response returns three questions with four options, the correct answer, and a short explanation.
- CORS enabled by default so a simple frontend can call it directly.

## File Structure
```
ai-learning-quiz-maker/
├── app.py              # FastAPI entrypoint and routing
├── models.py           # Pydantic schemas for request/response payloads
├── prompts.py          # Centralized prompt template builder
├── quiz_service.py     # Encapsulates OpenAI call + validation
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Run Locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key
uvicorn app:app --reload
```

## Example Request
```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{
        "educational_text": "Photosynthesis is the process by which green plants use sunlight...",
        "difficulty": "easy",
        "topic": "biology"
      }'
```

### Example Response
```json
{
  "difficulty": "easy",
  "topic": "biology",
  "questions": [
    {
      "question": "What is the purpose of photosynthesis in plants?",
      "options": [
        "To absorb minerals from the soil",
        "To convert sunlight, water, and CO2 into glucose",
        "To transport sugars through the stem",
        "To attract pollinators"
      ],
      "answer": "To convert sunlight, water, and CO2 into glucose",
      "explanation": "Plants use photosynthesis to turn sunlight and raw materials into food energy."
    },
    "... two more questions ..."
  ]
}
```

## Future Improvements
- Streaming responses so clients can render questions as they arrive.
- Add citation support linking each question back to the original paragraph.
- Provide difficulty auto-detection based on reading level of the source text.
