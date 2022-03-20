from database import models
from database.database import engine, DB

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


import uvicorn
from dependency import provider
from repository.github_authtoken_repository import WebGithubAuthTokenRepository
from repository.github_userinfo_repository import WebGithubUserInfoRepository
from repository.github_user_repository import SQLiteGithubUserRepository

provider.wire(
    {
        "github-config": {
            "client-id": "",
            "client-secret": "",
        },
        "db": DB(),
        "auth-token-repo": WebGithubAuthTokenRepository(),
        "user-info-repo": WebGithubUserInfoRepository(),
        "user-repo": SQLiteGithubUserRepository(),
    }
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
