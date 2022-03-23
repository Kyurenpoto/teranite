import pytest
from datasource.github_userinfo_datasource import GithubUserInfoDataSource
from dependency import provider
from entity.auth_token import GithubAuthToken
from hypothesis import given, strategies

from repository.github_userinfo_simple_repository import GithubUserInfoSimpleRepository


class FakeGithubUserInfoDataSource(GithubUserInfoDataSource):
    async def readUserInfo(self, accessToken: str) -> dict:
        return {"email": "heal9179@gmail.com"}


@pytest.mark.asyncio
@given(strategies.characters(), strategies.characters())
async def test_readByAuthToken(accessToken: str, refreshToken: str):
    provider.wire(
        {
            "user-info-source": FakeGithubUserInfoDataSource,
        }
    )

    result = await GithubUserInfoSimpleRepository().readByAuthToken(GithubAuthToken(accessToken, refreshToken))

    assert result.email == "heal9179@gmail.com"
