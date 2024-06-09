from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.entity import Role
from tests.settings import test_settings


@pytest.mark.asyncio
async def test_get_roles(admin_authenticated_client, db_session, roles):
    db_roles = (await db_session.scalars(select(Role))).all()
    expected_roles = [{"id": role.id, "name": role.name} for role in db_roles]
    token = admin_authenticated_client.headers.get("Authorization")
    headers = {'Authorization': f'Bearer {token}'}
    response = await admin_authenticated_client.get(f'http://{test_settings.service_url}/api/v1/role', headers=headers)

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    for role_response, expected_role in zip(response_data, expected_roles):
        assert role_response['id'] == str(expected_role['id'])
        assert role_response["name"] == expected_role["name"]
        assert role_response["access_level"] == expected_role["access_level"]


@pytest.mark.asyncio
async def test_cant_create_existing_role(admin_authenticated_client, db_session):
    response = await admin_authenticated_client.post("/role/create", json={'name': 'testrole', 'access_level': 1})

    assert response.status_code == HTTPStatus.BAD_REQUEST