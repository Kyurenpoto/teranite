from abc import ABC, abstractmethod

from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo


class GithubUserInfoRepository(ABC):
    @abstractmethod
    async def readByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        pass
