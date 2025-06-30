from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
    role : str