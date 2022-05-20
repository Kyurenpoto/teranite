from typing import NamedTuple

import pytest
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.temporary_code import TemporaryCode
from hypothesis import given, strategies

from usecase.login import LoginWithAuthToken, LoginWithTemporaryCode
from usecase.login_port import LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort


class FakeSocialAuthTokenRepository:
    def __init__(self):
        self.codes = set()

    async def readByTemporaryCode(self, code: TemporaryCode) -> SocialAuthToken:
        if code not in self.codes:
            raise RuntimeError("invalid temporary code")

        self.codes.remove(code)

        return SocialAuthToken(f"access@{code}", f"refresh@{code}")


class FakeUserEmailRepository:
    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken, snsType: str) -> str:
        return f"{socialAuthToken.accessToken}@{snsType}"


class FakeUserAuthTokenRepository:
    def __init__(self):
        self.users = {}

    async def readByEmail(self, email: str) -> dict:
        if email not in self.users:
            raise RuntimeError("invalid email")

        return self.users[email]

    async def updateSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        self.users[email] = (
            OwnAuthToken("", "") if email in self.users else self.users[email][0],
            socialAuthToken,
            socialType,
        )

    async def updateOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        self.users[email] = (
            ownAuthToken,
            SocialAuthToken("", "") if email in self.users else self.users[email][1],
            "",
        )


class FakePresenter(LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort):
    async def present(self, ownAuthToken: OwnAuthToken):
        self.ownAuthToken = ownAuthToken


class Fixture(NamedTuple):
    codes: list[str]
    users: dict[str, tuple[OwnAuthToken, SocialAuthToken, str]]
    socialAuthTokenRepo: FakeSocialAuthTokenRepository
    userAuthTokenRepo: FakeUserAuthTokenRepository


class FixtureFactory:
    @classmethod
    def createWithTemporaryCodes(
        cls, codes: list[str] = [], users: dict[str, tuple[OwnAuthToken, SocialAuthToken, str]] = {}
    ):
        provider.wire(
            {
                "auth": AuthContainer(
                    {
                        "social-auth-token-repo": FakeSocialAuthTokenRepository,
                        "user-email-repo": FakeUserEmailRepository,
                        "user-auth-token-repo": FakeUserAuthTokenRepository,
                        "token-presenter": FakePresenter,
                    }
                )
            }
        )

        fixture = Fixture(
            codes,
            users,
            provider["auth"]["social-auth-token-repo"],
            provider["auth"]["user-auth-token-repo"],
        )

        fixture.socialAuthTokenRepo.codes = set(fixture.codes)
        fixture.userAuthTokenRepo.users = {**fixture.users}

        return fixture


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1))
async def test_invalid_temporary_code(codes: list[str]):
    FixtureFactory.createWithTemporaryCodes(codes=codes[1:])

    with pytest.raises(RuntimeError) as e:
        await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    assert e.value.args[0] == "invalid temporary code"


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1))
async def test_valid_temporary_code_without_generate_own_auth_token(codes: list[str]):
    fixture = FixtureFactory.createWithTemporaryCodes(
        codes=codes,
        users={
            f"access@{codes[0]}@": (
                OwnAuthToken(f"access@{codes[0]}", f"refresh@{codes[0]}"),
                SocialAuthToken(f"access@{codes[0]}", f"refresh@{codes[0]}"),
                "",
            )
        },
    )

    await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.ownAuthToken == fixture.users[f"access@{codes[0]}@"][0]
    assert fixture.users == fixture.userAuthTokenRepo.users
    assert (set(fixture.codes) & fixture.socialAuthTokenRepo.codes) == fixture.socialAuthTokenRepo.codes and len(
        fixture.codes
    ) == len(list(fixture.socialAuthTokenRepo.codes)) + 1


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1))
async def test_valid_temporary_code_with_generate_own_auth_token(codes: list[str]):
    fixture = FixtureFactory.createWithTemporaryCodes(codes=codes)

    await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.ownAuthToken == fixture.users[f"access@{codes[0]}@"][0]
    assert len(list(set(fixture.users.keys()) & set(fixture.userAuthTokenRepo.users.keys()))) == len(
        fixture.users
    ) and len(fixture.users) + 1 == len(fixture.userAuthTokenRepo.users)
    assert (set(fixture.codes) & fixture.socialAuthTokenRepo.codes) == fixture.socialAuthTokenRepo.codes and len(
        fixture.codes
    ) == len(list(fixture.socialAuthTokenRepo.codes)) + 1


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1))
async def test_invalid_email(emails: list[str]):
    FixtureFactory.createWithTemporaryCodes(
        users={
            x: (OwnAuthToken(f"access@{x}", f"refresh@{x}"), SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
            for x in emails[1:]
        }
    )

    with pytest.raises(RuntimeError) as e:
        await LoginWithAuthToken().login(emails[0], OwnAuthToken("", ""))

    assert e.value.args[0] == "invalid email"


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1))
async def test_invalid_own_auth_token(emails: list[str]):
    FixtureFactory.createWithTemporaryCodes(
        users={
            x: (OwnAuthToken(f"access@{x}", f"refresh@{x}"), SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
            for x in emails
        }
    )

    with pytest.raises(RuntimeError) as e:
        await LoginWithAuthToken().login(emails[0], OwnAuthToken("", ""))

    assert e.value.args[0] == "invalid own auth token"


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1))
async def test_not_update_own_auth_token(emails: list[str]):
    fixture = FixtureFactory.createWithTemporaryCodes(
        users={
            x: (OwnAuthToken(f"access@{x}", f"refresh@{x}"), SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
            for x in emails
        }
    )

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]][0])

    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.ownAuthToken == fixture.users[emails[0]][0]
    assert fixture.users == fixture.userAuthTokenRepo.users
    assert set(fixture.codes) == fixture.socialAuthTokenRepo.codes


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1))
async def test_update_own_auth_token(emails: list[str]):
    fixture = FixtureFactory.createWithTemporaryCodes(
        users={
            x: (OwnAuthToken(f"access@{x}", f"refresh@{x}"), SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
            for x in emails
        }
    )

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]][0])

    presenter: FakePresenter = provider["auth"]["token-presenter"]

    assert presenter.ownAuthToken != fixture.users[emails[0]][0]
    assert fixture.users != fixture.userAuthTokenRepo.users
    assert set(fixture.codes) == fixture.socialAuthTokenRepo.codes
