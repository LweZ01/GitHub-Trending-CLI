# exceptions.py

from typing import Optional


class TrendingRepoError(Exception):
    """Excepción base para todos los errores del dominio de la aplicación."""
    pass


class InvalidDurationError(TrendingRepoError):
    """Se lanza cuando el valor de duration no es uno de los permitidos."""

    def __init__(self, duration: str, valid_options: tuple[str, ...]):
        self.duration = duration
        self.valid_options = valid_options
        message = (
            f"'{duration}' no es un valor válido para duration. "
            f"Use uno de: {', '.join(valid_options)}."
        )
        super().__init__(message)


class GithubAPIError(TrendingRepoError):
    """Se lanza cuando falla la comunicación con la API de GitHub."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

class InvalidLimitError(TrendingRepoError):
    """Se lanza cuando el limit solicitado no es un entero positivo."""

    def __init__(self, limit: int):
        self.limit = limit
        super().__init__(f"El límite debe ser un entero positivo, se recibió: {limit}")