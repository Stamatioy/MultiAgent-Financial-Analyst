from __future__ import annotations

import argparse
from datetime import date, timedelta

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.fundamental_repository import (
    FundamentalRepository,
)
from financial_analyst.database.price_repository import (
    PriceRepository,
)
from financial_analyst.fundamentals.service import (
    FundamentalDataService,
)
from financial_analyst.market_data.service import (
    MarketDataService,
)
from financial_analyst.market_data.yahoo_provider import (
    YahooFinanceProvider,
)
from financial_analyst.sec.client import (
    SECClient,
)
from financial_analyst.sec.company_facts import (
    SECCompanyFactsParser,
)
from financial_analyst.sec.ticker_map import (
    SECTickerMapper,
)
from financial_analyst.valuation.service import (
    ValuationService,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate deterministic company valuation metrics."
        )
    )

    parser.add_argument("ticker")
    parser.add_argument("fiscal_year", type=int)

    parser.add_argument(
        "--market-years",
        type=int,
        default=5,
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    end_date = date.today()

    start_date = (
        end_date
        - timedelta(
            days=round(
                args.market_years * 365.25
            )
        )
    )

    connection = get_database_connection()

    try:
        price_repository = PriceRepository(
            connection
        )

        fundamental_repository = (
            FundamentalRepository(
                connection
            )
        )

        market_service = MarketDataService(
            provider=YahooFinanceProvider(),
            repository=price_repository,
        )

        with SECClient() as sec_client:
            fundamental_service = (
                FundamentalDataService(
                    ticker_mapper=SECTickerMapper(
                        sec_client
                    ),
                    company_facts=(
                        SECCompanyFactsParser(
                            sec_client
                        )
                    ),
                    repository=(
                        fundamental_repository
                    ),
                )
            )

            market_result = market_service.analyze(
                ticker=args.ticker,
                start_date=start_date,
                end_date=end_date,
                refresh=not args.cached_only,
            )

            fundamentals = (
                fundamental_service.analyze(
                    ticker=args.ticker,
                    fiscal_year=args.fiscal_year,
                    refresh=not args.cached_only,
                )
            )

        valuation = ValuationService().analyze(
            market_metrics=market_result.metrics,
            fundamental_metrics=fundamentals,
        )

        print(
            valuation.model_dump_json(
                indent=2
            )
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()