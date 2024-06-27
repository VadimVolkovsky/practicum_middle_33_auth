from models.entity import SocialNetwork
from .base import CRUDBase


class CRUDSocialNetwork(CRUDBase):
    """Класс для работы с моделью SocialNetwork в БД"""
    pass


social_network_crud = CRUDSocialNetwork(SocialNetwork)
