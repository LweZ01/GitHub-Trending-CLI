from dataclasses import dataclass
from typing import Optional


@dataclass
class Repository:
    name: str
    stars: int
    url: str
    description: Optional[str] = None
    language: Optional[str] = None