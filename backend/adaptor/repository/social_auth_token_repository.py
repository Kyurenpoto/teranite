from abc import ABC, abstractmethod
from entity.auth_token import SocialAuthToken
from entity.temporary_code import TemporaryCode


class InvalidTemporaryCodeError(RuntimeError):
    def __init__(self):
        super().__init__("invalid temporary code")


class SocialAuthTokenRepository(ABC):
    @abstractmethod
    async def readByTemporaryCode(self, code: TemporaryCode, socialType: str) -> SocialAuthToken:
        pass


class FakeSocialAuthTokenRepository(SocialAuthTokenRepository):
    def __init__(self):
        self.codes = set()

    async def readByTemporaryCode(self, code: TemporaryCode, socialType: str) -> SocialAuthToken:
        if str(code) not in self.codes:
            raise InvalidTemporaryCodeError()

        self.codes.remove(code)

        return SocialAuthToken(f"access@{code}", f"refresh@{code}")
