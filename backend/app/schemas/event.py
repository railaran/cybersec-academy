from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    title: str
    slug: Optional[str] = None
    type: str = "ctf"
    description: Optional[str] = None
    location: Optional[str] = None
    cover_url: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    capacity: int = 0
    is_free: bool = True
    price: int = 0
    is_published: bool = False

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    cover_url: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    capacity: Optional[int] = None
    is_free: Optional[bool] = None
    price: Optional[int] = None
    is_published: Optional[bool] = None

class EventOut(EventBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
