from abc import ABC, abstractmethod
from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.user_auth_token import UserAuthToken, UserAuthTokenBuilder
from entity.raw_datetime import RawDatetime


class InvalidEmailError(RuntimeError):
    def __init__(self):
        super().__init__("invalid email")


class UserAuthTokenRepository(ABC):
    @abstractmethod
    async def readByEmail(self, email: str) -> UserAuthToken:
        pass

    @abstractmethod
    async def saveSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        pass

    @abstractmethod
    async def saveOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        pass


class FakeUserAuthTokenRepository(UserAuthTokenRepository):
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
