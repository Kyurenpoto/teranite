import pytest
from datasource.github_authtoken_datasource import GithubAuthTokenDataSource
from dependency import provider
from entity.github_temporary_code import GithubTemporaryCode
from hypothesis import given, strategies

from repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository


class FakeGithubAuthTokenDataSource(GithubAuthTokenDataSource):
    async def createAuthToken(self, code: str) -> dict:
        return {"access_token": "heal9179@gmail.com", "refresh_token": "heal9179@gmail.com"}


@pytest.mark.asyncio
@given(strategies.characters())
async def test_readByTemporaryCode(code: str):
    provider.wire(
        {
            "auth-token-source": FakeGithubAuthTokenDataSource,
        }
    )

    result = await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert result.accessToken == "heal9179@gmail.com" and result.refreshToken == "heal9179@gmail.com"
