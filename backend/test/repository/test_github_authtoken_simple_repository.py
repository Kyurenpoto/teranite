import pytest
from adaptor.datasource.github_authtoken_datasource import GithubAuthTokenDataSource
from dependencies.dependency import provider
from entity.github_temporary_code import GithubTemporaryCode
from hypothesis import given, strategies

from adaptor.repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository


class FakeGithubAuthTokenDataSource(GithubAuthTokenDataSource):
    def __init__(self):
        self.accounts: dict[str, dict] = {}

    async def createAuthToken(self, code: str) -> dict:
        self.accounts["email"] = {
            "email": "email",
            "access_token": f"access_token@{code}",
            "refresh_token": f"refresh_token@{code}",
        }
        return {
            "access_token": self.accounts["email"]["access_token"],
            "refresh_token": self.accounts["email"]["refresh_token"],
        }


@pytest.mark.asyncio
@given(strategies.characters())
async def test_readByTemporaryCode_issued(code: str):
    provider.wire(
        {
            "auth-token-source": FakeGithubAuthTokenDataSource,
        }
    )

    accounts = {
        "email": {
            "email": "email",
            "access_token": f"accesstoken@{code}",
            "refresh_token": f"refreshtoken@{code}",
        }
    }

    tokenSource: FakeGithubAuthTokenDataSource = provider["auth-token-source"]
    tokenSource.accounts = {**accounts}

    result = await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert result.accessToken == f"access_token@{code}" and result.refreshToken == f"refresh_token@{code}"

    assert len(tokenSource.accounts) == len(accounts)

    email = list(filter(lambda x: x[1]["access_token"] == f"access_token@{code}", tokenSource.accounts.items()))[0][0]
    assert list(filter(lambda x: x[0] == email, tokenSource.accounts.items()))[0][0] == email
    assert dict(filter(lambda x: x[0] != email, tokenSource.accounts.items())) == dict(
        filter(lambda x: x[0] != email, accounts.items())
    )
