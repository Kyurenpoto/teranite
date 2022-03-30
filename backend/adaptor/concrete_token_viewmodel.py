from fastapi.responses import JSONResponse

from adaptor.temporary_code import TemporaryCode
from adaptor.token_viewmodel import TokenViewModel
from adaptor.token_controller import TokenController


class TokenViewModelImpl(TokenViewModel):
    def __init__(self):
        self.controller = TokenController(self)

    async def update(self, code: TemporaryCode, sns_type: str) -> JSONResponse:
        await self.controller.execute(code, sns_type)

        return self.response
