from models.repository import Repository


def test_repository_creation():
    repo = Repository(
        name="mi-proyecto",
        description="Proyecto de ejemplo",
        stars=25,
        language="Python",
        url="https://github.com/user/mi-proyecto"
    )

    assert repo.name == "mi-proyecto"
    assert repo.description == "Proyecto de ejemplo"
    assert repo.stars == 25
    assert repo.language == "Python"
    assert repo.url == "https://github.com/user/mi-proyecto"


def test_repository_none_values():
    repo = Repository(
        name="proyecto-sin-descripcion",
        description=None,
        stars=0,
        language=None,
        url="https://github.com/user/proyecto-sin-descripcion"
    )

    assert repo.name == "proyecto-sin-descripcion"
    assert repo.description is None
    assert repo.stars == 0
    assert repo.language is None


def test_repository_default_values():
    repo = Repository(name="proyecto")

    assert repo.name == "proyecto"
    assert repo.description is None
    assert repo.stars == 0
    assert repo.language is None
    assert repo.url == ""