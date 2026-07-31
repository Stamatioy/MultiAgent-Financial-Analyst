from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from financial_analyst.agents.news_agent import (
    NewsAgentOutput,
    NewsAnalystAgent,
)
from financial_analyst.news.models import (
    NewsArticle,
)


def make_articles() -> list[NewsArticle]:
    now = datetime(
        2026,
        7,
        30,
        12,
        0,
        tzinfo=timezone.utc,
    )

    return [
        NewsArticle(
            article_id="article-1",
            ticker="TEST",
            title="Company reports quarterly earnings",
            summary="Revenue increased during the quarter.",
            publisher="Publisher A",
            url="https://example.com/a",
            published_at=now,
            source="test",
            fetched_at=now,
        ),
        NewsArticle(
            article_id="article-2",
            ticker="TEST",
            title="Company results beat prior year",
            summary="The company reported improved results.",
            publisher="Publisher B",
            url="https://example.com/b",
            published_at=now,
            source="test",
            fetched_at=now,
        ),
    ]


def make_output() -> NewsAgentOutput:
    return NewsAgentOutput(
        ticker="TEST",
        article_count=2,
        distinct_event_count=1,
        overall_sentiment="positive",
        events=[
            {
                "event_id": "event_1",
                "event_type": "earnings",
                "headline": "Quarterly earnings reported",
                "summary": (
                    "Two articles describe the same "
                    "earnings development."
                ),
                "sentiment": "positive",
                "materiality": "high",
                "time_horizon": "medium_term",
                "supporting_article_ids": [
                    "article-1",
                    "article-2",
                ],
                "positive_factors": [
                    "Reported performance improved."
                ],
                "negative_factors": [],
                "uncertainties": [],
            }
        ],
        overall_summary="Coverage is primarily positive.",
        major_positive_developments=[
            "Improved reported performance."
        ],
        major_negative_developments=[],
        limitations=[
            "Analysis is limited to supplied news."
        ],
    )


class FakeLLMClient:
    def __init__(
        self,
        result: NewsAgentOutput,
    ) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def generate_structured(
        self,
        **kwargs: Any,
    ) -> NewsAgentOutput:
        self.calls.append(kwargs)
        return self.result


def test_news_agent_receives_articles() -> None:
    client = FakeLLMClient(
        make_output()
    )

    agent = NewsAnalystAgent(
        llm_client=client
    )

    result = agent.analyze(
        ticker="TEST",
        articles=make_articles(),
    )

    assert result.article_count == 2
    assert result.distinct_event_count == 1
    assert len(client.calls) == 1

    prompt = client.calls[0][
        "user_prompt"
    ]

    assert "article-1" in prompt
    assert "article-2" in prompt


def test_reject_unknown_article_reference() -> None:
    output = make_output()

    event = output.events[0].model_copy(
        update={
            "supporting_article_ids": [
                "article-1",
                "invented-id",
            ]
        }
    )

    output = output.model_copy(
        update={
            "events": [event]
        }
    )

    agent = NewsAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="unknown article ID",
    ):
        agent.analyze(
            ticker="TEST",
            articles=make_articles(),
        )


def test_corrects_wrong_article_count() -> None:
    output = make_output().model_copy(
        update={
            "article_count": 20
        }
    )

    agent = NewsAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    result = agent.analyze(
        ticker="TEST",
        articles=make_articles(),
    )

    assert result.article_count == 2


def test_corrects_wrong_event_count() -> None:
    output = make_output().model_copy(
        update={
            "distinct_event_count": 999
        }
    )

    agent = NewsAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    result = agent.analyze(
        ticker="TEST",
        articles=make_articles(),
    )

    assert result.distinct_event_count == 1

