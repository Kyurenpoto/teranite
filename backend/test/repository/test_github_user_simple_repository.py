import pytest
from adaptor.datasource.github_user_datasource import GithubUserDataSource
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser
from hypothesis import given, strategies

from adaptor.repository.github_user_simple_repository import GithubUserSimpleRepository


class FakeGithubUserDataSource(GithubUserDataSource):
    def __init__(self):
        self.users: dict[str, dict] = {}

    async def readUser(self, email: str) -> dict:
        return self.users[email] if email in self.users else {}

    async def createUser(self, email: str, accessToken: str, refreshToken: str):
        self.users[email] = {"email": email, "githubAccessToken": accessToken, "githubRefreshToken": refreshToken}

    async def updateUser(self, email: str, accessToken: str, refreshToken: str):
        self.users[email]["githubAccessToken"] = accessToken
        self.users[email]["githubRefreshToken"] = refreshToken


class Fixture:
    def __init__(self, users: dict):
        provider.wire({"auth": AuthContainer({"user-source": FakeGithubUserDataSource})})

        self.users = users

        self.userSource: FakeGithubUserDataSource = provider["auth"]["user-source"]
        self.userSource.users = {**self.users}


@pytest.mark.asyncio
@given(strategies.emails())
async def test_readByEmail_exists(email: str):
    fixture = Fixture({email: {"email": email, "githubAccessToken": email, "githubRefreshToken": email}})

    result = await GithubUserSimpleRepository().readByEmail(email)

    assert result is not None
    assert (
        result.email == fixture.users[email]["email"]
        and result.authToken.accessToken == fixture.users[email]["githubAccessToken"]
        and result.authToken.refreshToken == fixture.users[email]["githubRefreshToken"]
    )

    assert fixture.userSource.users == fixture.users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_readByEmail_not_exists(email: str):
    fixture = Fixture({})

    result = await GithubUserSimpleRepository().readByEmail(email)

    assert result is None

    assert fixture.userSource.users == fixture.users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_create(email: str):
    fixture = Fixture({})

    await GithubUserSimpleRepository().create(GithubUser(email, GithubAuthToken(email, email)))

    assert len(fixture.userSource.users) == len(fixture.users) + 1
    assert dict(filter(lambda x: x[0] != email, fixture.userSource.users.items())) == fixture.users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_updateAuthToken(email: str):
    fixture = Fixture({email: {"email": email, "githubAccessToken": "", "githubRefreshToken": ""}})

    await GithubUserSimpleRepository().updateAuthToken(email, GithubAuthToken(email, email))

    assert len(fixture.userSource.users) == len(fixture.users)
    assert list(filter(lambda x: x[0] == email, fixture.userSource.users.items()))[0][1]["email"] == email
    assert dict(filter(lambda x: x[0] != email, fixture.userSource.users.items())) == dict(
        filter(lambda x: x[0] != email, fixture.users.items())
    )
