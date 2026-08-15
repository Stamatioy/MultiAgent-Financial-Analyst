from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import pytest

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.risk.metrics import (
    calculate_risk_metrics,
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


def prices_from_returns(
    *,
    ticker: str,
    returns: list[float],
) -> pd.DataFrame:
    values = [100.0]

    for daily_return in returns:
        values.append(
            values[-1]
            * (1.0 + daily_return)
        )

    dates = pd.bdate_range(
        "2025-01-01",
        periods=len(values),
    )

    return pd.DataFrame(
        {
            "ticker": ticker,
            "trading_date": dates,
            "open": values,
            "high": values,
            "low": values,
            "close": values,
            "adjusted_close": values,
            "volume": [
                1_000_000
                for _ in values
            ],
        }
    )


def test_beta_and_correlation() -> None:
    benchmark_returns = [
        0.01 if index % 2 == 0
        else -0.005
        for index in range(260)
    ]

    stock_returns = [
        value * 2.0
        for value in benchmark_returns
    ]

    result = calculate_risk_metrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        stock_prices=prices_from_returns(
            ticker="TEST",
            returns=stock_returns,
        ),

        benchmark_prices=prices_from_returns(
            ticker="^GSPC",
            returns=benchmark_returns,
        ),

        fundamentals=make_fundamentals(),

        risk_free_rate_annual=0.0,
    )

    assert result.beta == pytest.approx(
        2.0,
        rel=1e-6,
    )

    assert (
        result.benchmark_correlation
        == pytest.approx(
            1.0,
            rel=1e-6,
        )
    )

    assert (
        result.aligned_benchmark_observations
        >= 250
    )


def test_var_and_cvar_are_positive_loss_magnitudes() -> None:
    returns = [
        -0.08,
        -0.06,
        -0.05,
        -0.04,
        -0.03,
    ] + [
        0.001
        for _ in range(255)
    ]

    result = calculate_risk_metrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        stock_prices=prices_from_returns(
            ticker="TEST",
            returns=returns,
        ),

        benchmark_prices=prices_from_returns(
            ticker="^GSPC",
            returns=[
                0.001
                for _ in range(260)
            ],
        ),

        fundamentals=make_fundamentals(),
    )

    assert result.daily_var_95 is not None
    assert result.daily_var_95 >= 0

    assert result.daily_cvar_95 is not None
    assert result.daily_cvar_95 >= 0

    assert (
        result.daily_cvar_95
        >= result.daily_var_95
    )


def test_financial_risk_metrics() -> None:
    returns = [
        0.001
        if index % 2 == 0
        else -0.001
        for index in range(260)
    ]

    result = calculate_risk_metrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        stock_prices=prices_from_returns(
            ticker="TEST",
            returns=returns,
        ),

        benchmark_prices=prices_from_returns(
            ticker="^GSPC",
            returns=returns,
        ),

        fundamentals=make_fundamentals(),
    )

    assert result.net_debt == pytest.approx(
        -20.0
    )

    assert (
        result.debt_to_free_cash_flow
        == pytest.approx(
            20.0 / 60.0
        )
    )


def test_missing_benchmark_is_allowed() -> None:
    returns = [
        0.001
        for _ in range(260)
    ]

    empty_benchmark = pd.DataFrame(
        columns=[
            "trading_date",
            "adjusted_close",
        ]
    )

    result = calculate_risk_metrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        stock_prices=prices_from_returns(
            ticker="TEST",
            returns=returns,
        ),

        benchmark_prices=(
            empty_benchmark
        ),

        fundamentals=make_fundamentals(),
    )

    assert result.beta is None

    assert (
        result.benchmark_correlation
        is None
    )

    assert (
        result.benchmark_data_available
        is False
    )

def test_maximum_drawdown() -> None:
    frame = pd.DataFrame(
        {
            "ticker": ["TEST"] * 5,

            "trading_date": pd.bdate_range(
                "2025-01-01",
                periods=5,
            ),

            "open": [
                100.0,
                120.0,
                90.0,
                100.0,
                120.0,
            ],

            "high": [
                100.0,
                120.0,
                90.0,
                100.0,
                120.0,
            ],

            "low": [
                100.0,
                120.0,
                90.0,
                100.0,
                120.0,
            ],

            "close": [
                100.0,
                120.0,
                90.0,
                100.0,
                120.0,
            ],

            "adjusted_close": [
                100.0,
                120.0,
                90.0,
                100.0,
                120.0,
            ],

            "volume": [
                1_000_000
            ] * 5,
        }
    )

    result = calculate_risk_metrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        stock_prices=frame,

        benchmark_prices=(
            frame.copy()
        ),

        fundamentals=make_fundamentals(),
    )

    assert (
        result.maximum_drawdown
        == pytest.approx(
            -0.25
        )
    )