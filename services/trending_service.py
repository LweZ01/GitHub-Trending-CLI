from datetime import date, timedelta

from config import DURATION_TO_DAYS, DurationOption, validate_duration
from exceptions import InvalidLimitError
from models.repository import Repository
from services.github_client import IGithubClient


class TrendingService:
    """Orquesta la obtención de repositorios trending: valida input,
    construye la búsqueda, parsea la respuesta, ordena y aplica el límite."""

    def __init__(self, client: IGithubClient):
        self._client = client

    def get_trending(self, duration: str, limit: int) -> list[Repository]:
        duration_option = validate_duration(duration)
        self._validate_limit(limit)

        query = self._build_query(duration_option)
        raw_response = self._client.search_repositories(query=query, sort="stars", order="desc")

        repositories = self._parse_repositories(raw_response)
        repositories.sort(key=lambda repo: repo.stars, reverse=True)

        return repositories[:limit]

    def _validate_limit(self, limit: int) -> None:
        if limit <= 0:
            raise InvalidLimitError(limit)

    def _build_query(self, duration_option: DurationOption) -> str:
        days = DURATION_TO_DAYS[duration_option]
        cutoff_date = date.today() - timedelta(days=days)
        return f"created:>{cutoff_date.isoformat()}"

    def _parse_repositories(self, raw_response: dict) -> list[Repository]:
        items = raw_response.get("items", [])
        return [
            Repository(
                name=item["name"],
                stars=item["stargazers_count"],
                url=item["html_url"],
                description=item.get("description"),
                language=item.get("language"),
            )
            for item in items
        ]