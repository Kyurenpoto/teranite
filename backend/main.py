from database import models
from database.database import DB, engine

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


from datasource.github_authtoken_api_datasource import GithubAuthTokenAPIDataSource
from datasource.github_user_db_datasource import GithubUserDBDataSource
from datasource.github_userinfo_api_datasource import GithubUserInfoAPIDataSource
from dependency import TypeValue, provider
from repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository
from repository.github_user_simple_repository import GithubUserSimpleRepository
from repository.github_userinfo_simple_repository import GithubUserInfoSimpleRepository

provider.wire(
    {
        "github-config": TypeValue(
            {
                "client-id": "",
                "client-secret": "",
            },
        ),
        "db": DB,
        "auth-token-repo": GithubAuthTokenSimpleRepository,
        "user-info-repo": GithubUserInfoSimpleRepository,
        "user-repo": GithubUserSimpleRepository,
        "auth-token-api": GithubAuthTokenAPIDataSource,
        "user-info-api": GithubUserInfoAPIDataSource,
        "user-db": GithubUserDBDataSource,
    }
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
