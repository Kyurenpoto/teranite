from typing import NamedTuple

from ..entity.auth_token import GithubAuthToken, UserAuthToken
from ..entity.user_info import UserInfo


class GithubIssueTokenSuccessResponse(GithubAuthToken):
    pass


class GithubIssueTokenFailResponse(NamedTuple):
    failure_type: str
    message: str


class GithubAccessUserInfoSuccessResponse(UserInfo):
    pass


class GithubAccessUserInfoFailResponse(NamedTuple):
    failure_type: str
    message: str


class GithubCreateUserSuccessResponse(NamedTuple):
    pass


class GithubCreateUserFailResponse(NamedTuple):
    failure_type: str
    message: str


class GithubUpdateUserAuthTokenSuccessResponse(NamedTuple):
    pass


class GithubUpdateUserAuthTokenFailResponse(NamedTuple):
    failure_type: str
    message: str


class GithubLoginWithoutTokenSuccessResponse(UserAuthToken):
    pass


class GithubLoginWithoutTokenFailResponse(NamedTuple):
    failure_type: str
    message: str
