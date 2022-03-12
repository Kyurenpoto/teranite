from database import models
from database.database import engine

models.Base.metadata.create_all(bind=engine)

from enum import Enum, auto
from typing import Callable, NamedTuple

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


class PathType(Enum):
    NONE = auto()
    HTML_ROUTE = auto()
    API_ROUTE = auto()
    STATIC_FILE = auto()


class ValidPath(NamedTuple):
    path: str
    type: PathType = PathType.NONE


VALID_PATHS = [
    ValidPath("/favicon.ico", PathType.STATIC_FILE),
    ValidPath("/logo.svg", PathType.STATIC_FILE),
    ValidPath("/robots.txt", PathType.STATIC_FILE),
    ValidPath("/dist/index.css", PathType.STATIC_FILE),
    ValidPath("/dist/index.js", PathType.STATIC_FILE),
    ValidPath("/", PathType.HTML_ROUTE),
    ValidPath("/login", PathType.HTML_ROUTE),
    ValidPath("/login/github/callback", PathType.HTML_ROUTE),
]

templates = Jinja2Templates(directory="static")


class UriRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            valids = list(filter(lambda x: x.path == request.url.path, VALID_PATHS))
            if len(valids) == 0:
                print("invalid uri")
                return templates.TemplateResponse("index.html", {"request": request})

            if valids[0].type == PathType.HTML_ROUTE:
                return templates.TemplateResponse("index.html", {"request": request})

            if valids[0].type == PathType.API_ROUTE:
                return await original_route_handler(request)

            if valids[0].type == PathType.STATIC_FILE:
                return FileResponse(f"static{request.url.path}")

            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

        return custom_route_handler


app = FastAPI()
app.router.route_class = UriRoute

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

import executable_request
from config import container

app.state.container = container
app.state.container.wire(modules=[executable_request])


from executable_request import ExecutableRequest, GithubLoginLogic

logics: dict[str, ExecutableRequest] = {
    "login/github/callback": GithubLoginLogic(clientId="", clientSecret="")
}


@app.get("/{full_path:path}")
async def index(request: Request, full_path: str):
    print(f"full_path: {full_path}")
    if full_path in logics:
        return await logics[full_path].execute(request)
    return templates.TemplateResponse("index.html", {"request": request})
