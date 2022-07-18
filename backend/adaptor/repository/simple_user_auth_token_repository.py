from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.user_auth_token import UserAuthToken

from adaptor.repository.user_auth_token_repository import UserAuthTokenRepository


class SimpleUserAuthTokenRepository(UserAuthTokenRepository):
    async def readByEmail(self, email: str) -> UserAuthToken:
        pass

    async def saveSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        pass

    async def saveOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        pass

