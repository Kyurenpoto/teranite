from abc import ABC, abstractmethod

from httpx import AsyncClient


class GithubUserInfoDataSource(ABC):
    @abstractmethod
    async def readUserInfo(self, accessToken: str) -> dict:
        pass


class GithubUserInfoAPIDataSource(GithubUserInfoDataSource):
    async def readUserInfo(self, accessToken: str) -> dict:
        async with AsyncClient() as client:
            return (
                await client.get(
                    url="https://api.github.com/user",
                    headers={"Authorization": f"token {accessToken}"},
                    timeout=1.0,
                )
            ).json()
