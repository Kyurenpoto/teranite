from database import models
from database.database import engine

models.Base.metadata.create_all(bind=engine)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from router import router

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

from config import container
from repository import github_authtoken_repository, github_user_repository
from usecase import github_login
from repository.github_userinfo_repository import WebGithubUserInfoRepository
from repository.github_authtoken_repository import WebGithubAuthTokenRepository
from repository.github_user_repository import SQLiteGithubUserRepository

app.state.container = container
app.state.container.config.from_dict(
    {
        "githubClientId": "",
        "githubClientSecret": "",
        "repositories": {
            "github_userinfo_repository": WebGithubUserInfoRepository(),
            "github_authtoken_repository": WebGithubAuthTokenRepository(),
            "github_user_repository": SQLiteGithubUserRepository(),
        },
    }
)
app.state.container.wire(modules=[github_authtoken_repository, github_user_repository, github_login])
