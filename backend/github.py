from __future__ import annotations

from typing import NamedTuple

from dependency_injector.wiring import Provide, inject
from fastapi import status
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from pydantic import BaseModel

from config import Container
from database import crud, schemas
from database.database import DB


class Code(BaseModel):
    code: str


class GithubToken(NamedTuple):
    accessToken: str
    refreshToken: str


class GithubOAuth(NamedTuple):
    clientId: str
    clientSecret: str

    async def execute(self, code: Code):
        token: GithubToken = await self.accessToken(code.code)
        email: str = await self.email(token)
        await self.updateToken(email, token)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "has_account": True,
                "access_token": email,
                "refresh_token": email,
            },
        )

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
                refreshToken=response["refresh_token"],
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

    @inject
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
