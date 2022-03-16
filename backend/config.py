from dependency_injector import containers, providers

from database.database import DB


class Container(containers.DeclarativeContainer):
    db = providers.Factory(DB)


container = Container()
