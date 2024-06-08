from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.entity import Role


@pytest.mark.asyncio
async def test_get_roles(superuser_authenticated_client, test_db_session, roles):
    db_roles = (await test_db_session.scalars(select(Role))).all()
    expected_roles = [{"id": role.id, "name": role.name, "access_level": role.access_level} for role in db_roles]

    response = await superuser_authenticated_client.get("/role/")

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    for role_response, expected_role in zip(response_data, expected_roles):
        assert role_response['id'] == str(expected_role['id'])
        assert role_response["name"] == expected_role["name"]
        assert role_response["access_level"] == expected_role["access_level"]


@pytest.mark.asyncio
async def test_cant_create_existing_role(superuser_authenticated_client, test_db_session):
    response = await superuser_authenticated_client.post("/role/create", json={'name': 'testrole', 'access_level': 1})

    assert response.status_code == HTTPStatus.BAD_REQUEST