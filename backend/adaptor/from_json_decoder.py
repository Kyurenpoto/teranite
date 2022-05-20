from entity.auth_token import GithubAuthToken
from entity.github_user_info import GithubUserInfo


class JsonAuthTokenDecoder:
    @classmethod
    def from_json(cls, json: dict) -> GithubAuthToken:
        return GithubAuthToken(accessToken=json["access_token"], refreshToken=json["refresh_token"])


class JsonUserInfoDecoder:
    @classmethod
    def from_json(cls, json: dict) -> GithubUserInfo:
        return GithubUserInfo(email=json["email"])
