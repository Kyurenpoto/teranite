from abc import ABC, abstractmethod

from dependency import provider
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
    async def readByEmail(self, email: str) -> GithubUser | None:
        match await provider["user-db"].readUser(email):
            case {"email": email, "githubAccessToken": accessToken, "githubRefreshToken": refreshToken}:
                return GithubUser(email, GithubAuthToken(accessToken, refreshToken))
        return None

    async def create(self, user: GithubUser):
        return await provider["user-db"].createUser(user.email, user.authToken.accessToken, user.authToken.refreshToken)

    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        return await provider["user-db"].updateUser(email, authToken.accessToken, authToken.refreshToken)
