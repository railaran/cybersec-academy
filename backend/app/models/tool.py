from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CyberTool(Base):
    __tablename__ = "cyber_tools"
    id           = Column(Integer, primary_key=True)
    name         = Column(String(120), nullable=False, index=True)
    category     = Column(String(50), default="general")   # recon, exploitation, forensics, dll
    description  = Column(Text)
    homepage     = Column(String(300))
    install_cmd  = Column(String(300))
    usage_hint   = Column(Text)
    platform     = Column(String(50), default="linux")     # linux, windows, mac, web
    is_open_source = Column(Boolean, default=True)
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
