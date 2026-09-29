import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.event import Event, Registration
from app.schemas.event import EventCreate, EventUpdate, EventOut

router = APIRouter(prefix="/events", tags=["Events"])


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@router.get("/")
def list_events(page: int = Query(1, ge=1), limit: int = Query(9, ge=1, le=100),
                search: Optional[str] = None, type: Optional[str] = None,
                status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Event)
    if search: q = q.filter(Event.title.ilike(f"%{search}%"))
    if type:   q = q.filter(Event.type == type)
    if status == "published": q = q.filter(Event.is_published.is_(True))
    elif status == "draft":   q = q.filter(Event.is_published.is_(False))
    total = q.count()
    items = q.order_by(Event.start_at.desc().nullslast(), Event.id.desc()) \
             .offset((page - 1) * limit).limit(limit).all()
    return {"items": [EventOut.model_validate(i).model_dump() for i in items],
            "total": total, "page": page, "limit": limit}


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    e = db.query(Event).get(event_id)
    if not e: raise HTTPException(404, "Event tidak ditemukan")
    return e


@router.post("/", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    data = payload.model_dump()
    if not data.get("slug"):
        data["slug"] = slugify(data["title"])
    if db.query(Event).filter(Event.slug == data["slug"]).first():
        raise HTTPException(400, "Slug sudah dipakai")
    e = Event(**data)
    db.add(e); db.commit(); db.refresh(e)
    return e


@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    e = db.query(Event).get(event_id)
    if not e: raise HTTPException(404, "Event tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(e, k, v)
    db.commit(); db.refresh(e)
    return e


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    e = db.query(Event).get(event_id)
    if not e: raise HTTPException(404, "Event tidak ditemukan")
    db.delete(e); db.commit()


@router.post("/{event_id}/register")
def register_event(event_id: int, db: Session = Depends(get_db)):
    e = db.query(Event).get(event_id)
    if not e: raise HTTPException(404, "Event tidak ditemukan")
    if e.capacity > 0:
        count = db.query(Registration).filter(Registration.event_id == event_id,
                                              Registration.status == "registered").count()
        if count >= e.capacity:
            raise HTTPException(400, "Event sudah penuh")
    reg = Registration(event_id=event_id, user_id=1, status="registered")
    db.add(reg); db.commit(); db.refresh(reg)
    return {"ok": True, "registration_id": reg.id}
