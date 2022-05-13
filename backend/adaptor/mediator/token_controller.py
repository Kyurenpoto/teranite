from adaptor.mediator.temporary_code import TemporaryCode
from adaptor.mediator.token_presenter import TokenPresenter
from dependencies.dependency import provider
from entity.github_temporary_code import GithubTemporaryCode
from usecase.github_login import GithubLoginWithTemporaryCode


class TokenController:
    def presenter(self) -> TokenPresenter:
        return provider["auth"]["token-presenter"]

    def githubUsecase(self) -> GithubLoginWithTemporaryCode:
        return provider["auth"]["github-login-with-temporary-code"]

    async def execute(self, code: TemporaryCode, sns_type: str):
        try:
            if sns_type == "github":
                await self.githubUsecase().login(GithubTemporaryCode(code.code))
            else:
                await self.presenter().presentInvalidSnsType()
        except RuntimeError as e:
            print(e)
            await self.presenter().presentUnknown()
