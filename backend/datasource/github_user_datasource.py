from abc import ABC, abstractmethod

from database import models


class GithubUserDataSource(ABC):
    @abstractmethod
    async def readUser(self, email: str) -> models.User | None:
        pass

    @abstractmethod
    async def createUser(self, email: str, accessToken: str, refreshToken: str):
        pass

    @abstractmethod
    async def updateUser(self, email: str, accessToken: str, refreshToken: str):
        pass
