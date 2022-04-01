from abc import ABC, abstractmethod

from fastapi import status
from fastapi.responses import JSONResponse


class TokenViewModel(ABC):
    def __init__(self):
        self.response = JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @abstractmethod
    async def update(self):
        pass
