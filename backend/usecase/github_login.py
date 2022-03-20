from entity.auth_token import GithubAuthToken, UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from entity.github_user import GithubUser
from entity.github_user_info import GithubUserInfo
from dependency import provider


class GithubIssueToken:    
    async def issue(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return await provider.dependency("auth-token-repo").findByTemporaryCode(code)


class GithubAccessUserInfo:    
    async def access(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return await provider.dependency("user-info-repo").findByAuthToken(authToken)


class GithubUserExistance:    
    async def exist(self, userInfo: GithubUserInfo) -> bool:
        match await provider.dependency("user-repo").readByEmail(userInfo.email):
            case GithubUser():
                return True
            
        return False


class GithubCreateUser:    
    async def create(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await provider.dependency("user-repo").create(GithubUser(email=userInfo.email, authToken=authToken))


class GithubUpdateUserAuthToken:    
    async def update(self, userInfo: GithubUserInfo, authToken: GithubAuthToken):
        await provider.dependency("user-repo").updateAuthToken(email=userInfo.email, authToken=authToken)


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
