import typer
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import app_settings
from src.models.entity import User, Role

Base = declarative_base()
dsn = (f'postgresql+psycopg2://{app_settings.postgres_user}:{app_settings.postgres_password}@'
       f'{app_settings.postgres_host}:{app_settings.postgres_port}/{app_settings.postgres_db}')
engine = create_engine(dsn, echo=True, future=True)
session_maker = sessionmaker(engine, expire_on_commit=False)
session = session_maker()


def create_superuser():
    """Создание супер пользователя"""
    role_obj = session.execute(select(Role).where(Role.name == 'admin'))
    admin_role = role_obj.scalars().first()

    user_obj = User(
        email='admin@mail.ru',
        first_name='admin',
        last_name='god',
        password='admin_password',
        role=admin_role
    )

    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    print('superuser created:')
    print(f'email: {user_obj.email}')
    print(f'password: admin_password')


if __name__ == "__main__":
    typer.run(create_superuser)
