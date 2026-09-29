from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    item_type  = Column(String(30), index=True)   # lab, quiz, course
    item_id    = Column(Integer, index=True)
    status     = Column(String(20), default="completed")
    score      = Column(Integer, default=0)
    points     = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
