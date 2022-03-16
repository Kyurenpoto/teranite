from typing import NamedTuple

from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user_info import GithubUserInfo


class GithubIssueTokenRequest(GithubTemporaryCode):
    pass


class GithubAccessUserInfoRequest(GithubAuthToken):
    pass


class GithubUserExistanceRequest(GithubUserInfo):
    pass


class GithubCreateUserRequest(NamedTuple):
    userInfo: GithubUserInfo
    authToken: GithubAuthToken


class GithubUpdateUserAuthTokenRequest(NamedTuple):
    userInfo: GithubUserInfo
    authToken: GithubAuthToken


class GithubLoginWithoutTokenRequest(GithubTemporaryCode):
    pass
