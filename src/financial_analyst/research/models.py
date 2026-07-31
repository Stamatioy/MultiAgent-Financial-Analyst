from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.agents.fundamental_agent import (
    FundamentalAgentOutput,
)
from financial_analyst.agents.market_agent import (
    MarketAgentOutput,
)
from financial_analyst.agents.news_agent import (
    NewsAgentOutput,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
)
from financial_analyst.retrieval.models import (
    RetrievedNewsArticle,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ResearchParameters(StrictModel):
    ticker: str
    fiscal_year: int

    market_years: int = Field(
        ge=1,
        le=30,
    )

    news_query: str = Field(
        min_length=1,
        max_length=1000,
    )

    news_limit: int = Field(
        ge=1,
        le=50,
    )

    as_of: datetime | None = None


class CompanyResearchBundle(StrictModel):
    ticker: str
    generated_at: datetime

    parameters: ResearchParameters

    market_metrics: MarketMetrics
    market_analysis: MarketAgentOutput

    fundamental_metrics: FundamentalMetrics
    fundamental_analysis: FundamentalAgentOutput

    retrieved_news: list[RetrievedNewsArticle]
    news_analysis: NewsAgentOutput