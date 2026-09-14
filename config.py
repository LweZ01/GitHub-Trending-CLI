from enum import Enum

from exceptions import InvalidDurationError


class DurationOption(str, Enum):
    """Opciones válidas para el rango de tiempo de búsqueda."""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


DURATION_TO_DAYS: dict[DurationOption, int] = {
    DurationOption.DAY: 1,
    DurationOption.WEEK: 7,
    DurationOption.MONTH: 30,
    DurationOption.YEAR: 365,
}

BASE_URL = "https://api.github.com/search/repositories"


def validate_duration(duration: str) -> DurationOption:
    """Valida que el string recibido sea una duration soportada.

    Lanza InvalidDurationError si no lo es.
    """
    try:
        return DurationOption(duration)
    except ValueError:
        valid_options = tuple(option.value for option in DurationOption)
        raise InvalidDurationError(duration, valid_options)