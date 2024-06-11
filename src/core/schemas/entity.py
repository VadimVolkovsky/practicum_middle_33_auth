import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Cхема UserCreate описывает то, что мы ожидаем получить при создании записи в базе данных. """
    username: str
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    """Модель для работы с аутентификацией пользователя"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Модель обновления данных пользователя"""
    username: str | None = None
    password: str | None = None


class UserInDB(BaseModel):
    """UserInDB — это то, что мы будем отдавать пользователю — детальную информацию по нужным полям модели. """
    id: UUID
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserLoginHistory(BaseModel):
    user_id: UUID


class UserLoginHistoryInDB(BaseModel):
    """
    UserLoginHistoryInDB — это то, что мы будем отдавать пользователю — детальную информацию по нужным полям модели.
    """
    login_date: list[datetime.datetime]


class JWTResponse(BaseModel):
    """Модель для работы с токенами"""
    access_token: str
    refresh_token: str
