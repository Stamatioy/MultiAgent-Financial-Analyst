from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RiskMetrics(StrictModel):
    ticker: str
    benchmark_ticker: str

    start_date: date
    end_date: date

    stock_observations: int = Field(gt=1)
    aligned_benchmark_observations: int = Field(ge=0)

    risk_free_rate_annual: float

    annualized_volatility: float | None
    downside_deviation: float | None

    beta: float | None
    benchmark_correlation: float | None

    sharpe_ratio: float | None
    sortino_ratio: float | None

    daily_var_95: float | None
    daily_cvar_95: float | None

    worst_daily_return: float | None
    worst_weekly_return: float | None
    worst_monthly_return: float | None

    maximum_drawdown: float | None
    max_drawdown_duration_days: int | None

    average_daily_volume_20: float | None
    average_daily_dollar_volume_20: float | None

    net_debt: float | None
    debt_to_free_cash_flow: float | None

    benchmark_data_available: bool

    notes: list[str] = Field(
        default_factory=list,
        max_length=10,
    )