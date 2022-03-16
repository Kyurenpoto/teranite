from typing import NamedTuple

from entity.auth_token import GithubAuthToken, UserAuthToken
from entity.github_user_info import GithubUserInfo


class GithubIssueTokenResponse(GithubAuthToken):
    pass


class GithubAccessUserInfoResponse(GithubUserInfo):
    pass


class GithubUserExistanceResponse(NamedTuple):
    result: bool


class GithubLoginWithoutTokenResponse(UserAuthToken):
    pass
