from adaptor.mediator.temporary_code import TemporaryCode
from adaptor.mediator.token_presenter import TokenPresenter
from adaptor.mediator.token_viewmodel import TokenViewModel
from entity.github_temporary_code import GithubTemporaryCode
from usecase.github_login import GithubLoginWithoutToken


class TokenController:
    def __init__(self, viewModel: TokenViewModel):
        self.presenter = TokenPresenter(viewModel)
        self.githubUsecase = GithubLoginWithoutToken(self.presenter)

    async def execute(self, code: TemporaryCode, sns_type: str):
        try:
            if sns_type == "github":
                await self.githubUsecase.login(GithubTemporaryCode(code.code))
            else:
                await self.presenter.presentInvalidSnsType()
        except RuntimeError as e:
            print(e)
            await self.presenter.presentUnknown()
