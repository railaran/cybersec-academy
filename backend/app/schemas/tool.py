from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ToolBase(BaseModel):
    name: str
    category: str = "general"
    description: Optional[str] = None
    homepage: Optional[str] = None
    install_cmd: Optional[str] = None
    usage_hint: Optional[str] = None
    platform: str = "linux"
    is_open_source: bool = True
    is_active: bool = True

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    install_cmd: Optional[str] = None
    usage_hint: Optional[str] = None
    platform: Optional[str] = None
    is_open_source: Optional[bool] = None
    is_active: Optional[bool] = None

class ToolOut(ToolBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
