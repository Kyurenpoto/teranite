from entity.auth_token import UserAuthToken


class TokenJsonEncoder:
    @classmethod
    def from_token(cls, token: UserAuthToken) -> dict:
        return {
            "has_account": True,
            "access_token": token.accessToken,
            "refresh_token": token.refreshToken,
        }
