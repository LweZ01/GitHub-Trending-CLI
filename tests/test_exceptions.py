# tests/test_exceptions.py
import pytest
from exceptions import InvalidDurationError, GithubAPIError, TrendingRepoError


def test_invalid_duration_error_stores_duration_and_options():
    error = InvalidDurationError("month3", ("day", "week", "month", "year"))

    assert error.duration == "month3"
    assert error.valid_options == ("day", "week", "month", "year")
    assert "month3" in str(error)


def test_invalid_duration_error_is_a_trending_repo_error():
    assert issubclass(InvalidDurationError, TrendingRepoError)


def test_github_api_error_stores_status_code():
    error = GithubAPIError("Rate limit exceeded", status_code=403)

    assert error.status_code == 403
    assert "Rate limit exceeded" in str(error)


def test_github_api_error_status_code_defaults_to_none():
    error = GithubAPIError("Connection timeout")

    assert error.status_code is None


def test_github_api_error_is_a_trending_repo_error():
    assert issubclass(GithubAPIError, TrendingRepoError)