from abc import ABC, abstractmethod

import requests

from exceptions import GithubAPIError


class IGithubClient(ABC):
    """Contrato para cualquier cliente que consulte repositorios en GitHub."""

    @abstractmethod
    def search_repositories(self, query: str, sort: str, order: str) -> dict:
        """Busca repositorios y devuelve la respuesta JSON como dict."""
        raise NotImplementedError


class GithubClient(IGithubClient):
    """Implementación concreta que habla con la API REST de GitHub vía HTTP."""

    def __init__(self, base_url: str, session: requests.Session, timeout: int = 10):
        self._base_url = base_url
        self._session = session
        self._timeout = timeout

    def search_repositories(self, query: str, sort: str, order: str) -> dict:
        params = {"q": query, "sort": sort, "order": order}

        try:
            response = self._session.get(self._base_url, params=params, timeout=self._timeout)
        except requests.exceptions.RequestException as exc:
            raise GithubAPIError(f"Error de red al contactar GitHub: {exc}") from exc

        if response.status_code != 200:
            raise GithubAPIError(
                f"GitHub respondió con error: {response.status_code}",
                status_code=response.status_code,
            )

        return response.json()