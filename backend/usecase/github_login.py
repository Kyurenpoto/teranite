from dependency import provider
from entity.auth_token import GithubAuthToken, UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user import GithubUser
from entity.github_user_info import GithubUserInfo
from repository.github_authtoken_repository import GithubAuthTokenRepository
from repository.github_user_repository import GithubUserRepository
from repository.github_userinfo_repository import GithubUserInfoRepository


class GithubIssueToken:
    def __init__(self):
        self.repository: GithubAuthTokenRepository = provider["auth-token-repo"]
    
    async def issue(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return await self.repository.readByTemporaryCode(code)


class GithubAccessUserInfo:
    def __init__(self):
        self.repository: GithubUserInfoRepository = provider["user-info-repo"]
    
    async def access(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return await self.repository.readByAuthToken(authToken)


class GithubUserExistance:
    def __init__(self):
        self.repository: GithubUserRepository = provider["user-repo"]
    
    async def exist(self, userInfo: GithubUserInfo) -> bool:
        match await self.repository.readByEmail(userInfo.email):
            case GithubUser():
                return True
            
        return False


class GithubCreateUser:
    def __init__(self):
        self.repository: GithubUserRepository = provider["user-repo"]
        
    async def create(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await self.repository.create(GithubUser(email=userInfo.email, authToken=authToken))


class GithubUpdateUserAuthToken:
    def __init__(self):
        self.repository: GithubUserRepository = provider["user-repo"]
        
    async def update(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await self.repository.updateAuthToken(email=userInfo.email, authToken=authToken)


class GithubLoginWithoutToken:
    async def login(self, code: GithubTemporaryCode) -> UserAuthToken:
        authToken = await GithubIssueToken().issue(code)
        userInfo = await GithubAccessUserInfo().access(authToken)

        if (await GithubUserExistance().exist(userInfo)):
            await GithubUpdateUserAuthToken().update(userInfo, authToken)

            return UserAuthToken(userInfo.email, userInfo.email)
        else:
            await GithubCreateUser().create(userInfo, authToken)

            return UserAuthToken(userInfo.email, userInfo.email)
