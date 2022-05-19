from typing import NamedTuple


class AuthToken(NamedTuple):
    accessToken: str
    refreshToken: str


class UserAuthToken(AuthToken):
    pass


class GithubAuthToken(AuthToken):
    pass


class OwnAuthToken(AuthToken):
    pass


class SocialAuthToken(AuthToken):
    pass
