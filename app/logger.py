import logging
import sys

from app.config import settings


def setup_logger():
    # Читаем уровень из .env (по умолчанию INFO)
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Настраиваем формат (как в профессиональных проектах)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Вывод в консоль (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # Отключаем лишние логи от библиотек (например, sqlalchemy)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Экземпляр логгера, который можно импортировать в другие файлы
logger = logging.getLogger("taskflow")
