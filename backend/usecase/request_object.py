from typing import NamedTuple

from ..entity.auth_token import GithubAuthToken
from ..entity.github_temporary_code import GithubTemporaryCode
from ..entity.user_info import UserInfo


class GithubIssueTokenRequest(GithubTemporaryCode):
    pass


class GithubAccessUserInfoRequest(NamedTuple):
    authToken: GithubAuthToken
    userInfo: UserInfo


class GithubUpdateUserAuthTokenRequest(NamedTuple):
    userInfo: UserInfo
    authToken: GithubAuthToken


class GithubCreateUserRequest(NamedTuple):
    userInfo: UserInfo
    authToken: GithubAuthToken


class GithubLoginWithoutTokenRequest(GithubTemporaryCode):
    pass
