from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlayerBase(BaseModel):
    full_name: str
    number: int
    position: str
    photo_url: Optional[str] = None
    goals: int = 0
    assists: int = 0
    saves: int = 0

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    rating: float

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str

class NewsCreate(NewsBase):
    pass

class NewsItem(NewsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
