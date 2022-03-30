from entity.github_temporary_code import GithubTemporaryCode
from usecase.github_login import GithubLoginWithoutToken

from adaptor.temporary_code import TemporaryCode
from adaptor.token_presenter import TokenPresenter
from adaptor.token_viewmodel import TokenViewModel


class TokenController:
    def __init__(self, viewModel: TokenViewModel):
        self.presenter = TokenPresenter(viewModel)

    async def execute(self, code: TemporaryCode, sns_type: str):
        try:
            if sns_type == "github":
                await self.presenter.present(await GithubLoginWithoutToken().login(GithubTemporaryCode(code.code)))
            else:
                await self.presenter.presentInvalid()
        except RuntimeError as e:
            print(e)
