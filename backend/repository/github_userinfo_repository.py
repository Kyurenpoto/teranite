from abc import ABC, abstractmethod

from httpx import AsyncClient

from ..entity.auth_token import GithubAuthToken
from ..entity.github_user_info import GithubUserInfo


class GithubUserInfoRepository(ABC):
    @abstractmethod
    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        pass

