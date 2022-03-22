from abc import ABC, abstractmethod

from httpx import AsyncClient
from dependency import provider


class GithubAuthTokenDataSource(ABC):
    @abstractmethod
    async def createAuthToken(self, code: str) -> dict:
        pass


class GithubAuthTokenAPIDataSource(GithubAuthTokenDataSource):
    async def createAuthToken(self, code: str) -> dict:
        async with AsyncClient() as client:
            return (
                await client.post(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": provider["github-config"]["client-id"],
                        "client_secret": provider["github-config"]["client-secret"],
                        "code": str(code),
                    },
                    timeout=1.0,
                )
            ).json()
