from __future__ import annotations

import argparse

from financial_analyst.agents.fundamental_agent import (
    FundamentalAnalystAgent,
)
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
from financial_analyst.sec.ticker_map import SECTickerMapper


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze SEC fundamentals and interpret them with "
            "the local Fundamental Analyst agent."
        )
    )

    parser.add_argument(
        "ticker",
        help="U.S. SEC-listed ticker.",
    )

    parser.add_argument(
        "fiscal_year",
        type=int,
        help="Fiscal year to analyze.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Use only SEC facts already stored in DuckDB.",
    )

    parser.add_argument(
        "--show-metrics",
        action="store_true",
        help="Print deterministic metrics before agent analysis.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

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

            metrics = service.analyze(
                ticker=args.ticker,
                fiscal_year=args.fiscal_year,
                refresh=not args.cached_only,
            )

        if args.show_metrics:
            print("DETERMINISTIC FUNDAMENTAL METRICS")
            print(metrics.model_dump_json(indent=2))
            print()

        agent = FundamentalAnalystAgent()

        result = agent.analyze(metrics)

        print("FUNDAMENTAL ANALYST OUTPUT")
        print(result.model_dump_json(indent=2))

    finally:
        connection.close()


if __name__ == "__main__":
    main()