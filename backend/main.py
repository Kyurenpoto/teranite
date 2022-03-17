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


def wire():
    app.state.container = container
    app.state.container.config.from_dict(
        {
            "githubClientId": "",
            "githubClientSecret": "",
        }
    )
    app.state.container.wire(modules=[github_authtoken_repository, github_user_repository])


def unwire():
    app.state.container.unwire()


import uvicorn

if __name__ == "__main__":
    wire()

    uvicorn.run("main:app", reload=True)
