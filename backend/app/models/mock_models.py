from pydantic import BaseModel
from typing import List

class MockResponse(BaseModel):
    questions: List[str]
