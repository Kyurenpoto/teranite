from adaptor.mediator.temporary_code import TemporaryCode
from adaptor.mediator.token_controller import TokenController
from adaptor.mediator.token_viewmodel import TokenViewModel
from fastapi.responses import JSONResponse


class UpdatableTokenViewModel(TokenViewModel):
    def __init__(self):
        self.controller = TokenController(self)

    async def update(self, code: TemporaryCode, sns_type: str) -> JSONResponse:
        await self.controller.execute(code, sns_type)

        return self.response
