from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from fastapi import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient, Response


class ExecutableRequest(ABC):
    @abstractmethod
    async def execute(self, request: Request):
        pass


class GithubData(NamedTuple):
    clientId: str
    clientSecret: str


class GithubLoginLogic(GithubData, ExecutableRequest):
    async def execute(self, request: Request):
        print("github logic")
        async with AsyncClient() as client:
            response: Response = await client.post(
                url=f"https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                params={
                    "client_id": self.clientId,
                    "client_secret": self.clientSecret,
                    "code": request.query_params["code"],
                },
                timeout=1.0,
            )
            print(response.json())
            return RedirectResponse("http://127.0.0.1:8000/")
