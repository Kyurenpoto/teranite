from abc import ABC, abstractmethod

from entity.auth_token import UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubLoginWithoutTokenOutputPort(ABC):
    @abstractmethod
    async def present(self, authToken: UserAuthToken):
        pass


class GithubLoginWithoutTokenInputPort(ABC):
    def __init__(self, outputPort: GithubLoginWithoutTokenOutputPort):
        self.outputPort = outputPort

    @abstractmethod
    async def login(self, code: GithubTemporaryCode):
        pass
