import pytest
from main import app, unwire, wire


@pytest.fixture
async def container():
    wire()
    yield app.state.container
    unwire()
