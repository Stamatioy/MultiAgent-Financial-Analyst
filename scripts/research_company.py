from __future__ import annotations

import argparse
from datetime import datetime, timezone

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.research.factory import (
    build_research_coordinator,
)
from financial_analyst.sec.client import (
    SECClient,
)


def parse_as_of(
    value: str | None,
) -> datetime | None:
    if value is None:
        return None

    text = value.strip()

    if text.endswith("Z"):
        text = (
            text[:-1]
            + "+00:00"
        )

    parsed = datetime.fromisoformat(
        text
    )

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed.astimezone(
        timezone.utc
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run coordinated multi-agent research "
            "for one company."
        )
    )

    parser.add_argument(
        "ticker",
    )

    parser.add_argument(
        "fiscal_year",
        type=int,
    )

    parser.add_argument(
        "--market-years",
        type=int,
        default=5,
    )

    parser.add_argument(
        "--news-limit",
        type=int,
        default=15,
    )

    parser.add_argument(
        "--news-query",
        type=str,
        default=(
            "material company developments, "
            "earnings, guidance, products, "
            "regulation and risks"
        ),
    )

    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--cached-market",
        action="store_true",
    )

    parser.add_argument(
        "--cached-fundamentals",
        action="store_true",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    connection = (
        get_database_connection()
    )

    try:
        with SECClient() as sec_client:
            coordinator = (
                build_research_coordinator(
                    connection=connection,
                    sec_client=sec_client,
                )
            )

            result = coordinator.research(
                ticker=args.ticker,
                fiscal_year=args.fiscal_year,
                market_years=(
                    args.market_years
                ),
                news_query=args.news_query,
                news_limit=args.news_limit,
                as_of=parse_as_of(
                    args.as_of
                ),
                refresh_market=(
                    not args.cached_market
                ),
                refresh_fundamentals=(
                    not args.cached_fundamentals
                ),
            )

        print(
            result.model_dump_json(
                indent=2
            )
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()