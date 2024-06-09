from dataclasses import dataclass

import pytest_asyncio
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture
async def post_request(api_session):
    async def inner(url, data):
        async with api_session.post(url, json=data) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner