from __future__ import annotations

from financial_analyst.database.fundamental_repository import (
    FundamentalRepository,
)
from financial_analyst.fundamentals.metrics import (
    calculate_fundamental_metrics,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.sec.company_facts import (
    SECCompanyFactsParser,
)
from financial_analyst.sec.ticker_map import (
    SECTickerMapper,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)

class FundamentalDataService:
    def __init__(
        self,
        *,
        ticker_mapper: SECTickerMapper,
        company_facts: SECCompanyFactsParser,
        repository: FundamentalRepository,
    ) -> None:
        self.ticker_mapper = ticker_mapper
        self.company_facts = company_facts
        self.repository = repository

    def analyze(
        self,
        *,
        ticker: str,
        fiscal_year: int,
        refresh: bool = True,
    ) -> FundamentalMetrics:
        identity = self.ticker_mapper.get_company(
            ticker
        )

        if refresh:
            facts = self.company_facts.fetch(
                ticker=identity.ticker,
                cik=identity.cik,
            )

            self.repository.upsert_facts(facts)

        stored = self.repository.get_facts(
            ticker=identity.ticker,
        )

        if stored.empty:
            raise RuntimeError(
                f"No SEC facts stored for {identity.ticker}."
            )

        return calculate_fundamental_metrics(
            ticker=identity.ticker,
            facts=stored,
            fiscal_year=fiscal_year,
        )

    def get_cached_facts(
        self,
        *,
        ticker: str,
    ):
        normalized_ticker = (
            normalize_ticker(
                ticker
            )
        )

        return (
            self.repository.get_facts(
                ticker=(
                    normalized_ticker
                )
            )
        )