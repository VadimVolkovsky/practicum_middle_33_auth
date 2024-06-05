from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Cхема UserCreate описывает то, что мы ожидаем получить при создании записи в базе данных. """
    login: str
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    """Модель для работы с аутентификацией пользователя"""
    login: str
    password: str


class UserUpdate(BaseModel):
    """Модель обновления данных пользователя"""
    login: str | None
    password: str | None


class UserInDB(BaseModel):
    """UserInDB — это то, что мы будем отдавать пользователю — детальную информацию по нужным полям модели. """
    id: UUID
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class JWTResponse(BaseModel):
    """Модель для работы с токенами"""
    access_token: str
    refresh_token: str
