from datetime import date

import pytest

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
    MarketTrend,
)
from financial_analyst.valuation.metrics import (
    calculate_valuation_metrics,
)


def make_market_metrics() -> MarketMetrics:
    return MarketMetrics(
        ticker="TEST",
        start_date=date(2021, 1, 1),
        end_date=date(2025, 12, 31),
        observations=1000,

        latest_close=100.0,

        total_return=0.50,
        annualized_return=0.10,
        annualized_volatility=0.25,
        maximum_drawdown=-0.30,

        return_1_month=0.02,
        return_3_months=0.05,
        return_6_months=0.10,
        return_1_year=0.20,

        moving_average_20=98.0,
        moving_average_50=95.0,
        moving_average_200=90.0,

        distance_from_20_day_average=0.0204,
        distance_from_50_day_average=0.0526,
        distance_from_200_day_average=0.1111,

        trend=MarketTrend.BULLISH,
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


def test_calculate_valuation_metrics() -> None:
    result = calculate_valuation_metrics(
        market=make_market_metrics(),
        fundamentals=make_fundamentals(),
    )

    assert result.market_cap == pytest.approx(
        1000.0
    )

    assert result.enterprise_value == pytest.approx(
        980.0
    )

    assert result.trailing_pe == pytest.approx(
        20.0
    )

    assert result.earnings_yield == pytest.approx(
        0.05
    )

    assert result.price_to_sales == pytest.approx(
        2.0
    )

    assert result.price_to_book == pytest.approx(
        2.0
    )

    assert result.ev_to_sales == pytest.approx(
        1.96
    )

    assert (
        result.ev_to_operating_income
        == pytest.approx(
            980.0 / 60.0
        )
    )

    assert result.free_cash_flow_yield == pytest.approx(
        0.06
    )

    assert result.net_cash == pytest.approx(
        20.0
    )


def test_missing_shares_prevents_market_cap() -> None:
    fundamentals = make_fundamentals().model_copy(
        update={
            "shares_outstanding": None,
        }
    )

    result = calculate_valuation_metrics(
        market=make_market_metrics(),
        fundamentals=fundamentals,
    )

    assert result.market_cap is None
    assert result.trailing_pe is None
    assert result.shares_missing is True


def test_negative_income_has_no_pe() -> None:
    fundamentals = make_fundamentals().model_copy(
        update={
            "net_income": -10.0,
        }
    )

    result = calculate_valuation_metrics(
        market=make_market_metrics(),
        fundamentals=fundamentals,
    )

    assert result.trailing_pe is None
    assert result.earnings_yield == pytest.approx(
        -0.01
    )


def test_ticker_mismatch_rejected() -> None:
    fundamentals = make_fundamentals().model_copy(
        update={
            "ticker": "WRONG",
        }
    )

    with pytest.raises(
        ValueError,
        match="ticker mismatch",
    ):
        calculate_valuation_metrics(
            market=make_market_metrics(),
            fundamentals=fundamentals,
        )