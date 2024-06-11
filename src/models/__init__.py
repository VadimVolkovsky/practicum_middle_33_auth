from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .entity import Role, User, UserLoginHistory # noqa
