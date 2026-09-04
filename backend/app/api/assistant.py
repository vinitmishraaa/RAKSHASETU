from fastapi import APIRouter
from app.schemas.schemas import AssistantQuery, AssistantAnswer
from app.ai_assistant.assistant import ask

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("", response_model=AssistantAnswer)
async def ask_assistant(query: AssistantQuery):
    result = await ask(query.question)
    return result
