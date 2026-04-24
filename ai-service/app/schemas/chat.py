from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.provider import ProviderCard


class ChatRequest(BaseModel):
    user_input: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str

    providers: List[ProviderCard] = Field(default_factory=list)
    best_provider: Optional[ProviderCard] = None

    suggestions: List[str] = Field(default_factory=list)
    status_hint: Optional[str] = None