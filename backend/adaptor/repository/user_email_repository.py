from abc import ABC, abstractmethod
from entity.auth_token import SocialAuthToken


class UserEmailRepository(ABC):
    @abstractmethod
    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        pass


class FakeUserEmailRepository(UserEmailRepository):
    async def readBySocialAuthToken(self, socialAuthToken: SocialAuthToken, socialType: str) -> str:
        return f"email@{socialAuthToken.accessToken[7:]}"
