from abc import ABC, abstractmethod


class GithubUserInfoDataSource(ABC):
    @abstractmethod
    async def readUserInfo(self, accessToken: str) -> dict:
        pass
