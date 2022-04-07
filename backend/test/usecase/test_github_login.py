import pytest
from adaptor.repository.github_authtoken_repository import GithubAuthTokenRepository
from adaptor.repository.github_user_repository import GithubUserRepository
from adaptor.repository.github_userinfo_repository import GithubUserInfoRepository
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import GithubAuthToken, UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user import GithubUser
from entity.github_user_info import GithubUserInfo
from hypothesis import given, strategies

from usecase.github_login import GithubLoginWithoutToken
from usecase.github_login_port import GithubLoginWithoutTokenOutputPort


class FakeGithubAuthTokenRepository(GithubAuthTokenRepository):
    async def readByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return GithubAuthToken(f"access_token@{code}", f"refresh_token@{code}")


class FakeGithubUserRepository(GithubUserRepository):
    def __init__(self):
        self.users: dict[str, GithubUser] = {}

    async def readByEmail(self, email: str) -> GithubUser | None:
        return self.users[email] if email in self.users else None

    async def create(self, user: GithubUser):
        self.users[user.email] = user

    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        self.users[email] = GithubUser(email, authToken)


class FakeGithubUserInfoRepository(GithubUserInfoRepository):
    async def readByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return GithubUserInfo(f"email@{authToken.accessToken}")


class FakePresenter(GithubLoginWithoutTokenOutputPort):
    async def present(self, authToken: UserAuthToken):
        self.authToken = authToken


class Fixture:
    def __init__(self, users: dict):
        provider.wire(
            {
                "auth": AuthContainer(
                    {
                        "auth-token-repo": FakeGithubAuthTokenRepository,
                        "user-info-repo": FakeGithubUserInfoRepository,
                        "user-repo": FakeGithubUserRepository,
                        "token-presenter": FakePresenter,
                    }
                )
            }
        )

        self.users = users

        self.userRepo: FakeGithubUserRepository = provider["auth"]["user-repo"]
        self.userRepo.users = {**self.users}


@pytest.mark.asyncio
@given(strategies.characters())
async def test_login_old_user(code: str):
    fixture = Fixture(
        {
            f"email@access_token@{code}": GithubUser(
                f"email@access_token@{code}", GithubAuthToken(f"access_token@{code}", f"refresh_token@{code}")
            )
        }
    )

    await GithubLoginWithoutToken().login(GithubTemporaryCode(code))
    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.authToken == UserAuthToken(f"email@access_token@{code}", f"email@access_token@{code}")

    assert fixture.userRepo.users == fixture.users


@pytest.mark.asyncio
@given(strategies.characters())
async def test_login_new_user(code: str):
    fixture = Fixture({})

    await GithubLoginWithoutToken().login(GithubTemporaryCode(code))
    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.authToken == UserAuthToken(f"email@access_token@{code}", f"email@access_token@{code}")

    assert len(fixture.userRepo.users) == len(fixture.users) + 1
    assert dict(filter(lambda x: x[0] in fixture.userRepo.users, fixture.users.items())) == fixture.users
