from typing import NamedTuple

import pytest
from adaptor.mediator.login_presenter import FakePresenter
from adaptor.repository.social_auth_token_repository import FakeSocialAuthTokenRepository
from adaptor.repository.user_auth_token_repository import FakeUserAuthTokenRepository
from adaptor.repository.user_email_repository import FakeUserEmailRepository
from dependencies.login_container import LoginContainer
from dependencies.dependency import provider
from entity.auth_token import FakeOwnAuthTokenGenerator, OwnAuthToken, SocialAuthToken
from entity.raw_datetime import FakeRawDatetime, RawDatetime
from entity.temporary_code import TemporaryCode
from entity.user_auth_token import UserAuthToken, UserAuthTokenBuilder
from hypothesis import given, strategies

from usecase.login import LoginWithAuthToken, LoginWithTemporaryCode


class Fixture(NamedTuple):
    codes: list[str]
    users: dict[str, UserAuthToken]
    socialAuthTokenRepo: FakeSocialAuthTokenRepository
    userAuthTokenRepo: FakeUserAuthTokenRepository


class FixtureFactory:
    @classmethod
    def create(cls, codes: list[str] = [], users: dict[str, UserAuthToken] = {}):
        provider.wire(
            {
                "login": LoginContainer(
                    {
                        "social-auth-token-repo": FakeSocialAuthTokenRepository,
                        "user-email-repo": FakeUserEmailRepository,
                        "user-auth-token-repo": FakeUserAuthTokenRepository,
                        "own-auth-token-generator": FakeOwnAuthTokenGenerator,
                        "login-presenter": FakePresenter,
                    }
                )
            }
        )

        fixture = Fixture(
            codes,
            users,
            provider["login"]["social-auth-token-repo"],
            provider["login"]["user-auth-token-repo"],
        )

        fixture.socialAuthTokenRepo.codes = set(fixture.codes)
        fixture.userAuthTokenRepo.users = {k: v.copy() for k, v in fixture.users.items()}

        return fixture

    @classmethod
    def createFromEmails(cls, emails: list[str] = []):
        return FixtureFactory.create(
            users={
                x: UserAuthTokenBuilder(x)
                .fillOwnAuthTokenWithExpireDatetime(
                    OwnAuthToken(f"access@{x}@access@{x}", f"refresh@{x}@refresh@{x}"), RawDatetime("")
                )
                .fillSocialAuthTokenWithSocialType(SocialAuthToken(f"access@{x}", f"refresh@{x}"), "")
                .build()
                for x in emails
            }
        )


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_invalid_temporary_code(codes: list[str]):
    FixtureFactory.create(codes=codes[1:])

    with pytest.raises(RuntimeError) as e:
        await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    assert e.value.args[0] == "invalid temporary code"


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_valid_temporary_code_without_generate_own_auth_token(codes: list[str]):
    fixture = FixtureFactory.create(
        codes=codes,
        users={
            f"email@{codes[0]}": UserAuthTokenBuilder(f"email@{codes[0]}")
            .fillOwnAuthTokenWithExpireDatetime(
                OwnAuthToken(f"access@{codes[0]}@access@{codes[0]}", f"refresh@{codes[0]}@refresh@{codes[0]}"),
                RawDatetime(""),
            )
            .fillSocialAuthTokenWithSocialType(SocialAuthToken(f"access@{codes[0]}", f"refresh@{codes[0]}"), "")
            .build()
        },
    )

    await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    presenter: FakePresenter = provider["login"]["login-presenter"]

    assert presenter.ownAuthToken == fixture.users[f"email@{codes[0]}"].ownAuthToken
    assert fixture.users == fixture.userAuthTokenRepo.users
    assert (set(fixture.codes) & fixture.socialAuthTokenRepo.codes) == fixture.socialAuthTokenRepo.codes and len(
        fixture.codes
    ) == len(list(fixture.socialAuthTokenRepo.codes)) + 1


@pytest.mark.asyncio
@given(strategies.lists(strategies.text(), min_size=1, unique=True))
async def test_valid_temporary_code_with_generate_own_auth_token(codes: list[str]):
    fixture = FixtureFactory.create(codes=codes)

    await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    assert f"email@{codes[0]}@" not in fixture.users
    assert len(list(set(fixture.users.keys()) & set(fixture.userAuthTokenRepo.users.keys()))) == len(
        fixture.users
    ) and len(fixture.users) + 1 == len(fixture.userAuthTokenRepo.users)
    assert (set(fixture.codes) & fixture.socialAuthTokenRepo.codes) == fixture.socialAuthTokenRepo.codes and len(
        fixture.codes
    ) == len(list(fixture.socialAuthTokenRepo.codes)) + 1


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_invalid_email(emails: list[str]):
    fixture = FixtureFactory.createFromEmails(emails[1:])

    with pytest.raises(RuntimeError) as e:
        await LoginWithAuthToken().login(emails[0], OwnAuthToken("", ""))

    assert e.value.args[0] == "invalid email"


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_invalid_own_auth_token(emails: list[str]):
    FixtureFactory.createFromEmails(emails)

    with pytest.raises(RuntimeError) as e:
        await LoginWithAuthToken().login(emails[0], OwnAuthToken("", ""))

    assert e.value.args[0] == "invalid own auth token"


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_not_update_own_auth_token(emails: list[str]):
    fixture = FixtureFactory.createFromEmails(emails)
    fixture.users[emails[0]].expireDatetime = FakeRawDatetime("")
    fixture.userAuthTokenRepo.users[emails[0]].expireDatetime = FakeRawDatetime("")

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]].ownAuthToken)

    presenter: FakePresenter = provider["login"]["login-presenter"]

    assert (
        presenter.ownAuthToken == fixture.users[emails[0]].ownAuthToken
        and fixture.users[emails[0]].expireDatetime == fixture.userAuthTokenRepo.users[emails[0]].expireDatetime
    )
    assert fixture.users == fixture.userAuthTokenRepo.users
    assert set(fixture.codes) == fixture.socialAuthTokenRepo.codes


@pytest.mark.asyncio
@given(strategies.lists(strategies.emails(), min_size=1, unique=True))
async def test_update_own_auth_token(emails: list[str]):
    fixture = FixtureFactory.createFromEmails(emails)
    fixture.users[emails[0]].expireDatetime = FakeRawDatetime("-")
    fixture.userAuthTokenRepo.users[emails[0]].expireDatetime = FakeRawDatetime("-")

    print(fixture.users[emails[0]].ownAuthToken)

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]].ownAuthToken)

    presenter: FakePresenter = provider["login"]["login-presenter"]

    print(fixture.users[emails[0]].ownAuthToken)

    assert (
        presenter.ownAuthToken != fixture.users[emails[0]].ownAuthToken
        and fixture.users[emails[0]].expireDatetime != fixture.userAuthTokenRepo.users[emails[0]].expireDatetime
    )
    assert dict(filter(lambda x: x[0] != emails[0], fixture.users.items())) == dict(
        filter(lambda x: x[0] != emails[0], fixture.userAuthTokenRepo.users.items())
    )
    assert set(fixture.codes) == fixture.socialAuthTokenRepo.codes
