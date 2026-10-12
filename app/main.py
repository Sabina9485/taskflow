from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import comments, labels, projects, tasks, users

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(labels.router)
app.include_router(tasks.router)
app.include_router(comments.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
