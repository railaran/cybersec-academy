from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: str
    role: str = "student"
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
