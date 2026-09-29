from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def list_courses(page: int = Query(1, ge=1), limit: int = Query(9, ge=1, le=100),
                 search: Optional[str] = None, level: Optional[str] = None,
                 status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Course)
    if search: q = q.filter(Course.title.ilike(f"%{search}%"))
    if level:  q = q.filter(Course.level == level)
    if status == "published": q = q.filter(Course.is_published.is_(True))
    elif status == "draft":   q = q.filter(Course.is_published.is_(False))
    total = q.count()
    items = q.order_by(Course.id.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"items": [CourseOut.model_validate(i).model_dump() for i in items],
            "total": total, "page": page, "limit": limit}


@router.post("/", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = Course(**payload.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.put("/{cid}", response_model=CourseOut)
def update_course(cid: int, payload: CourseUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(Course).get(cid)
    if not c:
        raise HTTPException(404, "Course tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c


@router.delete("/{cid}", status_code=204)
def delete_course(cid: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(Course).get(cid)
    if not c:
        raise HTTPException(404, "Course tidak ditemukan")
    db.delete(c); db.commit()
