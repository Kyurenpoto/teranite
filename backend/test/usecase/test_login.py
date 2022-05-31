from typing import NamedTuple

import pytest
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import AuthToken, OwnAuthToken, SocialAuthToken
from entity.temporary_code import TemporaryCode
from hypothesis import given, strategies

from usecase.login import LoginWithAuthToken, LoginWithTemporaryCode
from usecase.login_port import LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort


class FakeSocialAuthTokenRepository:
    def __init__(self):
        self.codes = set()

    async def readByTemporaryCode(self, code: TemporaryCode, socialType: str) -> SocialAuthToken:
        if str(code) not in self.codes:
            raise RuntimeError("invalid temporary code")

        self.codes.remove(code)

        return SocialAuthToken(f"access@{code}", f"refresh@{code}")


class FakeUserEmailRepository:
    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        return f"email@{socialAuthToken.accessToken[7:]}"


class UserAuthToken:
    email: str
    ownAuthToken: OwnAuthToken
    socialAuthToken: SocialAuthToken
    socialType: str
    expireDatetime: str

    def __init__(
        self,
        email: str,
        ownAuthToken: OwnAuthToken,
        expireDatetime: str,
        socialAuthToken: SocialAuthToken,
        socialType: str,
    ):
        self.email = email
        self.ownAuthToken = ownAuthToken
        self.expireDatetime = expireDatetime
        self.socialAuthToken = socialAuthToken
        self.socialType = socialType

    def __eq__(self, other) -> bool:
        return (
            self.email == other.email
            and self.ownAuthToken == other.ownAuthToken
            and self.expireDatetime == other.expireDatetime
            and self.socialAuthToken == other.socialAuthToken
            and self.socialType == other.socialType
        )

    def copy(self):
        return UserAuthToken(self.email, self.ownAuthToken, self.expireDatetime, self.socialAuthToken, self.socialType)


class UserAuthTokenBuilder:
    email: str
    ownAuthToken: OwnAuthToken
    expireDatetime: str
    socialAuthToken: SocialAuthToken
    socialType: str

    def __init__(self, email):
        self.email = email
        self.ownAuthToken = OwnAuthToken("", "")
        self.socialAuthToken = SocialAuthToken("", "")
        self.socialType = ""
        self.expireDatetime = ""

    def fillOwnAuthTokenWithExpireDatetime(self, ownAuthToken: OwnAuthToken, expireDatetime: str):
        self.ownAuthToken = ownAuthToken
        self.expireDatetime = expireDatetime

        return self

    def fillSocialAuthTokenWithSocialType(self, socialAuthToken: SocialAuthToken, socialType: str):
        self.socialAuthToken = socialAuthToken
        self.socialType = socialType

        return self

    def build(self) -> UserAuthToken:
        return UserAuthToken(self.email, self.ownAuthToken, self.expireDatetime, self.socialAuthToken, self.socialType)


class FakeUserAuthTokenRepository:
    def __init__(self):
        self.users = {}

    async def readByEmail(self, email: str) -> UserAuthToken:
        if email not in self.users:
            raise RuntimeError("invalid email")

        return self.users[email]

    async def updateSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        if email not in self.users:
            self.users[email] = (
                UserAuthTokenBuilder(email).fillSocialAuthTokenWithSocialType(socialAuthToken, socialType).build()
            )
        else:
            self.users[email].socialAuthtoken = socialAuthToken
            self.users[email].socialType = socialType

    async def updateOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        if email not in self.users:
            self.users[email] = UserAuthTokenBuilder(email).fillOwnAuthTokenWithExpireDatetime(ownAuthToken, "").build()
        else:
            self.users[email].ownAuthToken = ownAuthToken
            self.users[email].expireDatetime = ""


class FakeOwnAuthTokenGenerator:
    async def generate(self, email: str, authToken: AuthToken) -> OwnAuthToken:
        return OwnAuthToken(
            f"access@{email[6:]}@{authToken.accessToken}", f"refresh@{email[6:]}@{authToken.refreshToken}"
        )


class FakePresenter(LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort):
    async def present(self, ownAuthToken: OwnAuthToken):
        self.ownAuthToken = ownAuthToken


class FakeDatetimeValidator:
    async def validateExpiration(self, expireDatetime: str) -> bool:
        return expireDatetime == ""


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
                "auth": AuthContainer(
                    {
                        "social-auth-token-repo": FakeSocialAuthTokenRepository,
                        "user-email-repo": FakeUserEmailRepository,
                        "user-auth-token-repo": FakeUserAuthTokenRepository,
                        "own-auth-token-generator": FakeOwnAuthTokenGenerator,
                        "token-presenter": FakePresenter,
                        "datetime-validator": FakeDatetimeValidator,
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
        fixture.userAuthTokenRepo.users = {k: v.copy() for k, v in fixture.users.items()}

        return fixture

    @classmethod
    def createFromEmails(cls, emails: list[str] = []):
        return FixtureFactory.create(
            users={
                x: UserAuthTokenBuilder(x)
                .fillOwnAuthTokenWithExpireDatetime(
                    OwnAuthToken(f"access@{x}@access@{x}", f"refresh@{x}@refresh@{x}"), ""
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
                OwnAuthToken(f"access@{codes[0]}@access@{codes[0]}", f"refresh@{codes[0]}@refresh@{codes[0]}"), ""
            )
            .fillSocialAuthTokenWithSocialType(SocialAuthToken(f"access@{codes[0]}", f"refresh@{codes[0]}"), "")
            .build()
        },
    )

    await LoginWithTemporaryCode().login(TemporaryCode(codes[0]), "")

    presenter: FakePresenter = provider["auth"]["token-presenter"]

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

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]].ownAuthToken)

    presenter: FakePresenter = provider["auth"]["token-presenter"]

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
    fixture.users[emails[0]].expireDatetime = "-"
    fixture.userAuthTokenRepo.users[emails[0]].expireDatetime = "-"

    print(fixture.users[emails[0]].ownAuthToken)

    await LoginWithAuthToken().login(emails[0], fixture.users[emails[0]].ownAuthToken)

    presenter: FakePresenter = provider["auth"]["token-presenter"]

    print(fixture.users[emails[0]].ownAuthToken)

    assert (
        presenter.ownAuthToken != fixture.users[emails[0]].ownAuthToken
        and fixture.users[emails[0]].expireDatetime != fixture.userAuthTokenRepo.users[emails[0]].expireDatetime
    )
    assert dict(filter(lambda x: x[0] != emails[0], fixture.users.items())) == dict(
        filter(lambda x: x[0] != emails[0], fixture.userAuthTokenRepo.users.items())
    )
    assert set(fixture.codes) == fixture.socialAuthTokenRepo.codes
