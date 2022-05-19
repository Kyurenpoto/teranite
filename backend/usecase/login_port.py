from abc import ABC, abstractmethod

from entity.auth_token import OwnAuthToken
from entity.temporary_code import TemporaryCode


class LoginWithTemporaryCodeInputPort(ABC):
    @abstractmethod
    async def login(self, temporaryCode: TemporaryCode, socialType: str) -> None:
        pass


class LoginWithTemporaryCodeOutputPort(ABC):
    @abstractmethod
    async def present(self, ownAuthToken: OwnAuthToken) -> None:
        pass


class LoginWithAuthTokenInputPort(ABC):
    @abstractmethod
    async def login(self, email, ownAuthToken: OwnAuthToken) -> None:
        pass


class LoginWithAuthTokenOutputPort(ABC):
    @abstractmethod
    async def present(self, ownAuthToken: OwnAuthToken) -> None:
        pass
