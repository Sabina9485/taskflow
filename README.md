# TaskFlow API

REST API для управления задачами команды.

## Стек

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2
- Alembic
- Docker + Docker Compose

## Запуск

    cp .env.example .env
    docker compose up --build

API: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health

## Примеры запросов

Создать пользователя:

    curl -X POST http://localhost:8000/v1/users \
      -H "Content-Type: application/json" \
      -d '{"email":"alice@example.com","display_name":"Alice","role":"admin"}'

Создать задачу:

    curl -X POST http://localhost:8000/v1/tasks \
      -H "Content-Type: application/json" \
      -d '{"project_id":1,"title":"First task","status":"open","priority":"high"}'

Фильтры:

    curl "http://localhost:8000/v1/tasks?project_id=1&status=open"
    curl "http://localhost:8000/v1/comments?task_id=1"

## Миграции

    alembic upgrade head
    alembic downgrade base
    alembic upgrade head
