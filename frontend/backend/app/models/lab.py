from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Lab(Base):
    __tablename__ = "labs"
    id             = Column(Integer, primary_key=True)
    title          = Column(String(200), nullable=False, index=True)
    slug           = Column(String(200), unique=True, index=True)
    category       = Column(String(50), default="general")   # web, network, forensics, crypto, osint, dll
    difficulty     = Column(String(20), default="easy")      # easy, medium, hard, insane
    description    = Column(Text)
    objective      = Column(Text)
    docker_image   = Column(String(200))
    flag           = Column(String(200))
    points         = Column(Integer, default=100)
    time_limit_min = Column(Integer, default=60)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

class LabInstance(Base):
    __tablename__ = "lab_instances"
    id         = Column(Integer, primary_key=True)
    lab_id     = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"))
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status     = Column(String(20), default="stopped")  # running, stopped, expired
    container  = Column(String(200))
    started_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    solved     = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
