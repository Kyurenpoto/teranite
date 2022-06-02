from entity.auth_token import OwnAuthToken, SocialAuthToken


class UserAuthToken:
    email: str
    ownAuthToken: OwnAuthToken
    socialAuthToken: SocialAuthToken
    socialType: str
    expireDatetime: str

    def __init__(
        self,
        email: str,
        ownAuthToken: OwnAuthToken,
        expireDatetime: str,
        socialAuthToken: SocialAuthToken,
        socialType: str,
    ):
        self.email = email
        self.ownAuthToken = ownAuthToken
        self.expireDatetime = expireDatetime
        self.socialAuthToken = socialAuthToken
        self.socialType = socialType

    def __eq__(self, other) -> bool:
        return (
            self.email == other.email
            and self.ownAuthToken == other.ownAuthToken
            and self.expireDatetime == other.expireDatetime
            and self.socialAuthToken == other.socialAuthToken
            and self.socialType == other.socialType
        )

    def copy(self):
        return UserAuthToken(self.email, self.ownAuthToken, self.expireDatetime, self.socialAuthToken, self.socialType)


class UserAuthTokenBuilder:
    email: str
    ownAuthToken: OwnAuthToken
    expireDatetime: str
    socialAuthToken: SocialAuthToken
    socialType: str

    def __init__(self, email):
        self.email = email
        self.ownAuthToken = OwnAuthToken("", "")
        self.socialAuthToken = SocialAuthToken("", "")
        self.socialType = ""
        self.expireDatetime = ""

    def fillOwnAuthTokenWithExpireDatetime(self, ownAuthToken: OwnAuthToken, expireDatetime: str):
        self.ownAuthToken = ownAuthToken
        self.expireDatetime = expireDatetime

        return self

    def fillSocialAuthTokenWithSocialType(self, socialAuthToken: SocialAuthToken, socialType: str):
        self.socialAuthToken = socialAuthToken
        self.socialType = socialType

        return self

    def build(self) -> UserAuthToken:
        return UserAuthToken(self.email, self.ownAuthToken, self.expireDatetime, self.socialAuthToken, self.socialType)
