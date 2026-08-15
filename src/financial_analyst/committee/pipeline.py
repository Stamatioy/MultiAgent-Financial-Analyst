from __future__ import annotations

from datetime import datetime

from financial_analyst.committee.models import (
    CompanyInvestmentReport,
)
from financial_analyst.committee.service import (
    InvestmentCommitteeService,
)
from financial_analyst.research.coordinator import (
    ResearchCoordinator,
)
from collections.abc import Callable

from typing import Any

class InvestmentResearchPipeline:
    """
    Runs specialist research first and then sends the validated
    bundle to the Investment Committee.
    """

    def __init__(
        self,
        *,
        coordinator: ResearchCoordinator,
        committee: InvestmentCommitteeService,
    ) -> None:
        self.coordinator = coordinator
        self.committee = committee

    def analyze(
        self,
        *,
        ticker: str,
        fiscal_year: int,
        market_years: int = 5,
        benchmark_ticker: str = "^GSPC",
        risk_free_rate_annual: float = 0.0,
        news_query: str = (
            "material company developments, earnings, "
            "guidance, products, competition and risks"
        ),
        news_limit: int = 15,
        as_of: datetime | None = None,
        refresh_market: bool = True,
        refresh_fundamentals: bool = True,
        progress_callback: (
            Callable[
                [str, str, Any | None],
                None,
            ]
            | None
        ) = None,
    ) -> CompanyInvestmentReport:
        bundle = self.coordinator.research(
            ticker=ticker,
            fiscal_year=fiscal_year,
            market_years=market_years,

            benchmark_ticker=(
                benchmark_ticker
            ),

            risk_free_rate_annual=(
                risk_free_rate_annual
            ),

            news_query=news_query,
            news_limit=news_limit,

            as_of=as_of,

            refresh_market=(
                refresh_market
            ),

            refresh_fundamentals=(
                refresh_fundamentals
            ),

            progress_callback=(
                progress_callback
            ),
        )

        if progress_callback is not None:
            progress_callback(
                "committee",
                "running",
                None,
            )

        report = (
            self.committee.create_report(
                bundle
            )
        )

        if progress_callback is not None:
            progress_callback(
                "committee",
                "completed",
                report.committee,
            )

        return report