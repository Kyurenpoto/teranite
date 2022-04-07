from enum import Enum, auto
from functools import reduce
from typing import NamedTuple

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse


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
    ValidPath("/explore", PathType.HTML_ROUTE),
    ValidPath("/rank", PathType.HTML_ROUTE),
    ValidPath("/daily", PathType.HTML_ROUTE),
    ValidPath("/weekly", PathType.HTML_ROUTE),
    ValidPath("/monthly", PathType.HTML_ROUTE),
    ValidPath("/token/github{rest_path: path}", PathType.API_ROUTE),
]


router = APIRouter()


def getMultiPaths(paths: list[str]):
    def real_decorator(func):
        return reduce(lambda acc, cur: router.get(cur)(acc), paths, func)

    return real_decorator


from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="static")


@getMultiPaths(
    list(
        map(
            lambda x: x.path,
            filter(lambda x: x.type == PathType.HTML_ROUTE, VALID_PATHS),
        )
    )
)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@getMultiPaths(
    list(
        map(
            lambda x: x.path,
            filter(lambda x: x.type == PathType.STATIC_FILE, VALID_PATHS),
        )
    )
)
async def static(request: Request):
    return FileResponse(f"static{request.url.path}")


from adaptor.mediator.temporary_code import TemporaryCode
from dependencies.dependency import provider


@router.post("/token/{sns_type:path}")
async def token(code: TemporaryCode, sns_type: str):
    return await provider["auth"]["token-viewmodel"].update(code, sns_type)
