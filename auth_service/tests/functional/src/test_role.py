from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.entity import Role
from tests import test_settings


@pytest.mark.asyncio
async def test_get_roles(admin_authenticated_client, db_session, roles, redis_client):
    db_roles = (await db_session.scalars(select(Role))).all()
    expected_roles = [{"id": role.id, "name": role.name} for role in db_roles]

    # token = admin_authenticated_client.headers.get("Authorization")
    # headers = {'Authorization': f'Bearer {token}'}

    response = await admin_authenticated_client.get(f'http://{test_settings.service_host}:{test_settings.service_port}'
                                                    f'/api/v1/role')

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    for role_response, expected_role in zip(response_data, expected_roles):
        assert role_response['id'] == expected_role['id']
        assert role_response['name'] == expected_role['name']


@pytest.mark.asyncio
async def test_create_exist_role(admin_authenticated_client, db_session):
    response = await admin_authenticated_client.post(f'http://{test_settings.service_url}/api/v1/role/create',
                                                     json={'name': 'user'})

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_create_role(admin_authenticated_client, db_session):
    assert len((await db_session.scalars(select(Role))).all()) == 3

    response = await admin_authenticated_client.post(f'http://{test_settings.service_url}/api/v1/role/create',
                                                     json={'name': 'new_role'})

    assert response.status_code == HTTPStatus.CREATED
    assert len((await db_session.scalars(select(Role))).all()) == 4


@pytest.mark.asyncio
async def test_create_role_not_admin(user_authenticated_client, db_session):
    assert len((await db_session.scalars(select(Role))).all()) == 3

    response = await user_authenticated_client.post(f'http://{test_settings.service_url}/api/v1/role/create',
                                                    json={'name': 'new_role'})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert len((await db_session.scalars(select(Role))).all()) == 3
