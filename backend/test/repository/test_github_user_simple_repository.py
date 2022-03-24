import pytest
from datasource.github_user_datasource import GithubUserDataSource
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser
from hypothesis import given, strategies

from repository.github_user_simple_repository import GithubUserSimpleRepository


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


@pytest.mark.asyncio
@given(strategies.emails())
async def test_readByEmail_exists(email: str):
    provider.wire(
        {
            "user-source": FakeGithubUserDataSource,
        }
    )

    users = {email: {"email": email, "githubAccessToken": email, "githubRefreshToken": email}}

    userSource: FakeGithubUserDataSource = provider["user-source"]
    userSource.users = {**users}

    result = await GithubUserSimpleRepository().readByEmail(email)

    assert result is not None
    assert (
        result.email == users[email]["email"]
        and result.authToken.accessToken == users[email]["githubAccessToken"]
        and result.authToken.refreshToken == users[email]["githubRefreshToken"]
    )

    assert userSource.users == users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_readByEmail_not_exists(email: str):
    provider.wire(
        {
            "user-source": FakeGithubUserDataSource,
        }
    )

    users = {}

    userSource: FakeGithubUserDataSource = provider["user-source"]
    userSource.users = {**users}

    result = await GithubUserSimpleRepository().readByEmail(email)

    assert result is None

    assert userSource.users == users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_create(email: str):
    provider.wire(
        {
            "user-source": FakeGithubUserDataSource,
        }
    )

    users = {}

    userSource: FakeGithubUserDataSource = provider["user-source"]
    userSource.users = {**users}

    await GithubUserSimpleRepository().create(GithubUser(email, GithubAuthToken(email, email)))

    assert len(userSource.users) == len(users) + 1
    assert dict(filter(lambda x: x[0] != email, userSource.users.items())) == users


@pytest.mark.asyncio
@given(strategies.emails())
async def test_updateAuthToken(email: str):
    provider.wire(
        {
            "user-source": FakeGithubUserDataSource,
        }
    )

    users = {email: {"email": email, "githubAccessToken": "", "githubRefreshToken": ""}}

    userSource: FakeGithubUserDataSource = provider["user-source"]
    userSource.users = {**users}

    await GithubUserSimpleRepository().updateAuthToken(email, GithubAuthToken(email, email))

    assert len(userSource.users) == len(users)
    assert list(filter(lambda x: x[0] == email, userSource.users.items()))[0][1]["email"] == email
    assert dict(filter(lambda x: x[0] != email, userSource.users.items())) == dict(
        filter(lambda x: x[0] != email, users.items())
    )
