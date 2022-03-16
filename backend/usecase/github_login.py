from typing import NamedTuple

from entity.github_temporary_code import GithubTemporaryCode
from dependency_injector.wiring import Provide, inject

from config import Container
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


class GithubIssueToken:
    @inject
    async def issue(
        self,
        request: GithubIssueTokenRequest,
        repository: GithubAuthTokenRepository = Provide[Container.config.repositories.github_authtoken_repository]
    ) -> GithubIssueTokenResponse:
        return GithubIssueTokenResponse._make(await repository.findByTemporaryCode(GithubTemporaryCode(request)))


class GithubAccessUserInfo:
    @inject
    async def access(
        self,
        request: GithubAccessUserInfoRequest,
        repository: GithubUserInfoRepository = Provide[Container.config.repositories.github_userinfo_repository]
    ) -> GithubAccessUserInfoResponse:
        return GithubAccessUserInfoResponse._make(await repository.findByAuthToken(GithubAuthToken._make(request)))


class GithubUserExistance:
    @inject
    async def exist(
        self,
        request: GithubUserExistanceRequest,
        repository: GithubUserRepository = Provide[Container.config.repositories.github_user_repository]
    ) -> GithubUserExistanceResponse:
        match await repository.readByEmail(request.email):
            case GithubUser():
                return GithubUserExistanceResponse(True)
            
        return GithubUserExistanceResponse(False)


class GithubCreateUser:
    @inject
    async def create(
        self,
        request: GithubCreateUserRequest,
        repository: GithubUserRepository = Provide[Container.config.repositories.github_user_repository]
    ):
        await repository.create(GithubUser(email=request.userInfo.email, authToken=request.authToken))


class GithubUpdateUserAuthToken:
    @inject
    async def update(
        self, 
        request: GithubUpdateUserAuthTokenRequest,
        repository: GithubUserRepository = Provide[Container.config.repositories.github_user_repository]
    ):
        await repository.updateAuthToken(email=request.userInfo.email, authToken=request.authToken)


class GithubLoginWithoutToken(NamedTuple):
    issueToken = GithubIssueToken()
    accessUserInfo = GithubAccessUserInfo()
    userExistance = GithubUserExistance()
    createUser = GithubCreateUser()
    updateUserAuthToken = GithubUpdateUserAuthToken()

    async def login(self, request: GithubLoginWithoutTokenRequest) -> GithubLoginWithoutTokenResponse:
        authToken = GithubAuthToken._make(await self.issueToken.issue(GithubIssueTokenRequest(str(request))))
        userInfo = await self.accessUserInfo.access(GithubAccessUserInfoRequest._make(authToken))

        if (await self.userExistance.exist(GithubUserExistanceRequest._make(userInfo))).result:
            await self.updateUserAuthToken.update(GithubUpdateUserAuthTokenRequest(userInfo, authToken))

            return GithubLoginWithoutTokenResponse(userInfo.email, userInfo.email)
        else:
            await self.createUser.create(GithubCreateUserRequest(userInfo, authToken))

            return GithubLoginWithoutTokenResponse(userInfo.email, userInfo.email)
