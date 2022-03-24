import pytest
from datasource.github_userinfo_datasource import GithubUserInfoDataSource
from dependency import provider
from entity.auth_token import GithubAuthToken
from hypothesis import given, strategies

from repository.github_userinfo_simple_repository import GithubUserInfoSimpleRepository


class FakeGithubUserInfoDataSource(GithubUserInfoDataSource):
    def __init__(self):
        self.userInfos: dict[str, dict] = {}
        self.tokens: dict[str, str] = {}

    async def readUserInfo(self, accessToken: str) -> dict:
        return self.userInfos[self.tokens[accessToken]]


@pytest.mark.asyncio
@given(strategies.characters(), strategies.characters())
async def test_readByAuthToken(accessToken: str, refreshToken: str):
    provider.wire(
        {
            "user-info-source": FakeGithubUserInfoDataSource,
        }
    )

    userInfos = {"email": {"email": "email"}}
    userInfoSource: FakeGithubUserInfoDataSource = provider["user-info-source"]
    userInfoSource.userInfos = {**userInfos}
    userInfoSource.tokens = {accessToken: "email"}

    result = await GithubUserInfoSimpleRepository().readByAuthToken(GithubAuthToken(accessToken, refreshToken))

    assert result.email == "email"

    assert userInfoSource.userInfos == userInfos
