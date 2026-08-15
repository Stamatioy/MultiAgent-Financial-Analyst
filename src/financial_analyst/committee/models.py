from __future__ import annotations

from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from datetime import datetime

from financial_analyst.research.models import (
    CompanyResearchBundle,
)

class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )


class InvestmentRecommendation(str, Enum):
    STRONGLY_ATTRACTIVE = "strongly_attractive"
    ATTRACTIVE = "attractive"
    WATCHLIST = "watchlist"
    NEUTRAL = "neutral"
    UNATTRACTIVE = "unattractive"
    STRONGLY_UNATTRACTIVE = "strongly_unattractive"
    INSUFFICIENT_DATA = "insufficient_data"


class InvestmentHorizon(str, Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


class ConvictionLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class EvidenceSourceType(str, Enum):
    MARKET_METRIC = "market_metric"
    FUNDAMENTAL_METRIC = "fundamental_metric"
    VALUATION_METRIC = "valuation_metric"
    RISK_METRIC = "risk_metric"
    NEWS_EVENT = "news_event"


class CommitteeEvidenceItem(StrictModel):
    source_type: EvidenceSourceType

    field: str = Field(
        min_length=1,
        max_length=100,
    )

    source_id: str | None = Field(
        default=None,
        max_length=100,
    )

    interpretation: str = Field(
        min_length=1,
        max_length=500,
    )


class InvestmentCommitteeOutput(StrictModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    recommendation: InvestmentRecommendation

    conviction: ConvictionLevel

    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    investment_horizon: InvestmentHorizon

    thesis: str = Field(
        min_length=1,
        max_length=1200,
    )

    bull_case: str = Field(
        min_length=1,
        max_length=1200,
    )

    bear_case: str = Field(
        min_length=1,
        max_length=1200,
    )

    market_view: str = Field(
        min_length=1,
        max_length=700,
    )

    fundamental_view: str = Field(
        min_length=1,
        max_length=700,
    )

    valuation_view: str = Field(
        min_length=1,
        max_length=700,
    )

    risk_view: str = Field(
        min_length=1,
        max_length=700,
    )

    news_view: str = Field(
        min_length=1,
        max_length=700,
    )

    key_catalysts: list[str] = Field(
        max_length=8,
    )

    key_risks: list[str] = Field(
        max_length=8,
    )

    evidence: list[
        CommitteeEvidenceItem
    ] = Field(
        min_length=4,
        max_length=15,
    )

    conditions_to_upgrade: list[str] = Field(
        max_length=6,
    )

    conditions_to_downgrade: list[str] = Field(
        max_length=6,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=8,
    )

    final_summary: str = Field(
        min_length=1,
        max_length=1200,
    )

class CompanyInvestmentReport(StrictModel):
    ticker: str
    generated_at: datetime

    research: CompanyResearchBundle

    committee: InvestmentCommitteeOutput