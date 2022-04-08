import os

from click.testing import CliRunner
from dotenv import load_dotenv

from src.gh_stats.cli import main

load_dotenv()

runner = CliRunner()


def test_yaml_input_success():
    result = runner.invoke(main, ["-r", "example.yaml"])
    assert result.exit_code == 0


def test_org_input_success():
    result = runner.invoke(main, ["-o", "the-migus-group"])
    assert result.exit_code == 0


def test_user_input_success():
    result = runner.invoke(main, ["-u", "endlesstrax"])
    assert result.exit_code == 0


def test_no_input_fails():
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)


def test_pass_token_via_cli_success():
    token = os.getenv("GH_TOKEN")
    os.environ.pop("GH_TOKEN")
    result = runner.invoke(main, ["-r", "example.yaml", "-t", token])
    assert result.exit_code == 0
    os.environ["GH_TOKEN"] = token  # Add back so other tests don't fail.


def test_value_error_when_no_GH_token():
    token = os.getenv("GH_TOKEN")
    os.environ.pop("GH_TOKEN")
    result = runner.invoke(main, ["-r", "example.yaml"])
    assert isinstance(result.exception, ValueError)
    os.environ["GH_TOKEN"] = token  # Add back so other tests don't fail.
