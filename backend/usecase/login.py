from dependencies.dependency import provider
from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.temporary_code import TemporaryCode

from usecase.login_port import (
    LoginWithAuthTokenInputPort,
    LoginWithAuthTokenOutputPort,
    LoginWithTemporaryCodeInputPort,
    LoginWithTemporaryCodeOutputPort,
)


class IssueSocialServiceAuthToken:
    async def issue(self, temporaryCode: TemporaryCode, socialType: str) -> SocialAuthToken:
        return SocialAuthToken("", "")


class GenerateOwnAuthToken:
    async def generate(self, email: str, socialAuthToken: SocialAuthToken) -> OwnAuthToken:
        return OwnAuthToken("", "")


class ValidateOwnAuthToken:
    async def validate(self, email: str, ownAuthToken: OwnAuthToken) -> OwnAuthToken:
        return OwnAuthToken("", "")


class AccessUserEmail:
    async def access(self, socialAuthToken, socialType):
class UpdateUserAuthToken:
    async def updateSocialAuthToken(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        pass

    async def updateOwnAuthToken(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        pass


    async def updateOwnAuthToken(self, email, ownAuthToken):
        pass
class AccessUserEmail:
    async def access(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        return ""


class LoginWithTemporaryCode(LoginWithTemporaryCodeInputPort):
    def __init__(self):
        self.outputPort: LoginWithTemporaryCodeOutputPort = provider["auth"]["token-presenter"]

    async def login(self, temporaryCode: TemporaryCode, socialType: str) -> None:
        socialAuthToken = await IssueSocialServiceAuthToken().issue(temporaryCode, socialType)
        email = await AccessUserEmail().access(socialAuthToken, socialType)
        ownAuthToken = await GenerateOwnAuthToken().generate(email, socialAuthToken)

        await UpdateUserAuthToken().updateSocialAuthToken(email, socialAuthToken, socialType)
        await UpdateUserAuthToken().updateOwnAuthToken(email, ownAuthToken)

        await self.outputPort.present(ownAuthToken)


class LoginWithAuthToken(LoginWithAuthTokenInputPort):
    def __init__(self):
        self.outputPort: LoginWithAuthTokenOutputPort = provider["auth"]["token-presenter"]

    async def login(self, email, ownAuthToken: OwnAuthToken) -> None:
        newOwnAuthToken = await ValidateOwnAuthToken().validate(email, ownAuthToken)

        await UpdateUserAuthToken().updateOwnAuthToken(email, newOwnAuthToken)

        await self.outputPort.present(newOwnAuthToken)
