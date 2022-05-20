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


from dependencies.dependency import provider
from dependencies.auth_container import AuthContainer

provider.wire({"auth": AuthContainer()})

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
