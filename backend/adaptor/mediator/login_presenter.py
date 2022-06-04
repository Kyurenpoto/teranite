from entity.auth_token import OwnAuthToken

from usecase.login_port import LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort


class LoginPresenter(LoginWithAuthTokenOutputPort, LoginWithTemporaryCodeOutputPort):
    async def present(self, ownAuthToken: OwnAuthToken):
        pass


class FakePresenter(LoginPresenter):
    async def present(self, ownAuthToken: OwnAuthToken):
        self.ownAuthToken = ownAuthToken
