from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class LabBase(BaseModel):
    title: str
    slug: Optional[str] = None
    category: str = "general"
    difficulty: str = "easy"
    description: Optional[str] = None
    objective: Optional[str] = None
    docker_image: Optional[str] = None
    flag: Optional[str] = None
    points: int = 100
    time_limit_min: int = 60
    is_active: bool = True

class LabCreate(LabBase):
    pass

class LabUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[str] = None
    docker_image: Optional[str] = None
    flag: Optional[str] = None
    points: Optional[int] = None
    time_limit_min: Optional[int] = None
    is_active: Optional[bool] = None

class LabOut(LabBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class FlagSubmit(BaseModel):
    flag: str
