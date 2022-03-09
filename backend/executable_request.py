from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from fastapi import Request
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from sqlalchemy.orm import Session

from database import crud, schemas
from dependency_injector.wiring import Provide, inject
from config import Container
from database.database import DB


class GithubToken(NamedTuple):
    accessToken: str
    refreshToken: str


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
        token: GithubToken = await self.accessToken(request.query_params["code"])
        email: str = await self.email(token)
        await self.updateToken(email, token)

        print(f"login: {email}")

        return RedirectResponse("http://127.0.0.1:8000/")

    async def accessToken(self, authCode: str) -> GithubToken:
        async with AsyncClient() as client:
            response: dict = (
                await client.post(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": self.clientId,
                        "client_secret": self.clientSecret,
                        "code": authCode,
                    },
                    timeout=1.0,
                )
            ).json()

            return GithubToken(
                accessToken=response["access_token"],
                refreshToken=response["access_token"],
            )

    async def email(self, token: GithubToken) -> str:
        async with AsyncClient() as client:
            response: dict = (
                await client.get(
                    url="https://api.github.com/user",
                    headers={"Authorization": f"token {token.accessToken}"},
                    timeout=1.0,
                )
            ).json()

            return response["email"]

    async def updateToken(
        self, email: str, token: GithubToken, db: DB = Provide[Container.db]
    ):
        user = crud.readUser(db.db, email)
        if user is None:
            crud.createUser(
                db.db,
                schemas.User(
                    email=email,
                    githubAccessToken=token.accessToken,
                    githubRefreshToken=token.refreshToken,
                ),
            )
        else:
            crud.updateUser(
                db.db,
                email=email,
                accessToken=token.accessToken,
                refreshToken=token.refreshToken,
            )
