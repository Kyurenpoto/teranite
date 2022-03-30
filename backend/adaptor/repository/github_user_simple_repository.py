from adaptor.datasource.github_user_datasource import GithubUserDataSource
from adaptor.repository.github_user_repository import GithubUserRepository
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser


class GithubUserSimpleRepository(GithubUserRepository):
    def __init__(self):
        self.datasource: GithubUserDataSource = provider["user-source"]
    
    async def readByEmail(self, email: str) -> GithubUser | None:
        match await self.datasource.readUser(email):
            case {"email": email, "githubAccessToken": accessToken, "githubRefreshToken": refreshToken}:
                return GithubUser(email, GithubAuthToken(accessToken, refreshToken))
        return None

    async def create(self, user: GithubUser):
        return await self.datasource.createUser(user.email, user.authToken.accessToken, user.authToken.refreshToken)

    async def updateAuthToken(self, email: str, authToken: GithubAuthToken):
        return await self.datasource.updateUser(email, authToken.accessToken, authToken.refreshToken)
