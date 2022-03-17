from abc import ABC, abstractmethod
from typing import NamedTuple

from httpx import AsyncClient

from dependency import Container
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubAuthTokenRepository(ABC):
    @abstractmethod
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        pass


class WebGithubAuthTokenRepository(GithubAuthTokenRepository):
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        async with AsyncClient() as client:
            response: dict = (
                await client.post(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": Container.githubConfig.clientId,
                        "client_secret": Container.githubConfig.clientSecret,
                        "code": str(code),
                    },
                    timeout=1.0,
                )
            ).json()

            return GithubAuthToken(
                accessToken=response["access_token"],
                refreshToken=response["refresh_token"],
            )
