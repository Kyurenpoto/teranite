from typing import NamedTuple

import pytest
from adaptor.repository.simple_social_auth_token_repository import SimpleSocialAuthTokenRepository
from adaptor.repository.social_auth_token_repository import InvalidTemporaryCodeError
from dependencies.dependency import provider
from dependencies.login_container import LoginContainer
from entity.auth_token import SocialAuthToken
from entity.temporary_code import TemporaryCode
from hypothesis import given, strategies


class FakeSocialAuthTokenDataSource:
    def __init__(self):
        self.codes = set()

    async def readByTemporaryCode(self, code: TemporaryCode) -> SocialAuthToken:
        if str(code) not in self.codes:
            raise InvalidTemporaryCodeError()

        self.codes.remove(code)

        return SocialAuthToken(f"access@{code}", f"refresh@{code}")


class InvalidSocialTypeError(RuntimeError):
    def __init__(self):
        super().__init__("invalid social type")


class FakeSocialAuthTokenDataSourceColleciton:
    def __init__(self):
        self.sources = {}

    def source(self, social_type: str) -> FakeSocialAuthTokenDataSource:
        if social_type not in self.sources:
            raise InvalidSocialTypeError()

        return self.sources[social_type]


class Fixture(NamedTuple):
    codes: dict[str, list[str]]
    sources: FakeSocialAuthTokenDataSourceColleciton


class FixtureFactory:
    @classmethod
    def create(cls, codes: dict[str, list[str]] = dict()):
        provider.wire(
            {"login": LoginContainer({"social-auth-token-source-collection": FakeSocialAuthTokenDataSourceColleciton})}
        )

        fixture = Fixture(
            codes,
            provider["login"]["social-auth-token-source-collection"],
        )

        fixture.sources.sources = {x: FakeSocialAuthTokenDataSource() for x in codes.keys()}
        for k, v in codes.items():
            fixture.sources.source(k).codes = set(v)

        return fixture


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_invalid_temporary_code(codes: list[str]):
    FixtureFactory.create({".": codes[1:]})

    with pytest.raises(InvalidTemporaryCodeError):
        await SimpleSocialAuthTokenRepository().readByTemporaryCode(TemporaryCode(codes[0]), ".")


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_invalid_social_type(social_types: list[str]):
    FixtureFactory.create({x: [] for x in social_types[1:]})

    with pytest.raises(InvalidSocialTypeError):
        await SimpleSocialAuthTokenRepository().readByTemporaryCode(TemporaryCode(""), social_types[0])


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_valid_temporary_code_with_valid_social_type(codes: list[str]):
    fixture = FixtureFactory.create({".": codes})

    await SimpleSocialAuthTokenRepository().readByTemporaryCode(TemporaryCode(codes[0]), ".")

    assert (set(fixture.codes["."]) & fixture.sources.source(".").codes) == fixture.sources.source(".").codes and len(
        list(fixture.sources.source(".").codes)
    ) + 1 == len(fixture.codes["."])


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_use_the_same_temporary_code_twice(codes: list[str]):
    FixtureFactory.create({".": codes})

    await SimpleSocialAuthTokenRepository().readByTemporaryCode(TemporaryCode(codes[0]), ".")

    with pytest.raises(InvalidTemporaryCodeError):
        await SimpleSocialAuthTokenRepository().readByTemporaryCode(TemporaryCode(codes[0]), ".")
