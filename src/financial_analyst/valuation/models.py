from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ValuationMetrics(StrictModel):
    ticker: str

    fiscal_year: int
    price_date: date

    share_price: float = Field(gt=0)

    shares_outstanding: float | None

    market_cap: float | None
    enterprise_value: float | None

    trailing_pe: float | None
    earnings_yield: float | None

    price_to_sales: float | None
    price_to_book: float | None

    ev_to_sales: float | None
    ev_to_operating_income: float | None

    free_cash_flow_yield: float | None

    net_cash: float | None

    debt_used: float | None
    cash_used: float | None

    shares_missing: bool
    debt_missing: bool
    cash_missing: bool

    notes: list[str] = Field(
        default_factory=list,
        max_length=10,
    )