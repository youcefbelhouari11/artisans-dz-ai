from pydantic import BaseModel
from typing import Optional


class ProviderCard(BaseModel):
    id: int
    first_name: str
    last_name: str

    rating_average: Optional[float] = None
    experience_years: Optional[int] = None

    city: Optional[str] = None
    category: Optional[str] = None

    service_title: Optional[str] = None
    price: Optional[float] = None

    is_available: Optional[bool] = None
    is_verified: Optional[bool] = None
    trust_score: Optional[float] = None

    score: Optional[float] = None