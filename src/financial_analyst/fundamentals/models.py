from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReportingPeriod(str, Enum):
    FY = "FY"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class FinancialFact(StrictModel):
    ticker: str
    cik: int

    concept: str
    unit: str

    fiscal_year: int | None
    fiscal_period: str | None

    form: str
    filing_date: date
    period_start: date | None
    period_end: date

    accession_number: str

    value: float


class FundamentalMetrics(StrictModel):
    ticker: str

    fiscal_year: int

    revenue: float | None
    net_income: float | None
    operating_income: float | None

    total_assets: float | None
    total_liabilities: float | None
    stockholders_equity: float | None

    cash_and_equivalents: float | None

    shares_outstanding: float | None = None

    current_debt: float | None = None
    noncurrent_debt: float | None = None
    total_debt: float | None = None

    operating_cash_flow: float | None
    capital_expenditures: float | None
    free_cash_flow: float | None

    revenue_growth: float | None
    net_income_growth: float | None

    operating_margin: float | None
    net_margin: float | None

    return_on_assets: float | None
    return_on_equity: float | None

    liabilities_to_equity: float | None

