from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from httpx import AsyncClient, Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


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
                url=f"https://github.com/login/oauth/access_token?client_id={self.clientId}&client_secret={self.clientSecret}&code={request.query_params['code']}",
                headers={"Accept": "application/json"},
                timeout=1.0,
            )
            print(response.json())


logics: dict[str, ExecutableRequest] = {
    "login/github/callback": GithubLoginLogic("", "")
}


@app.get("/{full_path:path}")
async def index(request: Request, full_path: str):
    print(f"full_path: {full_path}")
    if full_path in logics:
        await logics[full_path].execute(request)
        return RedirectResponse("http://127.0.0.1:8000/")
    return templates.TemplateResponse("index.html", {"request": request})
