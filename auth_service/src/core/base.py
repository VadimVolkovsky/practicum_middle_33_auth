"""Импорты класса Base и всех моделей для Alembic."""
from db.postgres import Base  # noqa
from models.entity import User, Role, UserLoginHistory  # noqa
