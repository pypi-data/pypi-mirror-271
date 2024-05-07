from unittest import mock
from unittest.mock import mock_open

from click.testing import CliRunner

from exponent.cli import login


async def test_exponent_login(cli_runner: CliRunner) -> None:
    with mock.patch("builtins.open", new_callable=mock_open):
        result = cli_runner.invoke(
            login, ["--key", "123456"], env={"EXPONENT_API_KEY": "123456"}
        )
        assert result.exit_code == 0
        assert "Saving API Key" in result.output
