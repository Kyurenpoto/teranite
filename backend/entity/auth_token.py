from typing import NamedTuple


class AuthToken(NamedTuple):
    access_token: str
    refresh_token: str


class UserAuthToken(AuthToken):
    pass


class GithubAuthToken(AuthToken):
    pass
