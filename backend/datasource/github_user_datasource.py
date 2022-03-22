from abc import ABC, abstractmethod

from database import crud, models, schemas
from dependency import provider


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


class GithubUserDBDataSource(GithubUserDataSource):
    async def readUser(self, email: str) -> schemas.User | None:
        match crud.readUser(provider["db"].db, email):
            case models.User(email=userEmail, github_access_token=accessToken, github_refresh_token=refreshToken):
                return schemas.User(
                    email=str(userEmail), githubAccessToken=str(accessToken), githubRefreshToken=str(refreshToken)
                )
            
        return None

    async def createUser(self, email: str, accessToken: str, refreshToken: str):
        crud.createUser(
            provider["db"].db,
            schemas.User(
                email=email,
                githubAccessToken=accessToken,
                githubRefreshToken=refreshToken,
            ),
        )

    async def updateUser(self, email: str, accessToken: str, refreshToken: str):
        crud.updateUser(
            provider["db"].db,
            email=email,
            accessToken=accessToken,
            refreshToken=refreshToken,
        )
