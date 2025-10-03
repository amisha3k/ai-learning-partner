from pydantic import BaseModel

class ATSResponse(BaseModel):
    match_score: float
