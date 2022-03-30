from abc import ABC, abstractmethod


class GithubAuthTokenDataSource(ABC):
    @abstractmethod
    async def createAuthToken(self, code: str) -> dict:
        pass
