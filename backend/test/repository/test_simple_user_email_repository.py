from typing import NamedTuple

import pytest
from adaptor.repository.simple_user_email_repository import SimpleUserEmailRepository
from dependencies.dependency import provider
from dependencies.login_container import LoginContainer
from entity.auth_token import SocialAuthToken
from hypothesis import given, strategies


class InvalidSocialAuthTokenError(RuntimeError):
    def __init__(self):
        super().__init__("invalid social auth token")


class FakeUserEmailDataSource:
    def __init__(self):
        self.tokens = set()

    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken) -> str:
        if socialAuthToken not in self.tokens:
            raise InvalidSocialAuthTokenError()

        return f"email@{socialAuthToken.accessToken[7:]}"


class InvalidSocialTypeError(RuntimeError):
    def __init__(self):
        super().__init__("invalid social type")


class FakeUserEmailDataSourceColleciton:
    def __init__(self):
        self.sources = {}

    def source(self, social_type: str) -> FakeUserEmailDataSource:
        if social_type not in self.sources:
            raise InvalidSocialTypeError()

        return self.sources[social_type]


class Fixture(NamedTuple):
    tokens: dict[str, list[str]]
    sources: FakeUserEmailDataSourceColleciton


class FixtureFactory:
    @classmethod
    def create(cls, tokens: dict[str, list[str]] = dict()):
        provider.wire({"login": LoginContainer({"user-email-source-collection": FakeUserEmailDataSourceColleciton})})

        fixture = Fixture(
            tokens,
            provider["login"]["user-email-source-collection"],
        )

        fixture.sources.sources = {x: FakeUserEmailDataSource() for x in tokens.keys()}
        for k, v in tokens.items():
            fixture.sources.source(k).tokens = set(list(map(lambda x: SocialAuthToken(x, x), v)))

        return fixture


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_invalid_token(tokens: list[str]):
    FixtureFactory.create({".": tokens[1:]})

    with pytest.raises(InvalidSocialAuthTokenError):
        await SimpleUserEmailRepository().readBySocialAuthToken(SocialAuthToken(tokens[0], tokens[0]), ".")


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_invalid_social_type(social_types: list[str]):
    FixtureFactory.create({x: [] for x in social_types[1:]})

    with pytest.raises(InvalidSocialTypeError):
        await SimpleUserEmailRepository().readBySocialAuthToken(SocialAuthToken("", ""), social_types[0])


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_valid_token_with_valid_social_type(tokens: list[str]):
    fixture = FixtureFactory.create({".": tokens})

    await SimpleUserEmailRepository().readBySocialAuthToken(SocialAuthToken(tokens[0], tokens[0]), ".")

    assert fixture.sources.source(".").tokens == set(list(map(lambda x: SocialAuthToken(x, x), fixture.tokens["."])))
