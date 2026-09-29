from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    id            = Column(Integer, primary_key=True)
    title         = Column(String(200), nullable=False, index=True)
    slug          = Column(String(200), unique=True, index=True)
    type          = Column(String(30), default="ctf")     # ctf, workshop, webinar, bootcamp
    description   = Column(Text)
    location      = Column(String(200))                    # online / offline
    cover_url     = Column(String(500))
    start_at      = Column(DateTime(timezone=True))
    end_at        = Column(DateTime(timezone=True))
    capacity      = Column(Integer, default=0)
    is_free       = Column(Boolean, default=True)
    price         = Column(Integer, default=0)
    is_published  = Column(Boolean, default=False, index=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

class Registration(Base):
    __tablename__ = "event_registrations"
    id         = Column(Integer, primary_key=True)
    event_id   = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status     = Column(String(20), default="registered")  # registered, attended, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
