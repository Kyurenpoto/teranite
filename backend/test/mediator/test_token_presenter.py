import json

import pytest
from adaptor.mediator.token_presenter import TokenPresenter
from adaptor.mediator.token_viewmodel import TokenViewModel
from dependencies.auth_container import AuthContainer
from dependencies.dependency import provider
from entity.auth_token import UserAuthToken
from fastapi import status
from hypothesis import given, strategies


class FakeTokenViewModel(TokenViewModel):
    async def update(self):
        pass


@pytest.mark.asyncio
@given(strategies.characters(), strategies.characters())
async def test_present(accessToken: str, refreshToken: str):
    provider.wire({"auth": AuthContainer({"token-viewmodel": FakeTokenViewModel})})

    presenter = TokenPresenter()

    await presenter.present(UserAuthToken(accessToken, refreshToken))
    viewModel = provider["auth"]["token-viewmodel"]

    assert viewModel.response.status_code == status.HTTP_200_OK

    assert json.loads(viewModel.response.body) == {
        "has_account": True,
        "access_token": str([accessToken]),
        "refresh_token": str([refreshToken]),
    }
