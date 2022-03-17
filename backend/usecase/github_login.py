from typing import NamedTuple

from entity.github_temporary_code import GithubTemporaryCode

from entity.auth_token import GithubAuthToken
from entity.github_user import GithubUser
from repository.github_authtoken_repository import GithubAuthTokenRepository
from repository.github_user_repository import GithubUserRepository
from repository.github_userinfo_repository import GithubUserInfoRepository
from .request_object import (
    GithubAccessUserInfoRequest,
    GithubCreateUserRequest,
    GithubIssueTokenRequest,
    GithubLoginWithoutTokenRequest,
    GithubUpdateUserAuthTokenRequest,
    GithubUserExistanceRequest
)
from .response_object import (
    GithubAccessUserInfoResponse,
    GithubIssueTokenResponse,
    GithubLoginWithoutTokenResponse,
    GithubUserExistanceResponse
)


class GithubIssueToken(NamedTuple):
    repository: GithubAuthTokenRepository
    
    async def issue(self, request: GithubIssueTokenRequest) -> GithubIssueTokenResponse:
        return GithubIssueTokenResponse._make(await self.repository.findByTemporaryCode(GithubTemporaryCode(request)))


class GithubAccessUserInfo(NamedTuple):
    repository: GithubUserInfoRepository
    
    async def access(self, request: GithubAccessUserInfoRequest) -> GithubAccessUserInfoResponse:
        return GithubAccessUserInfoResponse._make(
            await self.repository.findByAuthToken(GithubAuthToken._make(request))
        )


class GithubUserExistance(NamedTuple):
    repository: GithubUserRepository
    
    async def exist(self, request: GithubUserExistanceRequest) -> GithubUserExistanceResponse:
        match await self.repository.readByEmail(request.email):
            case GithubUser():
                return GithubUserExistanceResponse(True)
            
        return GithubUserExistanceResponse(False)


class GithubCreateUser(NamedTuple):
    repository: GithubUserRepository
    
    async def create(self, request: GithubCreateUserRequest):
        await self.repository.create(GithubUser(email=request.userInfo.email, authToken=request.authToken))


class GithubUpdateUserAuthToken(NamedTuple):
    repository: GithubUserRepository
    
    async def update(self, request: GithubUpdateUserAuthTokenRequest):
        await self.repository.updateAuthToken(email=request.userInfo.email, authToken=request.authToken)


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

    async def login(self, request: GithubLoginWithoutTokenRequest) -> GithubLoginWithoutTokenResponse:
        authToken = GithubAuthToken._make(await self.issueToken.issue(GithubIssueTokenRequest(str(request))))
        userInfo = await self.accessUserInfo.access(GithubAccessUserInfoRequest._make(authToken))

        if (await self.userExistance.exist(GithubUserExistanceRequest._make(userInfo))).result:
            await self.updateUserAuthToken.update(GithubUpdateUserAuthTokenRequest(userInfo, authToken))

            return GithubLoginWithoutTokenResponse(userInfo.email, userInfo.email)
        else:
            await self.createUser.create(GithubCreateUserRequest(userInfo, authToken))

            return GithubLoginWithoutTokenResponse(userInfo.email, userInfo.email)
