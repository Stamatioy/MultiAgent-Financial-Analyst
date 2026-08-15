from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.committee.models import (
    CompanyInvestmentReport,
)


class StrictAPIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )


class ResearchRequest(StrictAPIModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    fiscal_year: int

    market_years: int = Field(
        default=5,
        ge=1,
        le=30,
    )

    benchmark_ticker: str = "^GSPC"

    risk_free_rate_annual: float = 0.0

    news_query: str = Field(
        default=(
            "material company developments, earnings, "
            "guidance, products, competition and risks"
        ),
        min_length=1,
        max_length=1000,
    )

    news_limit: int = Field(
        default=15,
        ge=1,
        le=50,
    )

    as_of: datetime | None = None

    refresh_market: bool = True
    refresh_fundamentals: bool = True


class ResearchResponse(StrictAPIModel):
    report: CompanyInvestmentReport