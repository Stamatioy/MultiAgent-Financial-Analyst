from __future__ import annotations

from datetime import date

import duckdb
import pandas as pd

from financial_analyst.database.price_repository import (
    PriceRepository,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.risk.service import (
    RiskService,
)


def make_price_frame(
    ticker: str,
) -> pd.DataFrame:
    dates = pd.bdate_range(
        "2025-01-01",
        periods=260,
    )

    prices = [
        100.0
        + index * 0.1
        for index in range(
            len(dates)
        )
    ]

    return pd.DataFrame(
        {
            "ticker": ticker,
            "trading_date": (
                dates.date
            ),
            "open": prices,
            "high": prices,
            "low": prices,
            "close": prices,
            "adjusted_close": prices,
            "volume": [
                1_000_000
            ] * len(dates),
        }
    )


def make_fundamentals() -> FundamentalMetrics:
    return FundamentalMetrics(
        ticker="TEST",
        fiscal_year=2025,

        revenue=500.0,
        net_income=50.0,
        operating_income=60.0,

        total_assets=800.0,
        total_liabilities=300.0,
        stockholders_equity=500.0,

        cash_and_equivalents=40.0,

        shares_outstanding=10.0,

        current_debt=5.0,
        noncurrent_debt=15.0,
        total_debt=20.0,

        operating_cash_flow=80.0,
        capital_expenditures=20.0,
        free_cash_flow=60.0,

        revenue_growth=0.20,
        net_income_growth=0.25,

        operating_margin=0.12,
        net_margin=0.10,

        return_on_assets=0.07,
        return_on_equity=0.11,

        liabilities_to_equity=0.60,
    )


class FakeMarketService:
    def analyze(
        self,
        **kwargs,
    ):
        raise AssertionError(
            "Market service should not be called "
            "when cached prices exist."
        )


def test_risk_service_uses_cached_prices() -> None:
    connection = duckdb.connect(
        ":memory:"
    )

    try:
        repository = PriceRepository(
            connection
        )

        repository.upsert_prices(
            make_price_frame(
                "TEST"
            )
        )

        repository.upsert_prices(
            make_price_frame(
                "^GSPC"
            )
        )

        service = RiskService(
            market_service=FakeMarketService(),
            repository=repository,
        )

        result = service.analyze(
            ticker="TEST",
            benchmark_ticker="^GSPC",

            start_date=date(
                2025,
                1,
                1,
            ),

            end_date=date(
                2025,
                12,
                31,
            ),

            fundamentals=(
                make_fundamentals()
            ),

            refresh_company=False,
            refresh_benchmark=False,
        )

        assert result.ticker == "TEST"

        assert (
            result.benchmark_ticker
            == "^GSPC"
        )

        assert (
            result.stock_observations
            == 260
        )

    finally:
        connection.close()