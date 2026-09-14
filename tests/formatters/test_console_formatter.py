# tests/formatters/test_console_formatter.py
from formatters.console_formatter import ConsoleFormatter
from models.repository import Repository


def make_repo(name="repo-x", stars=100, url="https://github.com/user/repo-x",
              description="Una descripción", language="Python"):
    return Repository(name=name, stars=stars, url=url, description=description, language=language)


def test_format_returns_message_when_list_is_empty():
    formatter = ConsoleFormatter()

    result = formatter.format([])

    assert result == "No se encontraron repositorios para los criterios indicados."


def test_format_includes_all_fields_for_single_repository():
    formatter = ConsoleFormatter()
    repo = make_repo(name="my-repo", stars=250, language="Go", description="Un CLI genial")

    result = formatter.format([repo])

    assert "my-repo" in result
    assert "250" in result
    assert "Go" in result
    assert "Un CLI genial" in result
    assert repo.url in result


def test_format_replaces_none_description_and_language():
    formatter = ConsoleFormatter()
    repo = make_repo(description=None, language=None)

    result = formatter.format([repo])

    assert "Sin descripción" in result
    assert "No especificado" in result
    assert "None" not in result


def test_format_joins_multiple_repositories():
    formatter = ConsoleFormatter()
    repos = [make_repo(name="repo-a"), make_repo(name="repo-b")]

    result = formatter.format(repos)

    assert "repo-a" in result
    assert "repo-b" in result
    assert result.index("repo-a") < result.index("repo-b")