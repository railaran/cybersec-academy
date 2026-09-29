from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(User)
    if search:
        q = q.filter(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    if role:
        q = q.filter(User.role == role)
    total = q.count()
    items = q.order_by(User.id.desc()).offset((page - 1) * limit).limit(limit).all()
    return {
        "items": [UserOut.model_validate(i).model_dump() for i in items],
        "total": total, "page": page, "limit": limit,
    }


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email sudah terdaftar")
    u = User(**payload.model_dump())
    db.add(u); db.commit(); db.refresh(u)
    return u


@router.put("/{uid}", response_model=UserOut)
def update_user(uid: int, payload: UserUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.query(User).get(uid)
    if not u:
        raise HTTPException(404, "User tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(u, k, v)
    db.commit(); db.refresh(u)
    return u


@router.delete("/{uid}", status_code=204)
def delete_user(uid: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.query(User).get(uid)
    if not u:
        raise HTTPException(404, "User tidak ditemukan")
    db.delete(u); db.commit()
