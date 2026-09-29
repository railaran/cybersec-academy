from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.course import Course
from app.models.lab import Lab
from app.models.quiz import Quiz
from app.models.tool import CyberTool
from app.models.event import Event

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "users":   db.query(User).count(),
        "courses": db.query(Course).count(),
        "labs":    db.query(Lab).count(),
        "quizzes": db.query(Quiz).count(),
        "tools":   db.query(CyberTool).count(),
        "events":  db.query(Event).count(),
    }


@router.get("/recent")
def recent(db: Session = Depends(get_db)):
    def top(model, limit=5):
        return [{"id": x.id, "title": getattr(x, "title", getattr(x, "name", ""))}
                for x in db.query(model).order_by(model.id.desc()).limit(limit).all()]
    return {
        "courses": top(Course),
        "labs":    top(Lab),
        "quizzes": top(Quiz),
        "tools":   top(CyberTool),
        "events":  top(Event),
    }
