from __future__ import annotations

import argparse

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.fundamental_repository import (
    FundamentalRepository,
)
from financial_analyst.fundamentals.service import (
    FundamentalDataService,
)
from financial_analyst.sec.client import SECClient
from financial_analyst.sec.company_facts import (
    SECCompanyFactsParser,
)
from financial_analyst.sec.ticker_map import (
    SECTickerMapper,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze SEC fundamental financial data."
    )

    parser.add_argument(
        "ticker",
        help="U.S. SEC-listed company ticker.",
    )

    parser.add_argument(
        "fiscal_year",
        type=int,
        help="Fiscal year to analyze, e.g. 2025.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Do not query SEC; use DuckDB data only.",
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    connection = get_database_connection()

    try:
        repository = FundamentalRepository(connection)

        with SECClient() as sec_client:
            ticker_mapper = SECTickerMapper(sec_client)
            facts_parser = SECCompanyFactsParser(sec_client)

            service = FundamentalDataService(
                ticker_mapper=ticker_mapper,
                company_facts=facts_parser,
                repository=repository,
            )

            result = service.analyze(
                ticker=arguments.ticker,
                fiscal_year=arguments.fiscal_year,
                refresh=not arguments.cached_only,
            )

            print(result.model_dump_json(indent=2))

    finally:
        connection.close()


if __name__ == "__main__":
    main()