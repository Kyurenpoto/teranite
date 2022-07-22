from adaptor.repository.user_email_repository import UserEmailRepository
from dependencies.dependency import provider
from entity.auth_token import SocialAuthToken


class SimpleUserEmailRepository(UserEmailRepository):
    def __init__(self):
        self.datasources = provider["login"]["user-email-source-collection"]

    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        return await self.datasources.source(socialType).readBySocialAuthToken(socialAuthToken)
