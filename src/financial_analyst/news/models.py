from __future__ import annotations

from datetime import datetime, timezone

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


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

    @field_validator(
        "published_at",
        "fetched_at",
        mode="after",
    )
    @classmethod
    def normalize_datetime_to_utc(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc
            )

        return value.astimezone(
            timezone.utc
        )

