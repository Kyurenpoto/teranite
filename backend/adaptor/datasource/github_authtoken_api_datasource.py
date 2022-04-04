from adaptor.datasource.github_authtoken_datasource import GithubAuthTokenDataSource
from dependencies.dependency import provider
from httpx import AsyncClient


class GithubAuthTokenAPIDataSource(GithubAuthTokenDataSource):
    def __init__(self):
        self.config = provider["github-config"]

    async def createAuthToken(self, code: str) -> dict:
        async with AsyncClient() as client:
            return (
                await client.post(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": self.config["client-id"],
                        "client_secret": self.config["client-secret"],
                        "code": str(code),
                    },
                    timeout=1.0,
                )
            ).json()
