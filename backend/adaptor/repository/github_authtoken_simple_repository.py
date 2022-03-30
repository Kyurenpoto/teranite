from adaptor.datasource.github_authtoken_datasource import GithubAuthTokenDataSource
from adaptor.from_json_decoder import JsonAuthTokenDecoder
from adaptor.repository.github_authtoken_repository import GithubAuthTokenRepository
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode


class GithubAuthTokenSimpleRepository(GithubAuthTokenRepository):
    def __init__(self):
        self.datasource: GithubAuthTokenDataSource = provider["auth-token-source"]

    async def readByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return JsonAuthTokenDecoder.from_json(await self.datasource.createAuthToken(str(code)))
