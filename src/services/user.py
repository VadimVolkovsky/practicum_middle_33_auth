from werkzeug.security import check_password_hash

from crud.user import user_crud


class UserService:
    """Класс для хранения бизнес-логики модели User"""

    async def check_user_credentials(self, login, password, session) -> bool:
        """Метод для проверки логина и пароля пользователя с данными в БД"""
        user_obj = await user_crud.get_user_by_login(login, session)
        if user_obj:
            if check_password_hash(user_obj.password, password):
                return True
        return False


user_service = UserService()
