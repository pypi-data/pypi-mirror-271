import asyncio
from collections.abc import Generator

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="session", autouse=True)
async def fixture_setup_env() -> None:
    session_mpatch = pytest.MonkeyPatch()
    session_mpatch.setenv("EXPONENT_API_KEY", "123456")
    session_mpatch.setenv("EXPONENT_BASE_URL", "https://exponent.run")
    session_mpatch.setenv("EXPONENT_API_BASE_URL", "https://api.exponent.run")
