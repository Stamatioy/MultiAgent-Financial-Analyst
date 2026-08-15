from __future__ import annotations

import argparse
from datetime import (
    datetime,
    timezone,
)

from financial_analyst.committee.factory import (
    build_investment_pipeline,
)
from financial_analyst.database.connection import (
    get_database_connection,
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

    result = datetime.fromisoformat(
        text
    )

    if result.tzinfo is None:
        result = result.replace(
            tzinfo=timezone.utc
        )

    return result.astimezone(
        timezone.utc
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run complete multi-agent company research "
            "and Investment Committee analysis."
        )
    )

    parser.add_argument(
        "ticker"
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
        "--benchmark",
        default="^GSPC",
    )

    parser.add_argument(
        "--risk-free-rate",
        type=float,
        default=0.0,
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
            "material company developments, earnings, "
            "guidance, products, competition and risks"
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

    parser.add_argument(
        "--committee-only",
        action="store_true",
        help=(
            "Print only the Investment Committee output "
            "rather than the complete research report."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    connection = (
        get_database_connection()
    )

    try:
        with SECClient() as sec_client:
            pipeline = build_investment_pipeline(
                connection=connection,
                sec_client=sec_client,
            )

            result = pipeline.analyze(
                ticker=args.ticker,

                fiscal_year=(
                    args.fiscal_year
                ),

                market_years=(
                    args.market_years
                ),

                benchmark_ticker=(
                    args.benchmark
                ),

                risk_free_rate_annual=(
                    args.risk_free_rate
                ),

                news_query=(
                    args.news_query
                ),

                news_limit=(
                    args.news_limit
                ),

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

        if args.committee_only:
            print(
                result.committee.model_dump_json(
                    indent=2
                )
            )

        else:
            print(
                result.model_dump_json(
                    indent=2
                )
            )

    finally:
        connection.close()


if __name__ == "__main__":
    main()