from adaptor.from_json_decoder import JsonUserInfoDecoder
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo
from repository.github_userinfo_repository import GithubUserInfoRepository


class GithubUserInfoSimpleRepository(GithubUserInfoRepository):
    async def readByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return JsonUserInfoDecoder.from_json(await provider["user-info-api"].readUserInfo(authToken.accessToken))
