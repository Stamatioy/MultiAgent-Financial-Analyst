from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class FinancialEventClassification(BaseModel):
    """Structured classification of a financial-market event."""

    company: str = Field(
        min_length=1,
        description="Company discussed in the input.",
    )

    ticker: str | None = Field(
        default=None,
        description="Ticker symbol when it can be inferred safely.",
    )

    event_type: str = Field(
        min_length=1,
        description=(
            "Financial event category, such as earnings, acquisition, "
            "guidance, regulation, product launch, litigation, or financing."
        ),
    )

    sentiment: Sentiment

    materiality: int = Field(
        ge=1,
        le=5,
        description="Estimated materiality from 1, low, to 5, very high.",
    )

    time_horizon: str = Field(
        description="Expected impact horizon: short, medium, or long term.",
    )

    summary: str = Field(
        min_length=1,
        max_length=500,
        description="Concise factual summary of the event.",
    )

    reasoning: str = Field(
        min_length=1,
        max_length=1000,
        description="Explanation based only on the provided information.",
    )