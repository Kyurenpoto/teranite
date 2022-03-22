from adaptor.from_json_decoder import JsonAuthTokenDecoder
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_temporary_code import GithubTemporaryCode
from repository.github_authtoken_repository import GithubAuthTokenRepository


class GithubAuthTokenSimpleRepository(GithubAuthTokenRepository):
    def __init__(self):
        self.datasource = provider["auth-token-api"]

    async def findByTemporaryCode(self, code: GithubTemporaryCode) -> GithubAuthToken:
        return JsonAuthTokenDecoder.from_json(await provider["auth-token-api"].createAuthToken(str(code)))
