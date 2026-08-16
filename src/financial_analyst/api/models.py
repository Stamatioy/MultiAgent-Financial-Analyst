from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.committee.models import (
    CompanyInvestmentReport,
)
from typing import Any, Literal

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

from enum import Enum


class ResearchJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchStepStatus(str, Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchStep(StrictAPIModel):
    name: str
    label: str

    status: ResearchStepStatus = (
        ResearchStepStatus.WAITING
    )


class ResearchJobCreated(StrictAPIModel):
    job_id: str

    status: ResearchJobStatus


class ResearchJobStatusResponse(
    StrictAPIModel
):
    job_id: str = Field(
        min_length=1
    )

    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    status: ResearchJobStatus

    current_step: (
        str | None
    ) = None

    progress: float = Field(
        ge=0.0,
        le=1.0,
    )

    steps: list[
        ResearchStep
    ]

    partial_results: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict
    )

    error: str | None = None

class ResearchJobResultResponse(StrictAPIModel):
    job_id: str

    report: CompanyInvestmentReport

class ResearchHistoryItem(
    StrictAPIModel
):
    research_id: str

    ticker: str

    generated_at: datetime

    recommendation: str

    conviction: str

    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    investment_horizon: str


class ResearchHistoryResponse(
    StrictAPIModel
):
    items: list[
        ResearchHistoryItem
    ]


class ResearchHistoryReportResponse(
    StrictAPIModel
):
    research_id: str

    report: CompanyInvestmentReport

class WatchlistAddRequest(
    StrictAPIModel
):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )


class WatchlistItem(
    StrictAPIModel
):
    ticker: str

    added_at: datetime

    research_id: (
        str | None
    ) = None

    last_researched_at: (
        datetime | None
    ) = None

    recommendation: (
        str | None
    ) = None

    conviction: (
        str | None
    ) = None

    confidence_score: (
        float | None
    ) = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    investment_horizon: (
        str | None
    ) = None


class WatchlistResponse(
    StrictAPIModel
):
    items: list[
        WatchlistItem
    ]