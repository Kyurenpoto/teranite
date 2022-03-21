from abc import ABC, abstractmethod

from database import crud, models, schemas
from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser
from dependency import provider


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


class SQLiteGithubUserRepository(GithubUserRepository):
    async def readByEmail(self, email: str) -> GithubUser | None:
        match crud.readUser(provider["db"].db, email):
            case models.User(email=userEmail, github_access_token=accessToken, github_refresh_token=refreshToken):
                return GithubUser(str(userEmail), GithubAuthToken(str(accessToken), str(refreshToken)))
            
        return None

    async def create(self, user: GithubUser):
        crud.createUser(
            provider["db"].db,
            schemas.User(
                email=user.email,
                githubAccessToken=user.authToken.accessToken,
                githubRefreshToken=user.authToken.refreshToken,
            ),
        )

    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        crud.updateUser(
            provider["db"].db,
            email=email,
            accessToken=authToken.accessToken,
            refreshToken=authToken.refreshToken,
        )
