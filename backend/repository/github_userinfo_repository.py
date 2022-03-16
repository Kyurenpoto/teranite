from abc import ABC, abstractmethod

from httpx import AsyncClient

from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo


class GithubUserInfoRepository(ABC):
    @abstractmethod
    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        pass


class WebGithubUserInfoRepository(GithubUserInfoRepository):
    async def findByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        async with AsyncClient() as client:
            response: dict = (
                await client.get(
                    url="https://api.github.com/user",
                    headers={"Authorization": f"token {authToken.accessToken}"},
                    timeout=1.0,
                )
            ).json()

            return GithubUserInfo(email=response["email"])
