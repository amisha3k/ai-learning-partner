from pydantic import BaseModel
from typing import List, Dict

class ATSResponse(BaseModel):
    percentage_match: float
    overall_score: float
    missing_keywords: List[str] = []
    sections: Dict[str, Dict[str, str]] = {}
    grammar_issues: List[str] = []
    repetitive_words: List[str] = []
    improvement_scope: str = ""

