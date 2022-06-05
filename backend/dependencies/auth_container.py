from adaptor.datasource.github_authtoken_api_datasource import GithubAuthTokenAPIDataSource
from adaptor.datasource.github_user_db_datasource import GithubUserDBDataSource
from adaptor.datasource.github_userinfo_api_datasource import GithubUserInfoAPIDataSource
from adaptor.mediator.updatable_token_viewmodel import UpdatableTokenViewModel
from adaptor.mediator.token_controller import TokenController
from adaptor.mediator.token_presenter import TokenPresenter
from adaptor.repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository
from adaptor.repository.github_user_simple_repository import GithubUserSimpleRepository
from adaptor.repository.github_userinfo_simple_repository import GithubUserInfoSimpleRepository
from database import DB
from usecase.github_login import GithubLoginWithTemporaryCode

from dependencies.dependency import Provider, TypeValue


class AuthContainer:
    def __init__(
        self,
        dependencies={
            "github-config": TypeValue(
                {
                    "client-id": "",
                    "client-secret": "",
                },
            ),
            "db": DB,
            "auth-token-source": GithubAuthTokenAPIDataSource,
            "user-info-source": GithubUserInfoAPIDataSource,
            "user-source": GithubUserDBDataSource,
            "auth-token-repo": GithubAuthTokenSimpleRepository,
            "user-info-repo": GithubUserInfoSimpleRepository,
            "user-repo": GithubUserSimpleRepository,
            "github-login-with-temporary-code": GithubLoginWithTemporaryCode,
            "token-viewmodel": UpdatableTokenViewModel,
            "token-presenter": TokenPresenter,
            "token-controller": TokenController,
        },
    ):
        self.provider = Provider()
        self.provider.wire(dependencies)

    def __call__(self):
        return self.provider
