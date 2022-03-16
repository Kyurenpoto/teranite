from abc import ABC, abstractmethod

from ..entity.auth_token import GithubAuthToken
from ..entity.github_user import GithubUser


class GithubUserRepository(ABC):
    @abstractmethod
    async def readByEmail(self, email: str) -> GithubUser | None:
        pass

    @abstractmethod
    async def create(self, user: GithubUser):
        pass

    @abstractmethod
    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        pass
