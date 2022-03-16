from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject

from config import Container
from database import crud, models, schemas
from database.database import DB
from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser


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
    @inject
    async def readByEmail(self, email: str, db: DB = Provide[Container.db]) -> GithubUser | None:
        match crud.readUser(db.db, email):
            case models.User(email=userEmail, github_access_token=accessToken, github_refresh_token=refreshToken):
                return GithubUser(userEmail, GithubAuthToken(accessToken, refreshToken))
            
        return None

    @inject
    async def create(self, user: GithubUser, db: DB = Provide[Container.db]):
        crud.createUser(
            db.db,
            schemas.User(
                email=user.email,
                githubAccessToken=user.authToken.accessToken,
                githubRefreshToken=user.authToken.refreshToken,
            ),
        )

    @inject
    async def updateAuthToken(self, email: str, authToken: GithubAuthToken, db: DB = Provide[Container.db]):
        crud.updateUser(
            db.db,
            email=email,
            accessToken=authToken.accessToken,
            refreshToken=authToken.refreshToken,
        )
