from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject
from httpx import AsyncClient

from config import Container, GithubConfig
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubAuthTokenRepository(ABC):
    @abstractmethod
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        pass


class WebGithubAuthTokenRepository(GithubAuthTokenRepository):
    @inject
    async def findByTemporaryCode(
        self, code: GithubTemporaryCode, config: GithubConfig = Provide[Container.githubConfig]
    ) -> GithubAuthToken:
        async with AsyncClient() as client:
            response: dict = (
                await client.post(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": config.clientId,
                        "client_secret": config.clientSecret,
                        "code": str(code),
                    },
                    timeout=1.0,
                )
            ).json()

            return GithubAuthToken(
                accessToken=response["access_token"],
                refreshToken=response["refresh_token"],
            )
