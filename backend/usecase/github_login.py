from typing import NamedTuple

from entity.auth_token import GithubAuthToken, UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user import GithubUser
from entity.github_user_info import GithubUserInfo
from repository.github_authtoken_repository import GithubAuthTokenRepository
from repository.github_user_repository import GithubUserRepository
from repository.github_userinfo_repository import GithubUserInfoRepository


class GithubIssueToken(NamedTuple):
    repository: GithubAuthTokenRepository
    
    async def issue(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return await self.repository.findByTemporaryCode(code)


class GithubAccessUserInfo(NamedTuple):
    repository: GithubUserInfoRepository
    
    async def access(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return await self.repository.findByAuthToken(authToken)


class GithubUserExistance(NamedTuple):
    repository: GithubUserRepository
    
    async def exist(self, userInfo: GithubUserInfo) -> bool:
        match await self.repository.readByEmail(userInfo.email):
            case GithubUser():
                return True
            
        return False


class GithubCreateUser(NamedTuple):
    repository: GithubUserRepository
    
    async def create(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await self.repository.create(GithubUser(email=userInfo.email, authToken=authToken))


class GithubUpdateUserAuthToken(NamedTuple):
    repository: GithubUserRepository
    
    async def update(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await self.repository.updateAuthToken(email=userInfo.email, authToken=authToken)


class GithubLoginWithoutToken(NamedTuple):
    issueToken: GithubIssueToken
    accessUserInfo: GithubAccessUserInfo
    userExistance: GithubUserExistance
    createUser: GithubCreateUser
    updateUserAuthToken: GithubUpdateUserAuthToken
    
    @classmethod
    def from_repositories(
        cls,
        authTokenRepository: GithubAuthTokenRepository,
        userInfoRepository: GithubUserInfoRepository,
        userRepository: GithubUserRepository
    ):
        return GithubLoginWithoutToken(
            GithubIssueToken(authTokenRepository),
            GithubAccessUserInfo(userInfoRepository),
            GithubUserExistance(userRepository),
            GithubCreateUser(userRepository),
            GithubUpdateUserAuthToken(userRepository)
        )

    async def login(self, code: GithubTemporaryCode) -> UserAuthToken:
        authToken = await self.issueToken.issue(code)
        userInfo = await self.accessUserInfo.access(authToken)

        if (await self.userExistance.exist(userInfo)):
            await self.updateUserAuthToken.update(userInfo, authToken)

            return UserAuthToken(userInfo.email, userInfo.email)
        else:
            await self.createUser.create(userInfo, authToken)

            return UserAuthToken(userInfo.email, userInfo.email)
