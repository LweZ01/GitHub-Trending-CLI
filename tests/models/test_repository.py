from models.repository import Repository


def test_creates_repository_with_all_fields():
    repo = Repository(
        name="awesome-project",
        description="A really awesome project",
        stars=1500,
        language="Python",
        url="https://github.com/user/awesome-project",
    )

    assert repo.name == "awesome-project"
    assert repo.description == "A really awesome project"
    assert repo.stars == 1500
    assert repo.language == "Python"
    assert repo.url == "https://github.com/user/awesome-project"


def test_repository_defaults_when_optional_fields_missing():
    repo = Repository(name="minimal-repo")

    assert repo.description is None
    assert repo.language is None
    assert repo.stars == 0
    assert repo.url == ""


def test_two_repositories_with_same_values_are_equal():
    repo_a = Repository(name="x", stars=10, url="https://x.com")
    repo_b = Repository(name="x", stars=10, url="https://x.com")

    assert repo_a == repo_b