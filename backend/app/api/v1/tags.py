from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.product import Tag
from app.schemas.tag_schema import TagRead
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("", response_model=List[TagRead])
def list_tags(
        db: Session = Depends(get_db)
):
    return db.query(Tag).order_by(Tag.type, Tag.name).all()
