from abc import ABC, abstractmethod


class LoginWithTemporaryCodeInputPort(ABC):
    @abstractmethod
    async def login(self, temporaryCode, socialType):
        pass


class LoginWithTemporaryCodeOutputPort(ABC):
    @abstractmethod
    async def present(self, ownAuthToken):
        pass


class LoginWithAuthTokenInputPort(ABC):
    @abstractmethod
    async def login(self, email, ownAuthToken):
        pass


class LoginWithAuthTokenOutputPort(ABC):
    @abstractmethod
    async def present(self, ownAuthToken):
        pass
