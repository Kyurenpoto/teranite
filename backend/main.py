from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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


from .executable_request import ExecutableRequest, GithubLoginLogic


logics: dict[str, ExecutableRequest] = {
    "login/github/callback": GithubLoginLogic(clientId="", clientSecret="")
}


@app.get("/{full_path:path}")
async def index(request: Request, full_path: str):
    print(f"full_path: {full_path}")
    if full_path in logics:
        return await logics[full_path].execute(request)
    return templates.TemplateResponse("index.html", {"request": request})
