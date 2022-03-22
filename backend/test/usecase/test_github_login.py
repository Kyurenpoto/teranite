from abc import abstractmethod

import pytest
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user import GithubUser
from entity.github_user_info import GithubUserInfo
from hypothesis import given, strategies
from dependency import provider
from repository.github_authtoken_repository import GithubAuthTokenRepository
from repository.github_user_repository import GithubUserRepository
from repository.github_userinfo_repository import GithubUserInfoRepository

from usecase.github_login import GithubLoginWithoutToken


class FakeGithubAuthTokenRepository(GithubAuthTokenRepository):
    def __init__(self):
        self.exec = []

    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        self.exec += [f"findByTemporaryCode: {code}"]

        return GithubAuthToken("access_token", "refresh_token")


class FakeGithubUserRepositoryBase(GithubUserRepository):
    def __init__(self):
        self.exec = []

    async def readByEmail(self, email: str) -> GithubUser | None:
        self.exec += [f"readByEmail: {email}"]

        return await self.fake(email)

    async def create(self, user: GithubUser):
        self.exec += [f"create: {user}"]

    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        self.exec += [f"updateAuthToken: {email}, {authToken}"]

    @abstractmethod
    async def fake(self, email: str) -> GithubUser | None:
        pass


class FakeGithubUserRepository(FakeGithubUserRepositoryBase):
    async def fake(self, email: str) -> GithubUser | None:
        return GithubUser(email, GithubAuthToken("access_token", "refresh_token"))


class FakeNoneGithubUserRepository(FakeGithubUserRepositoryBase):
    async def fake(self, email: str) -> GithubUser | None:
        return None


class FakeGithubUserInfoRepository(GithubUserInfoRepository):
    def __init__(self):
        self.exec = []

    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        self.exec += [f"findByAuthToken: {authToken}"]

        return GithubUserInfo("heal9179@gmail.com")


@pytest.mark.asyncio
@given(strategies.characters())
async def test_login(code: str):
    provider.wire(
        {
            "auth-token-repo": FakeGithubAuthTokenRepository,
            "user-info-repo": FakeGithubUserInfoRepository,
            "user-repo": FakeGithubUserRepository,
        }
    )

    result = await GithubLoginWithoutToken().login(GithubTemporaryCode(code))

    assert result.accessToken == "heal9179@gmail.com" and result.refreshToken == "heal9179@gmail.com"
