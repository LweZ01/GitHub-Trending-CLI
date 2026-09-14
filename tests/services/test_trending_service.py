# tests/services/test_trending_service.py
import pytest

from exceptions import InvalidDurationError, InvalidLimitError
from services.github_client import IGithubClient
from services.trending_service import TrendingService


class FakeGithubClient(IGithubClient):
    """Doble de prueba: devuelve una respuesta fija sin hacer red real."""

    def __init__(self, response: dict):
        self._response = response
        self.last_call = None

    def search_repositories(self, query: str, sort: str, order: str) -> dict:
        self.last_call = {"query": query, "sort": sort, "order": order}
        return self._response


def make_item(name, stars, description="desc", language="Python"):
    return {
        "name": name,
        "stargazers_count": stars,
        "html_url": f"https://github.com/user/{name}",
        "description": description,
        "language": language,
    }


def test_get_trending_returns_parsed_repositories_sorted_by_stars():
    response = {"items": [make_item("low", 10), make_item("high", 500), make_item("mid", 100)]}
    client = FakeGithubClient(response)
    service = TrendingService(client)

    result = service.get_trending(duration="week", limit=10)

    assert [repo.name for repo in result] == ["high", "mid", "low"]


def test_get_trending_applies_limit():
    response = {"items": [make_item(f"repo{i}", 100 - i) for i in range(5)]}
    client = FakeGithubClient(response)
    service = TrendingService(client)

    result = service.get_trending(duration="week", limit=2)

    assert len(result) == 2


def test_get_trending_raises_on_invalid_duration():
    client = FakeGithubClient({"items": []})
    service = TrendingService(client)

    with pytest.raises(InvalidDurationError):
        service.get_trending(duration="century", limit=10)


def test_get_trending_raises_on_invalid_limit():
    client = FakeGithubClient({"items": []})
    service = TrendingService(client)

    with pytest.raises(InvalidLimitError):
        service.get_trending(duration="week", limit=0)


def test_get_trending_returns_empty_list_when_no_items():
    client = FakeGithubClient({"items": []})
    service = TrendingService(client)

    result = service.get_trending(duration="week", limit=10)

    assert result == []


def test_get_trending_builds_query_with_created_filter():
    client = FakeGithubClient({"items": []})
    service = TrendingService(client)

    service.get_trending(duration="day", limit=10)

    assert client.last_call["query"].startswith("created:>")
    assert client.last_call["sort"] == "stars"
    assert client.last_call["order"] == "desc"