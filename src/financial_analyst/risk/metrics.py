from __future__ import annotations

import math

import numpy as np
import pandas as pd

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.risk.models import (
    RiskMetrics,
)


TRADING_DAYS_PER_YEAR = 252


class InsufficientRiskDataError(ValueError):
    """Raised when price history is insufficient for risk analysis."""


def calculate_risk_metrics(
    *,
    ticker: str,
    benchmark_ticker: str,
    stock_prices: pd.DataFrame,
    benchmark_prices: pd.DataFrame,
    fundamentals: FundamentalMetrics,
    risk_free_rate_annual: float = 0.0,
) -> RiskMetrics:
    stock = _prepare_prices(
        stock_prices,
        require_volume=True,
    )

    if len(stock) < 2:
        raise InsufficientRiskDataError(
            "At least two stock-price observations are required."
        )

    benchmark = _prepare_prices(
        benchmark_prices,
        require_volume=False,
    )

    stock_returns = (
        stock["adjusted_close"]
        .pct_change(fill_method=None)
        .dropna()
    )

    if stock_returns.empty:
        raise InsufficientRiskDataError(
            "Stock returns could not be calculated."
        )

    annualized_volatility = _annualized_volatility(
        stock_returns
    )

    risk_free_daily = (
        (1.0 + risk_free_rate_annual)
        ** (1.0 / TRADING_DAYS_PER_YEAR)
        - 1.0
    )

    excess_returns = (
        stock_returns
        - risk_free_daily
    )

    sharpe_ratio = _sharpe_ratio(
        excess_returns
    )

    downside_deviation = _downside_deviation(
        excess_returns
    )

    sortino_ratio = _sortino_ratio(
        excess_returns
    )

    daily_var_95, daily_cvar_95 = (
        _historical_var_cvar(
            stock_returns
        )
    )

    worst_daily_return = float(
        stock_returns.min()
    )

    worst_weekly_return = (
        _worst_period_return(
            stock,
            frequency="W-FRI",
        )
    )

    worst_monthly_return = (
        _worst_period_return(
            stock,
            frequency="ME",
        )
    )

    maximum_drawdown = (
        _maximum_drawdown(
            stock["adjusted_close"]
        )
    )

    max_drawdown_duration_days = (
        _maximum_drawdown_duration_days(
            stock
        )
    )

    average_daily_volume_20 = None
    average_daily_dollar_volume_20 = None

    if "volume" in stock.columns:
        recent = stock.tail(20)

        if not recent.empty:
            average_daily_volume_20 = float(
                recent["volume"].mean()
            )

            average_daily_dollar_volume_20 = float(
                (
                    recent["adjusted_close"]
                    * recent["volume"]
                ).mean()
            )

    beta = None
    correlation = None
    aligned_observations = 0

    if len(benchmark) >= 2:
        beta, correlation, aligned_observations = (
            _benchmark_statistics(
                stock=stock,
                benchmark=benchmark,
            )
        )

    debt = fundamentals.total_debt
    cash = fundamentals.cash_and_equivalents

    net_debt = None

    if debt is not None and cash is not None:
        net_debt = float(
            debt - cash
        )

    debt_to_free_cash_flow = _safe_divide(
        debt,
        fundamentals.free_cash_flow,
        require_positive_denominator=True,
    )

    notes: list[str] = []

    if aligned_observations < 30:
        notes.append(
            "Fewer than 30 aligned benchmark-return observations "
            "were available; beta and correlation may be unavailable."
        )

    if fundamentals.total_debt is None:
        notes.append(
            "Interest-bearing debt was unavailable."
        )

    if fundamentals.free_cash_flow is None:
        notes.append(
            "Free cash flow was unavailable for financial-risk analysis."
        )

    return RiskMetrics(
        ticker=ticker,
        benchmark_ticker=benchmark_ticker,

        start_date=stock["trading_date"].iloc[0].date(),
        end_date=stock["trading_date"].iloc[-1].date(),

        stock_observations=len(stock),
        aligned_benchmark_observations=(
            aligned_observations
        ),

        risk_free_rate_annual=(
            risk_free_rate_annual
        ),

        annualized_volatility=(
            annualized_volatility
        ),

        downside_deviation=(
            downside_deviation
        ),

        beta=beta,

        benchmark_correlation=(
            correlation
        ),

        sharpe_ratio=sharpe_ratio,
        sortino_ratio=sortino_ratio,

        daily_var_95=daily_var_95,
        daily_cvar_95=daily_cvar_95,

        worst_daily_return=(
            worst_daily_return
        ),

        worst_weekly_return=(
            worst_weekly_return
        ),

        worst_monthly_return=(
            worst_monthly_return
        ),

        maximum_drawdown=(
            maximum_drawdown
        ),

        max_drawdown_duration_days=(
            max_drawdown_duration_days
        ),

        average_daily_volume_20=(
            average_daily_volume_20
        ),

        average_daily_dollar_volume_20=(
            average_daily_dollar_volume_20
        ),

        net_debt=net_debt,

        debt_to_free_cash_flow=(
            debt_to_free_cash_flow
        ),

        benchmark_data_available=(
            aligned_observations >= 30
        ),

        notes=notes,
    )


def _prepare_prices(
    prices: pd.DataFrame,
    *,
    require_volume: bool,
) -> pd.DataFrame:
    if prices.empty:
        return pd.DataFrame()

    required = {
        "trading_date",
        "adjusted_close",
    }

    if require_volume:
        required.add("volume")

    missing = required.difference(
        prices.columns
    )

    if missing:
        raise ValueError(
            "Price data is missing columns: "
            f"{sorted(missing)}"
        )

    columns = [
        "trading_date",
        "adjusted_close",
    ]

    if "volume" in prices.columns:
        columns.append("volume")

    frame = prices[
        columns
    ].copy()

    frame["trading_date"] = pd.to_datetime(
        frame["trading_date"],
        errors="coerce",
    )

    frame["adjusted_close"] = pd.to_numeric(
        frame["adjusted_close"],
        errors="coerce",
    )

    if "volume" in frame.columns:
        frame["volume"] = pd.to_numeric(
            frame["volume"],
            errors="coerce",
        )

    frame = frame.dropna(
        subset=[
            "trading_date",
            "adjusted_close",
        ]
    )

    frame = frame[
        frame["adjusted_close"] > 0
    ]

    frame = (
        frame
        .drop_duplicates(
            subset=["trading_date"],
            keep="last",
        )
        .sort_values("trading_date")
        .reset_index(drop=True)
    )

    return frame


def _annualized_volatility(
    returns: pd.Series,
) -> float | None:
    if len(returns) < 2:
        return None

    std = returns.std(
        ddof=1
    )

    if pd.isna(std):
        return None

    return float(
        std
        * math.sqrt(
            TRADING_DAYS_PER_YEAR
        )
    )


def _sharpe_ratio(
    excess_returns: pd.Series,
) -> float | None:
    if len(excess_returns) < 2:
        return None

    standard_deviation = (
        excess_returns.std(
            ddof=1
        )
    )

    if (
        pd.isna(standard_deviation)
        or standard_deviation <= 0
    ):
        return None

    return float(
        excess_returns.mean()
        / standard_deviation
        * math.sqrt(
            TRADING_DAYS_PER_YEAR
        )
    )


def _downside_deviation(
    excess_returns: pd.Series,
) -> float | None:
    if excess_returns.empty:
        return None

    downside = np.minimum(
        excess_returns.to_numpy(
            dtype=float
        ),
        0.0,
    )

    mean_squared_downside = float(
        np.mean(
            np.square(
                downside
            )
        )
    )

    if mean_squared_downside <= 0:
        return 0.0

    return float(
        math.sqrt(
            mean_squared_downside
        )
        * math.sqrt(
            TRADING_DAYS_PER_YEAR
        )
    )


def _sortino_ratio(
    excess_returns: pd.Series,
) -> float | None:
    downside_daily = np.minimum(
        excess_returns.to_numpy(
            dtype=float
        ),
        0.0,
    )

    denominator = math.sqrt(
        float(
            np.mean(
                np.square(
                    downside_daily
                )
            )
        )
    )

    if denominator <= 0:
        return None

    return float(
        excess_returns.mean()
        / denominator
        * math.sqrt(
            TRADING_DAYS_PER_YEAR
        )
    )


def _historical_var_cvar(
    returns: pd.Series,
) -> tuple[
    float | None,
    float | None,
]:
    if len(returns) < 20:
        return None, None

    values = returns.to_numpy(
        dtype=float
    )

    fifth_percentile = float(
        np.percentile(
            values,
            5,
        )
    )

    tail = values[
        values <= fifth_percentile
    ]

    var_95 = max(
        0.0,
        -fifth_percentile,
    )

    cvar_95 = None

    if len(tail) > 0:
        cvar_95 = max(
            0.0,
            -float(
                np.mean(
                    tail
                )
            ),
        )

    return (
        float(var_95),
        (
            float(cvar_95)
            if cvar_95 is not None
            else None
        ),
    )


def _worst_period_return(
    stock: pd.DataFrame,
    *,
    frequency: str,
) -> float | None:
    indexed = (
        stock
        .set_index(
            "trading_date"
        )["adjusted_close"]
    )

    period_prices = (
        indexed
        .resample(
            frequency
        )
        .last()
        .dropna()
    )

    returns = (
        period_prices
        .pct_change(
            fill_method=None
        )
        .dropna()
    )

    if returns.empty:
        return None

    return float(
        returns.min()
    )


def _maximum_drawdown(
    prices: pd.Series,
) -> float | None:
    if prices.empty:
        return None

    peaks = prices.cummax()

    drawdowns = (
        prices
        / peaks
        - 1.0
    )

    return float(
        drawdowns.min()
    )


def _maximum_drawdown_duration_days(
    stock: pd.DataFrame,
) -> int | None:
    if len(stock) < 2:
        return None

    prices = stock[
        "adjusted_close"
    ].to_numpy(
        dtype=float
    )

    dates = stock[
        "trading_date"
    ].tolist()

    peak_price = prices[0]
    peak_date = dates[0]

    drawdown_start = None

    longest_days = 0

    for index in range(
        1,
        len(prices),
    ):
        price = prices[index]
        current_date = dates[index]

        if price >= peak_price:
            if drawdown_start is not None:
                duration = (
                    current_date
                    - drawdown_start
                ).days

                longest_days = max(
                    longest_days,
                    duration,
                )

            peak_price = price
            peak_date = current_date
            drawdown_start = None

        elif drawdown_start is None:
            drawdown_start = peak_date

    if drawdown_start is not None:
        duration = (
            dates[-1]
            - drawdown_start
        ).days

        longest_days = max(
            longest_days,
            duration,
        )

    return int(
        longest_days
    )


def _benchmark_statistics(
    *,
    stock: pd.DataFrame,
    benchmark: pd.DataFrame,
) -> tuple[
    float | None,
    float | None,
    int,
]:
    stock_frame = stock[
        [
            "trading_date",
            "adjusted_close",
        ]
    ].copy()

    stock_frame["stock_return"] = (
        stock_frame[
            "adjusted_close"
        ]
        .pct_change(
            fill_method=None
        )
    )

    stock_frame = stock_frame[
        [
            "trading_date",
            "stock_return",
        ]
    ]

    benchmark_frame = benchmark[
        [
            "trading_date",
            "adjusted_close",
        ]
    ].copy()

    benchmark_frame[
        "benchmark_return"
    ] = (
        benchmark_frame[
            "adjusted_close"
        ]
        .pct_change(
            fill_method=None
        )
    )

    benchmark_frame = (
        benchmark_frame[
            [
                "trading_date",
                "benchmark_return",
            ]
        ]
    )

    aligned = stock_frame.merge(
        benchmark_frame,
        on="trading_date",
        how="inner",
    ).dropna()

    count = len(
        aligned
    )

    if count < 30:
        return (
            None,
            None,
            count,
        )

    stock_returns = aligned[
        "stock_return"
    ]

    benchmark_returns = aligned[
        "benchmark_return"
    ]

    benchmark_variance = float(
        benchmark_returns.var(
            ddof=1
        )
    )

    stock_std = float(
        stock_returns.std(
            ddof=1
        )
    )

    benchmark_std = float(
        benchmark_returns.std(
            ddof=1
        )
    )

    if (
        benchmark_variance <= 0
        or math.isnan(
            benchmark_variance
        )
    ):
        beta = None
    else:
        covariance = float(
            stock_returns.cov(
                benchmark_returns
            )
        )

        beta = (
            covariance
            / benchmark_variance
        )

    if (
        stock_std <= 0
        or benchmark_std <= 0
        or math.isnan(stock_std)
        or math.isnan(benchmark_std)
    ):
        correlation = None
    else:
        correlation = float(
            stock_returns.corr(
                benchmark_returns
            )
        )

        if math.isnan(
            correlation
        ):
            correlation = None

    return (
        (
            float(beta)
            if beta is not None
            else None
        ),
        correlation,
        count,
    )


def _safe_divide(
    numerator: float | None,
    denominator: float | None,
    *,
    require_positive_denominator: bool = False,
) -> float | None:
    if (
        numerator is None
        or denominator is None
        or denominator == 0
    ):
        return None

    if (
        require_positive_denominator
        and denominator <= 0
    ):
        return None

    return float(
        numerator
        / denominator
    )