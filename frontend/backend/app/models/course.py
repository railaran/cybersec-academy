from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Course(Base):
    __tablename__ = "courses"
    id             = Column(Integer, primary_key=True)
    title          = Column(String(200), nullable=False, index=True)
    category       = Column(String(50), default="general")
    description    = Column(Text)
    level          = Column(String(20), default="beginner")
    duration_hours = Column(Integer, default=0)
    price          = Column(Integer, default=0)
    thumbnail_url  = Column(String(500))
    is_published   = Column(Boolean, default=False, index=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
