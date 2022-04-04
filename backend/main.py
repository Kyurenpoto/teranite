from database import DB, Base, engine

Base.metadata.create_all(bind=engine)


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


from adaptor.datasource.github_authtoken_api_datasource import GithubAuthTokenAPIDataSource
from adaptor.datasource.github_user_db_datasource import GithubUserDBDataSource
from adaptor.datasource.github_userinfo_api_datasource import GithubUserInfoAPIDataSource
from adaptor.repository.github_authtoken_simple_repository import GithubAuthTokenSimpleRepository
from adaptor.repository.github_user_simple_repository import GithubUserSimpleRepository
from adaptor.repository.github_userinfo_simple_repository import GithubUserInfoSimpleRepository
from dependencies.dependency import TypeValue, provider

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
        "auth-token-source": GithubAuthTokenAPIDataSource,
        "user-info-source": GithubUserInfoAPIDataSource,
        "user-source": GithubUserDBDataSource,
    }
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
