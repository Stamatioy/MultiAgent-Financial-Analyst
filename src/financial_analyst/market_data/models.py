from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class MarketTrend(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    MIXED = "mixed"
    INSUFFICIENT_DATA = "insufficient_data"


class PriceRecord(BaseModel):
    ticker: str
    trading_date: date
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float
    volume: int = Field(ge=0)


class MarketMetrics(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    observations: int = Field(gt=0)

    latest_close: float = Field(gt=0)

    total_return: float | None
    annualized_return: float | None
    annualized_volatility: float | None
    maximum_drawdown: float | None

    return_1_month: float | None
    return_3_months: float | None
    return_6_months: float | None
    return_1_year: float | None

    moving_average_20: float | None
    moving_average_50: float | None
    moving_average_200: float | None

    distance_from_20_day_average: float | None
    distance_from_50_day_average: float | None
    distance_from_200_day_average: float | None

    trend: MarketTrend


class MarketAnalysisResult(BaseModel):
    ticker: str
    fetched_at: datetime
    source: str
    metrics: MarketMetrics