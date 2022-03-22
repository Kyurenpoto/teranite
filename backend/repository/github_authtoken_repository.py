from abc import ABC, abstractmethod

from adaptor.from_json_decoder import JsonAuthTokenDecoder
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubAuthTokenRepository(ABC):
    @abstractmethod
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        pass


class WebGithubAuthTokenRepository(GithubAuthTokenRepository):
    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return JsonAuthTokenDecoder.from_json(await provider["auth-token-api"].createAuthToken(str(code)))
