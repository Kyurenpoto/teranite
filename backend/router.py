from enum import Enum, auto
from functools import reduce
from typing import NamedTuple

from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse, JSONResponse


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


from pydantic import BaseModel

from adapter.token_json_encoder import TokenJsonEncoder
from repository.github_authtoken_repository import WebGithubAuthTokenRepository
from repository.github_user_repository import SQLiteGithubUserRepository
from repository.github_userinfo_repository import WebGithubUserInfoRepository
from usecase.github_login import GithubLoginWithoutToken
from usecase.request_object import GithubLoginWithoutTokenRequest


class TemporaryCode(BaseModel):
    code: str


@router.post("/token/{sns_type:path}")
async def token(code: TemporaryCode, sns_type: str):
    try:
        if sns_type == "github":
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=TokenJsonEncoder().from_token(
                    (
                        await GithubLoginWithoutToken.from_repositories(
                            WebGithubAuthTokenRepository(),
                            WebGithubUserInfoRepository(),
                            SQLiteGithubUserRepository(),
                        ).login(GithubLoginWithoutTokenRequest(code.code))
                    )
                ),
            )

        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    except RuntimeError as e:
        print(e)
