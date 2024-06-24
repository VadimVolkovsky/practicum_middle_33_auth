from dataclasses import dataclass

import pytest_asyncio
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture
async def get_request(api_session):
    async def inner(url, params=None, headers=None):
        async with api_session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest_asyncio.fixture(scope='session')
async def post_request(api_session):
    async def inner(url, data=None, headers=None):
        async with api_session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
