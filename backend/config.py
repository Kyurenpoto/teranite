from dependency_injector import containers, providers

from database.database import DB
from pydantic import BaseModel


class GithubConfig(BaseModel):
    clientId: str
    clientSecret: str


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Factory(DB)
    githubConfig = providers.Factory(
        GithubConfig, clientId=config.githubClientId, clientSecret=config.githubClientSecret
    )


container = Container()
