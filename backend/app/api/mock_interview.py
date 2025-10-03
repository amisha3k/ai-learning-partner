from fastapi import APIRouter, UploadFile
from app.models.mock_models import MockResponse
from app.services.mock_service import generate_questions
import PyPDF2 as pdf

router = APIRouter()

@router.post("/start", response_model=MockResponse)
async def start_mock(file: UploadFile, role: str):
    """
    Generate mock interview questions based on resume and role.
    """
    reader = pdf.PdfReader(file.file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""
    questions = generate_questions(role, resume_text)
    return MockResponse(questions=questions)
