from __future__ import annotations

from datetime import date

from financial_analyst.database.price_repository import (
    PriceRepository,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.service import (
    MarketDataService,
)
from financial_analyst.risk.metrics import (
    calculate_risk_metrics,
)
from financial_analyst.risk.models import (
    RiskMetrics,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)


class RiskService:
    """
    Coordinates stock/benchmark price retrieval and
    deterministic risk calculations.
    """

    def __init__(
        self,
        *,
        market_service: MarketDataService,
        repository: PriceRepository,
    ) -> None:
        self.market_service = market_service
        self.repository = repository

    def analyze(
        self,
        *,
        ticker: str,
        benchmark_ticker: str,
        start_date: date,
        end_date: date,
        fundamentals: FundamentalMetrics,
        risk_free_rate_annual: float = 0.0,
        refresh_company: bool = False,
        refresh_benchmark: bool = True,
    ) -> RiskMetrics:
        normalized_ticker = (
            normalize_ticker(
                ticker
            )
        )

        normalized_benchmark = (
            normalize_ticker(
                benchmark_ticker
            )
        )

        if (
            normalized_ticker
            != fundamentals.ticker
        ):
            raise ValueError(
                "Ticker and fundamental metrics mismatch."
            )

        if refresh_company:
            self.market_service.analyze(
                ticker=normalized_ticker,
                start_date=start_date,
                end_date=end_date,
                refresh=True,
            )

        company_prices = (
            self.repository.get_prices(
                ticker=normalized_ticker,
                start_date=start_date,
                end_date=end_date,
            )
        )

        if company_prices.empty:
            self.market_service.analyze(
                ticker=normalized_ticker,
                start_date=start_date,
                end_date=end_date,
                refresh=True,
            )

            company_prices = (
                self.repository.get_prices(
                    ticker=normalized_ticker,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

        if refresh_benchmark:
            self.market_service.analyze(
                ticker=normalized_benchmark,
                start_date=start_date,
                end_date=end_date,
                refresh=True,
            )

        benchmark_prices = (
            self.repository.get_prices(
                ticker=normalized_benchmark,
                start_date=start_date,
                end_date=end_date,
            )
        )

        # A missing benchmark should not destroy the
        # entire company risk analysis.
        if benchmark_prices.empty:
            benchmark_prices = (
                company_prices.iloc[0:0].copy()
            )

        return calculate_risk_metrics(
            ticker=normalized_ticker,
            benchmark_ticker=(
                normalized_benchmark
            ),
            stock_prices=(
                company_prices
            ),
            benchmark_prices=(
                benchmark_prices
            ),
            fundamentals=fundamentals,
            risk_free_rate_annual=(
                risk_free_rate_annual
            ),
        )