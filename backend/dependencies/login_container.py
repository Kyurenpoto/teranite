from adaptor.mediator.login_presenter import FakePresenter
from adaptor.repository.social_auth_token_repository import FakeSocialAuthTokenRepository
from adaptor.repository.user_auth_token_repository import FakeUserAuthTokenRepository
from adaptor.repository.user_email_repository import FakeUserEmailRepository
from entity.auth_token import FakeOwnAuthTokenGenerator

from dependencies.dependency import Provider


class LoginContainer:
    def __init__(
        self,
        dependencies={
            "social-auth-token-repo": FakeSocialAuthTokenRepository,
            "user-email-repo": FakeUserEmailRepository,
            "user-auth-token-repo": FakeUserAuthTokenRepository,
            "own-auth-token-generator": FakeOwnAuthTokenGenerator,
            "login-presenter": FakePresenter,
        },
    ):
        self.provider = Provider()
        self.provider.wire(dependencies)

    def __call__(self):
        return self.provider
