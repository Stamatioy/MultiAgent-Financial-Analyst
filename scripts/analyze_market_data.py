from __future__ import annotations

import argparse
from datetime import date, timedelta

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.price_repository import PriceRepository
from financial_analyst.market_data.service import MarketDataService
from financial_analyst.market_data.yahoo_provider import (
    YahooFinanceProvider,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and analyze historical stock prices."
    )

    parser.add_argument(
        "ticker",
        help="Market ticker, for example AMD, AAPL or MSFT.",
    )

    parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Number of years of historical prices to analyze.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Use only prices already stored in DuckDB.",
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    if arguments.years < 1 or arguments.years > 30:
        raise ValueError("--years must be between 1 and 30.")

    end_date = date.today()
    start_date = end_date - timedelta(
        days=round(arguments.years * 365.25)
    )

    connection = get_database_connection()

    try:
        repository = PriceRepository(connection)
        provider = YahooFinanceProvider()

        service = MarketDataService(
            provider=provider,
            repository=repository,
        )

        result = service.analyze(
            ticker=arguments.ticker,
            start_date=start_date,
            end_date=end_date,
            refresh=not arguments.cached_only,
        )

        print(result.model_dump_json(indent=2))
    finally:
        connection.close()


if __name__ == "__main__":
    main()