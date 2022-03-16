from typing import NamedTuple

from ..entity.auth_token import GithubAuthToken, UserAuthToken
from ..entity.github_temporary_code import GithubTemporaryCode
from ..entity.user_info import UserInfo
from .request_object import (
    GithubAccessUserInfoRequest,
    GithubCreateUserRequest,
    GithubIssueTokenRequest,
    GithubLoginWithoutTokenRequest,
    GithubUpdateUserAuthTokenRequest,
)
from .response_object import (
    GithubAccessUserInfoFailResponse,
    GithubAccessUserInfoSuccessResponse,
    GithubCreateUserFailResponse,
    GithubCreateUserSuccessResponse,
    GithubIssueTokenFailResponse,
    GithubIssueTokenSuccessResponse,
    GithubLoginWithoutTokenFailResponse,
    GithubLoginWithoutTokenSuccessResponse,
    GithubUpdateUserAuthTokenFailResponse,
    GithubUpdateUserAuthTokenSuccessResponse,
)


class GithubIssueToken(NamedTuple):
    async def issue(
        self, request: GithubIssueTokenRequest
    ) -> GithubIssueTokenSuccessResponse | GithubIssueTokenFailResponse:
        return GithubIssueTokenFailResponse("", "")


class GithubAccessUserInfo(NamedTuple):
    async def access(
        self, request: GithubAccessUserInfoRequest
    ) -> GithubAccessUserInfoSuccessResponse | GithubAccessUserInfoFailResponse:
        return GithubAccessUserInfoFailResponse("", "")


class GithubCreateUser(NamedTuple):
    async def create(
        self, request: GithubCreateUserRequest
    ) -> GithubCreateUserSuccessResponse | GithubCreateUserFailResponse:
        return GithubCreateUserFailResponse("", "")


class GithubUpdateUserAuthToken(NamedTuple):
    async def update(
        self, request: GithubUpdateUserAuthTokenRequest
    ) -> GithubUpdateUserAuthTokenSuccessResponse | GithubUpdateUserAuthTokenFailResponse:
        return GithubUpdateUserAuthTokenFailResponse("", "")


class GithubLoginWithoutToken(NamedTuple):
    issueToken: GithubIssueToken = GithubIssueToken()

    async def login(
        self, request: GithubLoginWithoutTokenRequest
    ) -> GithubLoginWithoutTokenSuccessResponse | GithubLoginWithoutTokenFailResponse:
        return GithubLoginWithoutTokenFailResponse("", "")
