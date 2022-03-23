from adaptor.from_json_decoder import JsonUserInfoDecoder
from dependency import provider
from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo
from repository.github_userinfo_repository import GithubUserInfoRepository
from datasource.github_userinfo_datasource import GithubUserInfoDataSource


class GithubUserInfoSimpleRepository(GithubUserInfoRepository):
    def __init__(self):
        self.datasource: GithubUserInfoDataSource = provider["user-info-source"]

    async def readByAuthToken(self, authToken: GithubAuthToken) -> GithubUserInfo:
        return JsonUserInfoDecoder.from_json(await self.datasource.readUserInfo(authToken.accessToken))
