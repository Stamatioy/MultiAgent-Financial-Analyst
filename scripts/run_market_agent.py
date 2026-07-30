from __future__ import annotations

import argparse
from datetime import date, timedelta

from financial_analyst.agents.market_agent import MarketAnalystAgent
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
        description=(
            "Calculate market metrics and interpret them with the local "
            "Market Analyst agent."
        )
    )

    parser.add_argument(
        "ticker",
        help="Ticker such as AMD, AAPL or MSFT.",
    )

    parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Number of years of price history.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Do not download prices; use DuckDB data only.",
    )

    parser.add_argument(
        "--show-metrics",
        action="store_true",
        help="Print deterministic metrics before the agent output.",
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

        market_service = MarketDataService(
            provider=provider,
            repository=repository,
        )

        market_result = market_service.analyze(
            ticker=arguments.ticker,
            start_date=start_date,
            end_date=end_date,
            refresh=not arguments.cached_only,
        )

        if arguments.show_metrics:
            print("DETERMINISTIC MARKET METRICS")
            print(
                market_result.metrics.model_dump_json(indent=2)
            )
            print()

        agent = MarketAnalystAgent()

        interpretation = agent.analyze(
            market_result.metrics
        )

        print("MARKET ANALYST OUTPUT")
        print(interpretation.model_dump_json(indent=2))

    finally:
        connection.close()


if __name__ == "__main__":
    main()