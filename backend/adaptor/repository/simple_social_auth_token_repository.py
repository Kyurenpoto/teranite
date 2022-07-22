from adaptor.repository.social_auth_token_repository import SocialAuthTokenRepository
from dependencies.dependency import provider
from entity.auth_token import SocialAuthToken
from entity.temporary_code import TemporaryCode


class SimpleSocialAuthTokenRepository(SocialAuthTokenRepository):
    def __init__(self):
        self.datasources = provider["login"]["social-auth-token-source-collection"]

    async def readByTemporaryCode(self, code: TemporaryCode, socialType: str) -> SocialAuthToken:
        return await self.datasources.source(socialType).readByTemporaryCode(code)
