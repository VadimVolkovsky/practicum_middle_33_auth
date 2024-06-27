"""Импорты класса Base и всех моделей для Alembic."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from src.models.entity import Role, User, UserLoginHistory # noqa
