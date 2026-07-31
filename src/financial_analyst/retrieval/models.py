from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.news.models import NewsArticle


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NewsVectorMetadata(StrictModel):
    vector_id: int = Field(ge=0)
    article_id: str
    ticker: str
    published_at: datetime | None


class RetrievedNewsArticle(StrictModel):
    article: NewsArticle
    semantic_score: float