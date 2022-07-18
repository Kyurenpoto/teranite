from typing import NamedTuple

import pytest
from adaptor.repository.simple_user_auth_token_repository import SimpleUserAuthTokenRepository
from adaptor.repository.user_auth_token_repository import InvalidEmailError
from dependencies.dependency import provider
from dependencies.login_container import LoginContainer
from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.raw_datetime import RawDatetime
from entity.user_auth_token import UserAuthToken, UserAuthTokenBuilder
from hypothesis import given, strategies


class FakeUserAuthTokenDataSource:
    def __init__(self):
        self.users = {}

    async def readByEmail(self, email: str) -> UserAuthToken:
        if email not in self.users:
            raise InvalidEmailError()

        return self.users[email]

    async def saveSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        if email not in self.users:
            self.users[email] = (
                UserAuthTokenBuilder(email).fillSocialAuthTokenWithSocialType(socialAuthToken, socialType).build()
            )
        else:
            self.users[email].socialAuthtoken = socialAuthToken
            self.users[email].socialType = socialType

    async def saveOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        if email not in self.users:
            self.users[email] = (
                UserAuthTokenBuilder(email).fillOwnAuthTokenWithExpireDatetime(ownAuthToken, RawDatetime("")).build()
            )
        else:
            self.users[email].ownAuthToken = ownAuthToken
            self.users[email].expireDatetime = RawDatetime("")


class Fixture(NamedTuple):
    users: dict[str, UserAuthToken]
    userAuthTokenSource: FakeUserAuthTokenDataSource


class FixtureFactory:
    @classmethod
    def usersFromEmails(cls, emails: list[str]):
        return {
            x: UserAuthTokenBuilder(x)
            .fillOwnAuthTokenWithExpireDatetime(
                OwnAuthToken(f"access@{x}@access@{x}", f"refresh@{x}@refresh@{x}"), RawDatetime("")
            )
            .fillSocialAuthTokenWithSocialType(SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
            .build()
            for x in emails
        }

    @classmethod
    def create(cls, emails: list[str] = []):
        provider.wire({"login": LoginContainer({"user-auth-token-source": FakeUserAuthTokenDataSource})})

        fixture = Fixture(
            FixtureFactory.usersFromEmails(emails),
            provider["login"]["user-auth-token-source"],
        )

        fixture.userAuthTokenSource.users = {k: v for k, v in fixture.users.items()}

        return fixture


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_read_user_auth_token(emails: list[str]):
    fixture = FixtureFactory.create(emails)

    userAuthToken = await SimpleUserAuthTokenRepository().readByEmail(emails[0])

    assert userAuthToken == fixture.users[emails[0]]
    assert fixture.users == fixture.userAuthTokenSource.users


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_read_user_auth_token_absent_email(emails: list[str]):
    FixtureFactory.create(emails[1:])

    with pytest.raises(InvalidEmailError):
        await SimpleUserAuthTokenRepository().readByEmail(emails[0])


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_save_social_auth_token(emails: list[str]):
    fixture = FixtureFactory.create(emails[1:])

    await SimpleUserAuthTokenRepository().saveSocialAuthTokenByEmail(
        emails[0], SocialAuthToken(f"access@{emails[0]}", f"refresh@{emails[0]}"), ""
    )

    assert (
        len(fixture.users) == len(fixture.userAuthTokenSource.users)
        and emails[0] in fixture.users
        and emails[0] in fixture.userAuthTokenSource.users
    )


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_save_social_auth_token_absent_email(emails: list[str]):
    fixture = FixtureFactory.create(emails[1:])

    await SimpleUserAuthTokenRepository().saveSocialAuthTokenByEmail(
        emails[0], SocialAuthToken(f"access@{emails[0]}", f"refresh@{emails[0]}"), ""
    )

    assert (
        len(fixture.users) + 1 == len(fixture.userAuthTokenSource.users)
        and emails[0] not in fixture.users
        and emails[0] in fixture.userAuthTokenSource.users
    )


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_save_own_auth_token(emails: list[str]):
    fixture = FixtureFactory.create(emails[1:])

    await SimpleUserAuthTokenRepository().saveOwnAuthTokenByEmail(
        emails[0], OwnAuthToken(f"access@{emails[0]}", f"refresh@{emails[0]}")
    )

    assert (
        len(fixture.users) == len(fixture.userAuthTokenSource.users)
        and emails[0] in fixture.users
        and emails[0] in fixture.userAuthTokenSource.users
    )


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_save_own_auth_token_absent_email(emails: list[str]):
    fixture = FixtureFactory.create(emails[1:])

    await SimpleUserAuthTokenRepository().saveOwnAuthTokenByEmail(
        emails[0], OwnAuthToken(f"access@{emails[0]}", f"refresh@{emails[0]}")
    )

    assert (
        len(fixture.users) + 1 == len(fixture.userAuthTokenSource.users)
        and emails[0] not in fixture.users
        and emails[0] in fixture.userAuthTokenSource.users
    )
