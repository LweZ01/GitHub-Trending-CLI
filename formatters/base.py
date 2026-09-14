# formatters/base.py
from abc import ABC, abstractmethod

from models.repository import Repository


class IFormatter(ABC):
    """Contrato para cualquier forma de presentar una lista de repositorios."""

    @abstractmethod
    def format(self, repositories: list[Repository]) -> str:
        raise NotImplementedError