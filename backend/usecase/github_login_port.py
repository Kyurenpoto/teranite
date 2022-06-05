from abc import ABC, abstractmethod

from entity.auth_token import UserAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubLoginWithTemporaryCodeInputPort(ABC):
    @abstractmethod
    async def login(self, code: GithubTemporaryCode):
        pass


class GithubLoginWithTemporaryCodeOutputPort(ABC):
    @abstractmethod
    async def present(self, authToken: UserAuthToken):
        pass
