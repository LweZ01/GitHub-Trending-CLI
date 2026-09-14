from dataclasses import dataclass
from typing import Optional


@dataclass
class Repository:
    name: str
    description: Optional[str] = None
    stars: int = 0
    language: Optional[str] = None
    url: str = ""