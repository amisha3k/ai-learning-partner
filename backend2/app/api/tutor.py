from fastapi import APIRouter
from app.models.tutor_models import TutorRequest, TutorResponse
from app.services.tutor_service import get_tutor_answer

router=APIRouter()

@router.post("/ask",response_model=TutorResponse)
def ask_tutor(request: TutorRequest):
    """
    Ask a question to AI Tutor.
    """
    answer=get_tutor_answer(request.question)
    return TutorResponse(answer=answer)

