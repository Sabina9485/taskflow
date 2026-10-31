from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger, setup_logger  # <-- Импортируем логгер
from app.routers import comments, labels, projects, tasks, users

# Настраиваем логгер при старте
setup_logger()

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(labels.router)
app.include_router(tasks.router)
app.include_router(comments.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    # ПРИМЕРЫ ВСЕХ УРОВНЕЙ ЛОГИРОВАНИЯ:
    logger.debug("Это DEBUG сообщение (подробности для разработчика)")
    logger.info("Это INFO сообщение (обычное событие)")
    logger.warning("Это WARNING сообщение (что-то подозрительное)")
    logger.error("Это ERROR сообщение (ошибка, но приложение работает)")
    logger.critical("Это CRITICAL сообщение (критическая ошибка)")

    db.execute(text("SELECT 1"))
    return {"status": "ok"}
