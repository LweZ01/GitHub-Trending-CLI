# tests/services/test_github_client.py
import pytest
import requests
import responses

from config import BASE_URL
from exceptions import GithubAPIError
from services.github_client import GithubClient


@pytest.fixture
def client():
    session = requests.Session()
    return GithubClient(base_url=BASE_URL, session=session)


@responses.activate
def test_search_repositories_returns_parsed_json(client):
    fake_response = {"total_count": 1, "items": [{"name": "repo-x"}]}
    responses.add(responses.GET, BASE_URL, json=fake_response, status=200)

    result = client.search_repositories(query="created:>2024-01-01", sort="stars", order="desc")

    assert result == fake_response


@responses.activate
def test_search_repositories_sends_correct_query_params(client):
    responses.add(responses.GET, BASE_URL, json={"items": []}, status=200)

    client.search_repositories(query="created:>2024-01-01", sort="stars", order="desc")

    sent_request = responses.calls[0].request
    assert "q=created" in sent_request.url
    assert "sort=stars" in sent_request.url
    assert "order=desc" in sent_request.url


@responses.activate
def test_search_repositories_raises_on_http_error_status(client):
    responses.add(responses.GET, BASE_URL, json={"message": "rate limit"}, status=403)

    with pytest.raises(GithubAPIError) as exc_info:
        client.search_repositories(query="created:>2024-01-01", sort="stars", order="desc")

    assert exc_info.value.status_code == 403


@responses.activate
def test_search_repositories_raises_on_connection_error(client):
    responses.add(
        responses.GET,
        BASE_URL,
        body=requests.exceptions.ConnectionError("boom"),
    )

    with pytest.raises(GithubAPIError) as exc_info:
        client.search_repositories(query="created:>2024-01-01", sort="stars", order="desc")

    assert exc_info.value.status_code is None