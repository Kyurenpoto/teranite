from abc import ABC, abstractmethod

from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubAuthTokenRepository(ABC):
    @abstractmethod
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        pass
