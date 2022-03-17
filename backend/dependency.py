from typing import NamedTuple

from database.database import DB


class GithubConfig(NamedTuple):
    clientId: str
    clientSecret: str


class Container(NamedTuple):
    db = DB()
    githubConfig = GithubConfig(clientId="", clientSecret="")
