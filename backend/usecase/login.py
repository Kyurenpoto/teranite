from dependencies.dependency import provider

from usecase.login_port import (
    LoginWithAuthTokenInputPort,
    LoginWithAuthTokenOutputPort,
    LoginWithTemporaryCodeInputPort,
    LoginWithTemporaryCodeOutputPort,
)


class IssueSocialServiceAuthToken:
    async def issue(self, temporaryCode, socialType):
        pass


class GenerateOwnAuthToken:
    async def generate(self, email, socialAuthToken):
        pass


class ValidateOwnAuthToken:
    async def validate(self, email, ownAuthToken):
        pass


class AccessUserEmail:
    async def access(self, socialAuthToken, socialType):
        pass


class UpdateUserAuthToken:
    async def updateSocialAuthToken(self, email, socialAuthToken, socialType):
        pass

    async def updateOwnAuthToken(self, email, ownAuthToken):
        pass


class LoginWithTemporaryCode(LoginWithTemporaryCodeInputPort):
    def __init__(self):
        self.outputPort: LoginWithTemporaryCodeOutputPort = provider["auth"]["token-presenter"]

    async def login(self, temporaryCode, socialType):
        socialAuthToken = await IssueSocialServiceAuthToken().issue(temporaryCode, socialType)
        email = await AccessUserEmail().access(socialAuthToken, socialType)
        ownAuthToken = await GenerateOwnAuthToken().generate(email, socialAuthToken)

        await UpdateUserAuthToken().updateSocialAuthToken(email, socialAuthToken, socialType)
        await UpdateUserAuthToken().updateOwnAuthToken(email, ownAuthToken)

        await self.outputPort.present(ownAuthToken)


class LoginWithAuthToken(LoginWithAuthTokenInputPort):
    def __init__(self):
        self.outputPort: LoginWithAuthTokenOutputPort = provider["auth"]["token-presenter"]

    async def login(self, email, ownAuthToken):
        newOwnAuthToken = await ValidateOwnAuthToken().validate(email, ownAuthToken)

        await UpdateUserAuthToken().updateOwnAuthToken(email, newOwnAuthToken)

        await self.outputPort.present(newOwnAuthToken)
