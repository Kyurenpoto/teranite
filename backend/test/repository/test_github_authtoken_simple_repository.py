from typing import NamedTuple

import pytest
from adaptor.datasource.github_authtoken_datasource import GithubAuthTokenDataSource
from adaptor.repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from hypothesis import given, strategies


class FakeGithubAuthTokenDataSource(GithubAuthTokenDataSource):
    def __init__(self):
        self.accounts: dict[str, dict] = {}

    async def createAuthToken(self, code: str) -> dict:
        try:
            token = self.accounts.pop(code)
            return token
        except:
            raise RuntimeError("invalid code")


class Fixture(NamedTuple):
    accounts: dict
    tokenSource: FakeGithubAuthTokenDataSource


class FixtureFactory:
    @classmethod
    def create(cls, accounts: dict):
        provider.wire({"auth": AuthContainer({"auth-token-source": FakeGithubAuthTokenDataSource})})

        fixture = Fixture(accounts, provider["auth"]["auth-token-source"])
        fixture.tokenSource.accounts = {**fixture.accounts}

        return fixture


@pytest.mark.asyncio
@given(strategies.characters())
async def test_issue_an_auth_token_from_the_github_auth_server_using_a_temporary_code(code: str):
    FixtureFactory.create({code: {"access_token": f"access_token@{code}", "refresh_token": f"refresh_token@{code}"}})

    authToken = await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert authToken == GithubAuthToken(f"access_token@{code}", f"refresh_token@{code}")


@pytest.mark.asyncio
@given(strategies.characters())
async def test_issue_an_auth_token_with_same_code(code: str):
    FixtureFactory.create({code: {"access_token": f"access_token@{code}", "refresh_token": f"refresh_token@{code}"}})

    authToken = await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert authToken == GithubAuthToken(f"access_token@{code}", f"refresh_token@{code}")

    with pytest.raises(RuntimeError) as e:
        await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert e.value.args[0] == "invalid code"


@pytest.mark.asyncio
@given(strategies.characters())
async def test_issue_an_auth_token_with_invalid_code(code: str):
    FixtureFactory.create({})

    with pytest.raises(RuntimeError) as e:
        await GithubAuthTokenSimpleRepository().readByTemporaryCode(GithubTemporaryCode(code))

    assert e.value.args[0] == "invalid code"
