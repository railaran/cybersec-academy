from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True)
    full_name  = Column(String(150))
    email      = Column(String(150), unique=True, index=True)
    password   = Column(String(255))
    role       = Column(String(20), default="student")
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
