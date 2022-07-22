from adaptor.repository.user_auth_token_repository import InvalidEmailError, UserAuthTokenRepository
from dependencies.dependency import provider
from entity.auth_token import OwnAuthToken, SocialAuthToken
from entity.raw_datetime import RawDatetime
from entity.user_auth_token import UserAuthToken


class SimpleUserAuthTokenRepository(UserAuthTokenRepository):
    def __init__(self):
        self.datasource = provider["login"]["user-auth-token-source"]
        self.datatimeGenerator = provider["login"]["raw-datatime-gen"]

    async def readByEmail(self, email: str) -> UserAuthToken:
        return await self.datasource.readByEmail(email)

    async def saveSocialAuthTokenByEmail(self, email: str, socialAuthToken: SocialAuthToken, socialType: str) -> None:
        try:
            await self.readByEmail(email)

            await self.datasource.updateSocialAuthTokenByEmail(email, socialAuthToken, socialType)
        except InvalidEmailError:
            await self.datasource.createSocialAuthTokenByEmail(email, socialAuthToken, socialType)

    async def saveOwnAuthTokenByEmail(self, email: str, ownAuthToken: OwnAuthToken) -> None:
        try:
            await self.readByEmail(email)

            await self.datasource.updateOwnAuthTokenByEmail(email, ownAuthToken, await self.datatimeGenerator.now())
        except InvalidEmailError:
            await self.datasource.createOwnAuthTokenByEmail(email, ownAuthToken, await self.datatimeGenerator.now())
