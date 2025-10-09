from pydantic import BaseModel
from typing import List

# class MockResponse(BaseModel):
#     questions: List[str]

from pydantic import BaseModel

# Request model when user starts interview
class StartRequest(BaseModel):
    role: str

# Request model for chat messages
class ChatRequest(BaseModel):
    session_id: str
    message: str

# Response model for sending replies
class ChatResponse(BaseModel):
    session_id: str
    response: str
    end: bool = False  # whether the interview ended
