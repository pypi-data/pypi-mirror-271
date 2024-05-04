from click.testing import CliRunner

from justtrade.cli import echo


def test_simple():
    runner = CliRunner()
    result = runner.invoke(echo)
    assert 0 == result.exit_code
