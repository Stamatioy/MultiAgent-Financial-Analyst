from __future__ import annotations

import math

import numpy as np
import pandas as pd

from financial_analyst.market_data.models import (
    MarketMetrics,
    MarketTrend,
)


TRADING_DAYS_PER_YEAR = 252


class InsufficientMarketDataError(ValueError):
    """Raised when there are not enough valid prices for analysis."""


def calculate_market_metrics(
    *,
    ticker: str,
    prices: pd.DataFrame,
) -> MarketMetrics:
    """Calculate deterministic return, risk and trend metrics."""

    if prices.empty:
        raise InsufficientMarketDataError(
            "At least two valid price observations are required."
        )

    required_columns = {"trading_date", "adjusted_close"}
    missing = required_columns.difference(prices.columns)

    if missing:
        raise ValueError(
            f"Price data is missing columns: {sorted(missing)}"
        )

    frame = prices.copy()

    frame["trading_date"] = pd.to_datetime(
        frame["trading_date"],
        errors="coerce",
    )

    frame["adjusted_close"] = pd.to_numeric(
        frame["adjusted_close"],
        errors="coerce",
    )

    frame = (
        frame
        .dropna(subset=["trading_date", "adjusted_close"])
        .loc[lambda item: item["adjusted_close"] > 0]
        .drop_duplicates(subset=["trading_date"], keep="last")
        .sort_values("trading_date")
        .reset_index(drop=True)
    )

    if len(frame) < 2:
        raise InsufficientMarketDataError(
            "At least two valid price observations are required."
        )

    close = frame["adjusted_close"].astype(float)
    daily_returns = close.pct_change(fill_method=None).dropna()

    total_return = _safe_return(close.iloc[0], close.iloc[-1])

    years = (frame["trading_date"].iloc[-1] -
             frame["trading_date"].iloc[0]).days / 365.25

    annualized_return = _annualized_return(
        initial_value=float(close.iloc[0]),
        final_value=float(close.iloc[-1]),
        years=years,
    )

    annualized_volatility = (
        float(daily_returns.std(ddof=1))
        * math.sqrt(TRADING_DAYS_PER_YEAR)
        if len(daily_returns) >= 2
        else None
    )

    running_peak = close.cummax()
    drawdowns = close / running_peak - 1.0
    maximum_drawdown = float(drawdowns.min())

    moving_average_20 = _rolling_average(close, 20)
    moving_average_50 = _rolling_average(close, 50)
    moving_average_200 = _rolling_average(close, 200)

    latest_close = float(close.iloc[-1])

    distance_20 = _distance_from_average(
        latest_close,
        moving_average_20,
    )
    distance_50 = _distance_from_average(
        latest_close,
        moving_average_50,
    )
    distance_200 = _distance_from_average(
        latest_close,
        moving_average_200,
    )

    return MarketMetrics(
        ticker=ticker,
        start_date=frame["trading_date"].iloc[0].date(),
        end_date=frame["trading_date"].iloc[-1].date(),
        observations=len(frame),
        latest_close=latest_close,
        total_return=total_return,
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        maximum_drawdown=maximum_drawdown,
        return_1_month=_period_return(close, 21),
        return_3_months=_period_return(close, 63),
        return_6_months=_period_return(close, 126),
        return_1_year=_period_return(close, 252),
        moving_average_20=moving_average_20,
        moving_average_50=moving_average_50,
        moving_average_200=moving_average_200,
        distance_from_20_day_average=distance_20,
        distance_from_50_day_average=distance_50,
        distance_from_200_day_average=distance_200,
        trend=_classify_trend(
            latest_close=latest_close,
            moving_average_20=moving_average_20,
            moving_average_50=moving_average_50,
            moving_average_200=moving_average_200,
        ),
    )


def _safe_return(
    initial_value: float,
    final_value: float,
) -> float | None:
    if initial_value <= 0:
        return None

    return float(final_value / initial_value - 1.0)


def _annualized_return(
    *,
    initial_value: float,
    final_value: float,
    years: float,
) -> float | None:
    if initial_value <= 0 or final_value <= 0 or years <= 0:
        return None

    return float((final_value / initial_value) ** (1.0 / years) - 1.0)


def _period_return(
    prices: pd.Series,
    periods: int,
) -> float | None:
    if len(prices) <= periods:
        return None

    earlier_price = float(prices.iloc[-periods - 1])
    latest_price = float(prices.iloc[-1])

    return _safe_return(earlier_price, latest_price)


def _rolling_average(
    prices: pd.Series,
    window: int,
) -> float | None:
    if len(prices) < window:
        return None

    value = prices.rolling(
        window=window,
        min_periods=window,
    ).mean().iloc[-1]

    if pd.isna(value):
        return None

    return float(value)


def _distance_from_average(
    latest_close: float,
    average: float | None,
) -> float | None:
    if average is None or average <= 0:
        return None

    return float(latest_close / average - 1.0)


def _classify_trend(
    *,
    latest_close: float,
    moving_average_20: float | None,
    moving_average_50: float | None,
    moving_average_200: float | None,
) -> MarketTrend:
    averages = [
        moving_average_20,
        moving_average_50,
        moving_average_200,
    ]

    if any(value is None for value in averages):
        return MarketTrend.INSUFFICIENT_DATA

    assert moving_average_20 is not None
    assert moving_average_50 is not None
    assert moving_average_200 is not None

    bullish = (
        latest_close > moving_average_20
        > moving_average_50
        > moving_average_200
    )

    bearish = (
        latest_close < moving_average_20
        < moving_average_50
        < moving_average_200
    )

    if bullish:
        return MarketTrend.BULLISH

    if bearish:
        return MarketTrend.BEARISH

    return MarketTrend.MIXED