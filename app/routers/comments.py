from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment
from app.schemas import CommentCreate, CommentRead, CommentUpdate

router = APIRouter(prefix="/v1/comments", tags=["comments"])


@router.get("", response_model=list[CommentRead])
def list_comments(task_id: int | None = None, db: Session = Depends(get_db)):
    query = select(Comment)
    if task_id is not None:
        query = query.where(Comment.task_id == task_id)
    return db.scalars(query).all()


@router.get("/{comment_id}", response_model=CommentRead)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    return comment


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    comment = Comment(**payload.model_dump())
    db.add(comment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Invalid task_id or author_id")
    db.refresh(comment)
    return comment


@router.patch("/{comment_id}", response_model=CommentRead)
def update_comment(comment_id: int, payload: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(comment, k, v)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    db.delete(comment)
    db.commit()
