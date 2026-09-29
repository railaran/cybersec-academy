from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    category: Optional[str] = "general"
    description: Optional[str] = None
    level: str = "beginner"
    duration_hours: int = 0
    price: int = 0
    thumbnail_url: Optional[str] = None
    is_published: bool = False

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    duration_hours: Optional[int] = None
    price: Optional[int] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None

class CourseOut(CourseBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
