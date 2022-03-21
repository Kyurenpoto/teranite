from abc import ABC, abstractmethod

from adaptor.from_json_decoder import JsonUserInfoDecoder
from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo
from httpx import AsyncClient


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

            return JsonUserInfoDecoder.from_json(response)
