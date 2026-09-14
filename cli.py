# cli.py
import argparse
import sys
from typing import Optional

import requests

from config import BASE_URL
from exceptions import TrendingRepoError
from formatters.base import IFormatter
from formatters.console_formatter import ConsoleFormatter
from services.github_client import GithubClient
from services.trending_service import TrendingService


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trending-repos",
        description="Muestra los repositorios más populares de GitHub en un rango de tiempo.",
    )
    parser.add_argument(
        "--duration",
        default="week",
        choices=["day", "week", "month", "year"],
        help="Rango de tiempo a considerar (default: week).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Cantidad máxima de repositorios a mostrar (default: 10).",
    )
    return parser


def main(
    argv: Optional[list[str]] = None,
    service: Optional[TrendingService] = None,
    formatter: Optional[IFormatter] = None,
) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if service is None:
        session = requests.Session()
        client = GithubClient(base_url=BASE_URL, session=session)
        service = TrendingService(client)

    if formatter is None:
        formatter = ConsoleFormatter()

    try:
        repositories = service.get_trending(duration=args.duration, limit=args.limit)
    except TrendingRepoError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(formatter.format(repositories))
    return 0


if __name__ == "__main__":
    sys.exit(main())