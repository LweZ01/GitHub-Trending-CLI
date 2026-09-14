# tests/test_cli.py
import pytest

from cli import main
from exceptions import GithubAPIError
from formatters.console_formatter import ConsoleFormatter
from models.repository import Repository
from services.github_client import IGithubClient
from services.trending_service import TrendingService


class FakeGithubClient(IGithubClient):
    def __init__(self, response=None, error=None):
        self._response = response or {"items": []}
        self._error = error

    def search_repositories(self, query, sort, order):
        if self._error:
            raise self._error
        return self._response


def make_item(name, stars):
    return {
        "name": name,
        "stargazers_count": stars,
        "html_url": f"https://github.com/user/{name}",
        "description": "desc",
        "language": "Python",
    }


def test_main_prints_formatted_repositories_and_returns_zero(capsys):
    response = {"items": [make_item("repo-a", 100)]}
    service = TrendingService(FakeGithubClient(response))

    exit_code = main(["--duration", "week", "--limit", "5"], service=service, formatter=ConsoleFormatter())

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "repo-a" in captured.out
    assert captured.err == ""


def test_main_prints_error_to_stderr_and_returns_one_on_api_error(capsys):
    service = TrendingService(FakeGithubClient(error=GithubAPIError("boom", status_code=500)))

    exit_code = main(["--duration", "week"], service=service, formatter=ConsoleFormatter())

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.err
    assert captured.out == ""


def test_main_rejects_invalid_duration_via_argparse():
    service = TrendingService(FakeGithubClient())

    with pytest.raises(SystemExit):
        main(["--duration", "century"], service=service, formatter=ConsoleFormatter())


def test_main_uses_default_duration_and_limit_when_not_provided(capsys):
    response = {"items": [make_item(f"repo{i}", 100 - i) for i in range(15)]}
    service = TrendingService(FakeGithubClient(response))

    exit_code = main([], service=service, formatter=ConsoleFormatter())

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "repo9" in captured.out
    assert "repo10" not in captured.out