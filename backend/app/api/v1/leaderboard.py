from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.progress import UserProgress

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
def leaderboard(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    rows = (
        db.query(
            User.id,
            User.full_name,
            User.email,
            func.coalesce(func.sum(UserProgress.points), 0).label("total_points"),
            func.count(UserProgress.id).label("completed"),
        )
        .outerjoin(UserProgress, UserProgress.user_id == User.id)
        .group_by(User.id, User.full_name, User.email)
        .order_by(func.coalesce(func.sum(UserProgress.points), 0).desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "user_id": r.id,
            "name": r.full_name or r.email,
            "points": int(r.total_points),
            "completed": int(r.completed),
        }
        for i, r in enumerate(rows)
    ]
