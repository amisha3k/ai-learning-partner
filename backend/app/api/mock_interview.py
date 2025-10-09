# from fastapi import APIRouter, UploadFile,Form
# from app.models.mock_models import MockResponse
# from app.services.mock_service import generate_questions, evaluate_answer
# import PyPDF2 as pdf

# router = APIRouter()

# #store user sessions temporarily 
# sessions={}

# @router.post("/start", response_model=MockResponse)
# async def start_mock(file: UploadFile, role: str = Form(...)):
#     """
#     Generate mock interview questions based on resume and role.
#     """
#     reader = pdf.PdfReader(file.file)
#     resume_text = ""
#     for page in reader.pages:
#         resume_text += page.extract_text() or ""
#     questions = generate_questions(role, resume_text)
#     session_id=str(len(sessions)+1)
#     sessions[session_id]={"questions": questions,"current":0,"score":0}

#     first_question=questions[0] if questions else "No question generated."
#     return {"session_id": session_id,"question":first_question}

#     # return MockResponse(questions=questions)

# @router.post("/next")
# async def next_question(session_id: str = Form(...), answer: str = Form(...)):
#     """
#     Evaluate user's answer and return next question or final result.
#     """
#     session = sessions.get(session_id)
#     if not session:
#         return {"error": "Invalid session ID."}

#     idx = session["current"]
#     questions = session["questions"]

#     # Evaluate current answer (you can define your own logic)
#     feedback, score = evaluate_answer(questions[idx], answer)
#     session["score"] += score
#     session["current"] += 1

#     if session["current"] < len(questions):
#         next_q = questions[session["current"]]
#         return {"feedback": feedback, "next_question": next_q}
#     else:
#         total = len(questions)
#         final_score = session["score"]
#         result = f"Interview complete! Final Score: {final_score}/{total}"
#         return {"feedback": feedback, "result": result}    

from fastapi import APIRouter
from app.models.mock_models import StartRequest, ChatRequest, ChatResponse
from app.services.mock_service import start_interview, process_message

router = APIRouter()

@router.post("/start", response_model=ChatResponse)
def start_mock_interview(request: StartRequest):
    session_id, first_question = start_interview(request.role)
    return ChatResponse(session_id=session_id, response=first_question)

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(request: ChatRequest):
    response, end = process_message(request.session_id, request.message)
    return ChatResponse(session_id=request.session_id, response=response, end=end)
