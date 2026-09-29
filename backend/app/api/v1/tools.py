from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import require_admin
from app.models.tool import CyberTool
from app.schemas.tool import ToolCreate, ToolUpdate, ToolOut

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("/")
def list_tools(page: int = Query(1, ge=1), limit: int = Query(12, ge=1, le=100),
               search: Optional[str] = None, category: Optional[str] = None,
               platform: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(CyberTool)
    if search:
        q = q.filter((CyberTool.name.ilike(f"%{search}%")) |
                     (CyberTool.description.ilike(f"%{search}%")))
    if category: q = q.filter(CyberTool.category == category)
    if platform: q = q.filter(CyberTool.platform == platform)
    total = q.count()
    items = q.order_by(CyberTool.name.asc()).offset((page - 1) * limit).limit(limit).all()
    return {"items": [ToolOut.model_validate(i).model_dump() for i in items],
            "total": total, "page": page, "limit": limit}


@router.get("/{tool_id}", response_model=ToolOut)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    t = db.query(CyberTool).get(tool_id)
    if not t: raise HTTPException(404, "Tool tidak ditemukan")
    return t


@router.post("/", response_model=ToolOut, status_code=201)
def create_tool(payload: ToolCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    t = CyberTool(**payload.model_dump())
    db.add(t); db.commit(); db.refresh(t)
    return t


@router.put("/{tool_id}", response_model=ToolOut)
def update_tool(tool_id: int, payload: ToolUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    t = db.query(CyberTool).get(tool_id)
    if not t: raise HTTPException(404, "Tool tidak ditemukan")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    db.commit(); db.refresh(t)
    return t


@router.delete("/{tool_id}", status_code=204)
def delete_tool(tool_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    t = db.query(CyberTool).get(tool_id)
    if not t: raise HTTPException(404, "Tool tidak ditemukan")
    db.delete(t); db.commit()
