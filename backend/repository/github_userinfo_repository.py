from abc import ABC, abstractmethod

from adaptor.from_json_decoder import JsonUserInfoDecoder
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo


class GithubUserInfoRepository(ABC):
    @abstractmethod
    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        pass


class WebGithubUserInfoRepository(GithubUserInfoRepository):
    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return JsonUserInfoDecoder.from_json(await provider["user-info-api"].readUserInfo(authToken.accessToken))
