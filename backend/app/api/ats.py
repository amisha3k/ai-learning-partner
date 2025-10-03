from fastapi import APIRouter, UploadFile, Form
from app.models.ats_models import ATSResponse
from app.services.ats_service import analyze_resume
import PyPDF2 as pdf

router = APIRouter()

@router.post("/analyze", response_model=ATSResponse)
async def analyze(file: UploadFile, jd: str = Form(...)):
    """
    Analyze resume PDF against job description.
    """
    reader = pdf.PdfReader(file.file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""
    score = analyze_resume(resume_text, jd)
    return ATSResponse(match_score=score)
