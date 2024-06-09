import subprocess

import pytest_asyncio

from models.entity import User
from tests.settings import test_settings


@pytest_asyncio.fixture
async def admin_authenticated_client(api_session, admin_user, post_request):
    login_data = {'login': admin_user.login, 'password': 'test_password'}
    response = subprocess.run(['curl', '-X', 'GET', 'http://'+test_settings.service_url+'/api/openapi'], capture_output=True, text=True)
    response = await api_session.post(f'http://{test_settings.service_url}/api/v1/auth/login', json=login_data)
    # response = await post_request(f'{test_settings.service_url}/api/v1/auth/login', login_data)
    assert response.status_code == 200
    cookies = response.cookies
    api_session.cookies = cookies
    yield api_session


@pytest_asyncio.fixture
async def admin_user(db_session, roles):
    admin_role = roles['admin']
    admin_user = User(login='admin_username3',
                      password='test_password',
                      first_name='test_first_name',
                      last_name='test_last_name',
                      role=admin_role.id,)
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    yield admin_user
