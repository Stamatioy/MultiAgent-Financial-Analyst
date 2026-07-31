from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NewsArticle(StrictModel):
    article_id: str = Field(
        min_length=1,
        max_length=64,
    )

    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    title: str = Field(
        min_length=1,
        max_length=1000,
    )

    summary: str | None = Field(
        default=None,
        max_length=5000,
    )

    publisher: str | None = Field(
        default=None,
        max_length=300,
    )

    url: str | None = Field(
        default=None,
        max_length=3000,
    )

    published_at: datetime | None

    source: str

    fetched_at: datetime

    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        default=0.0,
    )