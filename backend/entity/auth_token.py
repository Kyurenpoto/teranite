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


class OwnAuthTokenGenerator:
    async def generate(self, email: str, authToken: AuthToken) -> OwnAuthToken:
        return OwnAuthToken("", "")


class FakeOwnAuthTokenGenerator(OwnAuthTokenGenerator):
    async def generate(self, email: str, authToken: AuthToken) -> OwnAuthToken:
        return OwnAuthToken(
            f"access@{email[6:]}@{authToken.accessToken}", f"refresh@{email[6:]}@{authToken.refreshToken}"
        )
