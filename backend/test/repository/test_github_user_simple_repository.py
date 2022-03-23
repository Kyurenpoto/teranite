import pytest
from datasource.github_user_datasource import GithubUserDataSource
from dependency import provider
from hypothesis import given, strategies

from repository.github_user_simple_repository import GithubUserSimpleRepository


@pytest.mark.asyncio
@given(strategies.emails())
async def test_readByEmail(email: str):
    class FakeGithubUserDataSource(GithubUserDataSource):
        async def readUser(self, email: str) -> dict:
            return {"email": email, "githubAccessToken": email, "githubRefreshToken": email}

        async def createUser(self, email: str, accessToken: str, refreshToken: str):
            pass

        async def updateUser(self, email: str, accessToken: str, refreshToken: str):
            pass

    provider.wire(
        {
            "user-source": FakeGithubUserDataSource,
        }
    )

    result = await GithubUserSimpleRepository().readByEmail(email)

    assert result is not None
    assert result.email == email and result.authToken.accessToken == email and result.authToken.refreshToken == email
