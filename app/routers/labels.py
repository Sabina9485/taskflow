from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Label
from app.schemas import LabelCreate, LabelRead, LabelUpdate

router = APIRouter(prefix="/v1/labels", tags=["labels"])


@router.get("", response_model=list[LabelRead])
def list_labels(db: Session = Depends(get_db)):
    return db.scalars(select(Label)).all()


@router.get("/{label_id}", response_model=LabelRead)
def get_label(label_id: int, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if not label:
        raise HTTPException(404, "Label not found")
    return label


@router.post("", response_model=LabelRead, status_code=status.HTTP_201_CREATED)
def create_label(payload: LabelCreate, db: Session = Depends(get_db)):
    label = Label(**payload.model_dump())
    db.add(label)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Label name already exists")
    db.refresh(label)
    return label


@router.patch("/{label_id}", response_model=LabelRead)
def update_label(label_id: int, payload: LabelUpdate, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if not label:
        raise HTTPException(404, "Label not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(label, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Label name already exists")
    db.refresh(label)
    return label


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if not label:
        raise HTTPException(404, "Label not found")
    db.delete(label)
    db.commit()
