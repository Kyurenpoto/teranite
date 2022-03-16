from entity.auth_token import UserAuthToken


class TokenJsonEncoder:
    def from_token(self, token: UserAuthToken) -> dict:
        return {
            "has_account": True,
            "access_token": token.accessToken,
            "refresh_token": token.refreshToken,
        }
