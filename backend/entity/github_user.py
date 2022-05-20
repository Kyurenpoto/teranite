from typing import NamedTuple

from .auth_token import GithubAuthToken


class GithubUser(NamedTuple):
    email: str
    authToken: GithubAuthToken
