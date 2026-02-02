from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Tag
from app.schemas.tag_schema import TagCreate, TagUpdate, TagRead
from app.utils.admin import require_admin
from app.models.user import User


router = APIRouter()

@router.get("", response_model=List[TagRead])
def list_tags(
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    return db.query(Tag).order_by(Tag.type, Tag.name).all()

@router.post("", response_model=TagRead)
def create_tag(
        payload: TagCreate,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    if db.query(Tag).filter(Tag.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Tag slug already exists")

    parent = None
    if payload.parent_id:
        parent = db.query(Tag).get(payload.parent_id)
        if not parent:
            raise HTTPException(status_code=400, detail="Parent tag not found")

    tag = Tag(
        name=payload.name,
        slug=payload.slug,
        type=payload.type,
        parent=parent,
        is_active=payload.is_active,
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag

@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
        tag_id: int,
        payload: TagUpdate,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    tag = db.query(Tag).get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Slug uniqueness check
    if payload.slug and payload.slug != tag.slug:
        if db.query(Tag).filter(Tag.slug == payload.slug).first():
            raise HTTPException(status_code=400, detail="Slug already in use")

    parent = None
    if payload.parent_id is not None:
        if payload.parent_id:
            parent = db.query(Tag).get(payload.parent_id)
            if not parent:
                raise HTTPException(status_code=400, detail="Parent tag not found")
        tag.parent = parent

    for field, value in payload.dict(exclude_unset=True).items():
        if field not in {"parent_id"}:
            setattr(tag, field, value)

    db.commit()
    db.refresh(tag)

    return tag

@router.patch("/{tag_id}/toggle")
def toggle_tag_status(
        tag_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    tag = db.query(Tag).get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.is_active = not tag.is_active
    db.commit()

    return {
        "tag_id": tag.id,
        "is_active": tag.is_active,
        "message": "Tag status updated",
    }

