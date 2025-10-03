from fastapi import FastAPI
from app.api import tutor,ats,mock_interview
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="AI LEARNING PARTNER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)## this allows any frontend(ex-react) to call the backend

app.include_router(tutor.router,prefix="/api/tutor",tags=["Tutor"])
app.include_router(ats.router,prefix="/api/ats",tags=["ATS Analyzer"])
app.include_router(mock_interview.router,prefix="/api/mock_interview",tags=["Mock Interview"])

@app.get("/")
def root():
    return {"message": "AI Learning Partner API is running"}