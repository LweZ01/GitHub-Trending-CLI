from formatters.base import IFormatter
from models.repository import Repository


class ConsoleFormatter(IFormatter):
    """Presenta los repositorios como texto plano legible en terminal."""

    def format(self, repositories: list[Repository]) -> str:
        if not repositories:
            return "No se encontraron repositorios para los criterios indicados."

        blocks = [self._format_single(repo) for repo in repositories]
        return "\n\n".join(blocks)

    def _format_single(self, repo: Repository) -> str:
        description = repo.description or "Sin descripción"
        language = repo.language or "No especificado"

        return (
            f"{repo.name}\n"
            f"  Estrellas: {repo.stars}\n"
            f"  Lenguaje: {language}\n"
            f"  Descripción: {description}\n"
            f"  URL: {repo.url}"
        )