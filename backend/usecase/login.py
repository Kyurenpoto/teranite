from adaptor.repository.social_auth_token_repository import SocialAuthTokenRepository
from adaptor.repository.user_auth_token_repository import UserAuthTokenRepository
from adaptor.repository.user_email_repository import UserEmailRepository
from dependencies.dependency import provider
from entity.auth_token import AuthToken, OwnAuthToken, SocialAuthToken, OwnAuthTokenGenerator
from entity.temporary_code import TemporaryCode

from usecase.login_port import (
    LoginWithAuthTokenInputPort,
    LoginWithAuthTokenOutputPort,
    LoginWithTemporaryCodeInputPort,
    LoginWithTemporaryCodeOutputPort,
)


class InvalidOwnAuthTokenError(RuntimeError):
    def __init__(self):
        super().__init__("invalid own auth token")


class IssueSocialServiceAuthToken:
    def __init__(self):
        self.repository: SocialAuthTokenRepository = provider["login"]["social-auth-token-repo"]

    async def issue(self, temporaryCode: TemporaryCode, socialType: str) -> SocialAuthToken:
        return await self.repository.readByTemporaryCode(temporaryCode, socialType)


class AccessUserEmail:
    def __init__(self):
        self.repository: UserEmailRepository = provider["login"]["user-email-repo"]

    async def access(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        return await self.repository.readBySocialAuthToken(socialAuthToken, socialType)


class GenerateOwnAuthToken:
    def __init__(self):
        self.repository: UserAuthTokenRepository = provider["login"]["user-auth-token-repo"]
        self.generator: OwnAuthTokenGenerator = provider["login"]["own-auth-token-generator"]

    async def generateFromSocialAuthToken(self, email: str, socialAuthToken: SocialAuthToken) -> OwnAuthToken:
        return await self.generateToken(email, socialAuthToken)

    async def generateFromOwnAuthToken(self, email: str, ownAuthToken: OwnAuthToken) -> OwnAuthToken:
        userAuthToken = await self.repository.readByEmail(email)

        if userAuthToken.ownAuthToken != ownAuthToken:
            raise InvalidOwnAuthTokenError()

        return ownAuthToken if userAuthToken.expireDatetime.expired() else await self.generateToken(email, ownAuthToken)

    async def generateToken(self, email: str, authToken: AuthToken) -> OwnAuthToken:
        ownAuthToken = await self.generator.generate(email, authToken)

        return ownAuthToken


class SaveUserAuthToken:
    def __init__(self):
        self.repository: UserAuthTokenRepository = provider["login"]["user-auth-token-repo"]

    async def saveSocialAuthToken(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        await self.repository.saveSocialAuthTokenByEmail(email, socialAuthToken, socialType)

    async def saveOwnAuthToken(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        await self.repository.saveOwnAuthTokenByEmail(email, ownAuthToken)


class LoginWithTemporaryCode(LoginWithTemporaryCodeInputPort):
    def __init__(self):
        self.outputPort: LoginWithTemporaryCodeOutputPort = provider["login"]["login-presenter"]

    async def login(self, temporaryCode: TemporaryCode, socialType: str) -> None:
        socialAuthToken = await IssueSocialServiceAuthToken().issue(temporaryCode, socialType)
        email = await AccessUserEmail().access(socialAuthToken, socialType)
        ownAuthToken = await GenerateOwnAuthToken().generateFromSocialAuthToken(email, socialAuthToken)

        await SaveUserAuthToken().saveSocialAuthToken(email, socialAuthToken, socialType)
        await SaveUserAuthToken().saveOwnAuthToken(email, ownAuthToken)

        await self.outputPort.present(ownAuthToken)


class LoginWithAuthToken(LoginWithAuthTokenInputPort):
    def __init__(self):
        self.outputPort: LoginWithAuthTokenOutputPort = provider["login"]["login-presenter"]

    async def login(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        newOwnAuthToken = await GenerateOwnAuthToken().generateFromOwnAuthToken(email, ownAuthToken)

        await SaveUserAuthToken().saveOwnAuthToken(email, newOwnAuthToken)

        await self.outputPort.present(newOwnAuthToken)
