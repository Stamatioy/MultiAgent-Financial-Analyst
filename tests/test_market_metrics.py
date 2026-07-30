from __future__ import annotations

import math

import pandas as pd
import pytest

from financial_analyst.analytics.market_metrics import (
    calculate_market_metrics,
)
from financial_analyst.market_data.models import MarketTrend


def make_prices(values: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "trading_date": pd.bdate_range(
                start="2025-01-01",
                periods=len(values),
            ),
            "adjusted_close": values,
        }
    )


def test_calculate_total_return() -> None:
    prices = make_prices([100.0, 105.0, 110.0])

    result = calculate_market_metrics(
        ticker="TEST",
        prices=prices,
    )

    assert result.total_return == pytest.approx(0.10)
    assert result.latest_close == 110.0
    assert result.observations == 3


def test_calculate_maximum_drawdown() -> None:
    prices = make_prices(
        [100.0, 120.0, 90.0, 108.0]
    )

    result = calculate_market_metrics(
        ticker="TEST",
        prices=prices,
    )

    # Peak 120 to trough 90 = -25%.
    assert result.maximum_drawdown == pytest.approx(-0.25)


def test_bullish_trend_classification() -> None:
    values = [float(value) for value in range(1, 251)]

    result = calculate_market_metrics(
        ticker="TEST",
        prices=make_prices(values),
    )

    assert result.trend == MarketTrend.BULLISH
    assert result.latest_close > result.moving_average_20
    assert result.moving_average_20 > result.moving_average_50
    assert result.moving_average_50 > result.moving_average_200


def test_short_history_has_insufficient_trend_data() -> None:
    result = calculate_market_metrics(
        ticker="TEST",
        prices=make_prices([100.0, 101.0, 102.0]),
    )

    assert result.trend == MarketTrend.INSUFFICIENT_DATA
    assert result.moving_average_20 is None
    assert result.return_1_year is None