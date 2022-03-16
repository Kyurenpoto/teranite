from typing import NamedTuple


class AuthToken(NamedTuple):
    accessToken: str
    refreshToken: str


class UserAuthToken(AuthToken):
    pass


class GithubAuthToken(AuthToken):
    pass
