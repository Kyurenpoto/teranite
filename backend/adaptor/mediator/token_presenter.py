from adaptor.mediator.token_viewmodel import TokenViewModel
from entity.auth_token import UserAuthToken
from fastapi import status
from fastapi.responses import JSONResponse
from usecase.github_login_port import GithubLoginWithoutTokenOutputPort


class TokenPresenter(GithubLoginWithoutTokenOutputPort):
    def __init__(self, viewModel: TokenViewModel):
        self.viewModel = viewModel

    async def present(self, authToken: UserAuthToken):
        self.viewModel.response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "has_account": True,
                "access_token": str([authToken.accessToken]),
                "refresh_token": str([authToken.refreshToken]),
            },
        )

    async def presentInvalidSnsType(self):
        self.viewModel.response = JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    async def presentUnknown(self):
        self.viewModel.response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
