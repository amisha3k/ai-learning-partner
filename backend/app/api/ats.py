from fastapi import APIRouter, UploadFile, Form
from app.models.ats_models import ATSResponse
from app.services.ats_service import analyze_resume
import PyPDF2 as pdf

router = APIRouter()

@router.post("/analyze", response_model=ATSResponse)
async def analyze(file: UploadFile, jd: str = Form(...)):
    """
    Analyze resume PDF against job description and return structured results.
    """
    try:
        reader = pdf.PdfReader(file.file)
        resume_text = "".join([page.extract_text() or "" for page in reader.pages])

        print("✅ Resume text (first 500 chars):", resume_text[:500])
        print("✅ Job description (first 500 chars):", jd[:500])

        result = analyze_resume(resume_text, jd)
        print("✅ ATS result:", result)

        return ATSResponse(
            percentage_match=result.get("percentage_match", 0.0),
            overall_score=result.get("overall_score", 0.0),
            missing_keywords=result.get("missing_keywords", []),
            sections=result.get("sections", {}),
            grammar_issues=result.get("grammar_issues", []),
            repetitive_words=result.get("repetitive_words", []),
            improvement_scope=result.get("improvement_scope", "")
        )

    except Exception as e:
        print("Error in ATS analyze:", e)
        return ATSResponse(
            percentage_match=0.0,
            overall_score=0.0,
            missing_keywords=[],
            sections={},
            grammar_issues=[],
            repetitive_words=[],
            improvement_scope="Error analyzing resume."
        )
