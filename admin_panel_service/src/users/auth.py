import http
import json
import logging
from enum import StrEnum, auto
from urllib.request import Request

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from httpx import TooManyRedirects, Timeout
from pip._vendor.requests import RequestException

User = get_user_model()


class Roles(StrEnum):
    ADMIN = auto()
    SUBSCRIBER = auto()


class CustomBackend(BaseBackend):
    def authenticate(self, request: Request, username: str =None, password: str =None):
        url = settings.AUTH_ADMIN_LOGIN_URL
        payload = {'email': username, 'password': password}
        response = requests.post(url, data=json.dumps(payload))

        try:
            response = requests.post(url, data=json.dumps(payload))
        except (TooManyRedirects, RequestException, Timeout):
            logging.error('Auth service not working!')
            return None

        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, created = User.objects.get_or_create(id=data['id'], )
            user.email = data.get('email')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.is_admin = data.get('role') == Roles.ADMIN
            # user.is_active = data.get('is_active')
            user.is_active = True  # TODO DEBUG
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
