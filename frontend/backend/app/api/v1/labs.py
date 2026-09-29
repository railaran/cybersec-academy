import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.lab import Lab
from app.schemas.lab import LabCreate, LabUpdate, LabOut, FlagSubmit

router = APIRouter(prefix="/labs", tags=["Labs"])


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@router.get("/")
def list_labs(page: int = Query(1, ge=1), limit: int = Query(9, ge=1, le=100),
              search: Optional[str] = None, category: Optional[str] = None,
              difficulty: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Lab)
    if search:     q = q.filter(Lab.title.ilike(f"%{search}%"))
    if category:   q = q.filter(Lab.category == category)
    if difficulty: q = q.filter(Lab.difficulty == difficulty)
    total = q.count()
    items = q.order_by(Lab.id.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"items": [LabOut.model_validate(i).model_dump() for i in items],
            "total": total, "page": page, "limit": limit}


@router.get("/{lab_id}", response_model=LabOut)
def get_lab(lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(Lab).get(lab_id)
    if not lab: raise HTTPException(404, "Lab tidak ditemukan")
    return lab


@router.post("/", response_model=LabOut, status_code=201)
def create_lab(payload: LabCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    data = payload.model_dump()
    if not data.get("slug"):
        data["slug"] = slugify(data["title"])
    if db.query(Lab).filter(Lab.slug == data["slug"]).first():
        raise HTTPException(400, "Slug sudah dipakai")
    lab = Lab(**data)
    db.add(lab); db.commit(); db.refresh(lab)
    return lab


@router.put("/{lab_id}", response_model=LabOut)
def update_lab(lab_id: int, payload: LabUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    lab = db.query(Lab).get(lab_id)
    if not lab: raise HTTPException(404, "Lab tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(lab, k, v)
    db.commit(); db.refresh(lab)
    return lab


@router.delete("/{lab_id}", status_code=204)
def delete_lab(lab_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    lab = db.query(Lab).get(lab_id)
    if not lab: raise HTTPException(404, "Lab tidak ditemukan")
    db.delete(lab); db.commit()


@router.post("/{lab_id}/submit")
def submit_flag(lab_id: int, payload: FlagSubmit, db: Session = Depends(get_db)):
    lab = db.query(Lab).get(lab_id)
    if not lab: raise HTTPException(404, "Lab tidak ditemukan")
    if not lab.flag:
        raise HTTPException(400, "Lab belum punya flag")
    correct = payload.flag.strip() == lab.flag.strip()
    return {"correct": correct,
            "message": "Flag benar!" if correct else "Flag salah, coba lagi",
            "points": lab.points if correct else 0}
