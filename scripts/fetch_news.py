from __future__ import annotations

import argparse

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.service import NewsService
from financial_analyst.news.yahoo_provider import (
    YahooNewsProvider,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch and cache recent company news."
        )
    )

    parser.add_argument(
        "ticker",
        help="Ticker such as AMD, MSFT or AAPL.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of provider results.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Do not contact the provider.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    ticker = normalize_ticker(
        args.ticker
    )

    if args.limit < 1 or args.limit > 100:
        raise ValueError(
            "--limit must be between 1 and 100."
        )

    connection = get_database_connection()

    try:
        repository = NewsRepository(
            connection
        )

        if not args.cached_only:
            service = NewsService(
                provider=YahooNewsProvider(),
                repository=repository,
            )

            articles = service.refresh(
                ticker=ticker,
                limit=args.limit,
            )

            print(
                f"Fetched {len(articles)} "
                f"unique articles.\n"
            )

        stored = repository.get_recent_articles(
            ticker=ticker,
            limit=args.limit,
        )

        if stored.empty:
            print(
                f"No cached news exists for {ticker}."
            )
            return

        print(
            stored.to_string(
                index=False
            )
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()