from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.llm.client import LocalLLMClient
from financial_analyst.llm.protocol import StructuredLLMClient
from financial_analyst.news.models import NewsArticle
from financial_analyst.prompts.news_agent import (
    NEWS_AGENT_SYSTEM_PROMPT,
    build_news_agent_prompt,
)


class StrictAgentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NewsSentiment(str, Enum):
    STRONGLY_POSITIVE = "strongly_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    STRONGLY_NEGATIVE = "strongly_negative"
    MIXED = "mixed"
    UNCLEAR = "unclear"


class EventMateriality(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class EventTimeHorizon(str, Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
    UNCLEAR = "unclear"


class EventType(str, Enum):
    EARNINGS = "earnings"
    GUIDANCE = "guidance"
    PRODUCT = "product"
    ACQUISITION = "acquisition"
    DIVESTITURE = "divestiture"
    PARTNERSHIP = "partnership"
    REGULATION = "regulation"
    LITIGATION = "litigation"
    FINANCING = "financing"
    MANAGEMENT = "management"
    OPERATIONS = "operations"
    ANALYST_ACTION = "analyst_action"
    MACRO_EXPOSURE = "macro_exposure"
    OTHER = "other"


class NewsEvent(StrictAgentModel):
    event_id: str = Field(
        min_length=1,
        max_length=30,
        description="Local identifier such as event_1.",
    )

    event_type: EventType

    headline: str = Field(
        min_length=1,
        max_length=300,
    )

    summary: str = Field(
        min_length=1,
        max_length=700,
    )

    sentiment: NewsSentiment

    materiality: EventMateriality

    time_horizon: EventTimeHorizon

    supporting_article_ids: list[str] = Field(
        min_length=1,
        max_length=20,
    )

    positive_factors: list[str] = Field(
        max_length=5,
    )

    negative_factors: list[str] = Field(
        max_length=5,
    )

    uncertainties: list[str] = Field(
        max_length=5,
    )


class NewsAgentOutput(StrictAgentModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    article_count: int = Field(
        ge=1,
    )

    distinct_event_count: int = Field(
        ge=0,
    )

    overall_sentiment: NewsSentiment

    events: list[NewsEvent] = Field(
        max_length=15,
    )

    overall_summary: str = Field(
        min_length=1,
        max_length=1000,
    )

    major_positive_developments: list[str] = Field(
        max_length=6,
    )

    major_negative_developments: list[str] = Field(
        max_length=6,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=6,
    )


class NewsAnalystAgent:
    """Consolidates recent articles into grounded financial events."""

    def __init__(
        self,
        llm_client: StructuredLLMClient | None = None,
    ) -> None:
        self.llm_client = llm_client or LocalLLMClient()

    def analyze(
        self,
        *,
        ticker: str,
        articles: list[NewsArticle],
    ) -> NewsAgentOutput:
        if not articles:
            raise ValueError(
                "NewsAnalystAgent requires at least one article."
            )

        result = self.llm_client.generate_structured(
            system_prompt=NEWS_AGENT_SYSTEM_PROMPT,
            user_prompt=build_news_agent_prompt(
                ticker=ticker,
                articles=articles,
            ),
            response_model=NewsAgentOutput,
            temperature=0.1,
            max_tokens=3500,
        )

        self._validate_grounding(
            ticker=ticker,
            articles=articles,
            result=result,
        )

        return result
    
    @staticmethod
    def _validate_grounding(
        *,
        ticker: str,
        articles: list[NewsArticle],
        result: NewsAgentOutput,
    ) -> None:
        if result.ticker != ticker:
            raise ValueError(
                "News agent returned a different ticker: "
                f"expected {ticker}, got {result.ticker}."
            )

        if result.article_count != len(articles):
            raise ValueError(
                "News agent returned an incorrect article_count."
            )

        if result.distinct_event_count != len(result.events):
            raise ValueError(
                "distinct_event_count does not match events length."
            )

        allowed_ids = {
            article.article_id
            for article in articles
        }

        seen_event_ids: set[str] = set()

        for event in result.events:
            if event.event_id in seen_event_ids:
                raise ValueError(
                    f"Duplicate event ID: {event.event_id}"
                )

            seen_event_ids.add(event.event_id)

            for article_id in event.supporting_article_ids:
                if article_id not in allowed_ids:
                    raise ValueError(
                        "News agent referenced an unknown "
                        f"article ID: {article_id}"
                    )

            if len(event.supporting_article_ids) != len(
                set(event.supporting_article_ids)
            ):
                raise ValueError(
                    f"{event.event_id} contains duplicate article IDs."
                )