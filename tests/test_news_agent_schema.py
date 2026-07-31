import pytest
from pydantic import ValidationError

from financial_analyst.agents.news_agent import (
    NewsAgentOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",
        "article_count": 3,
        "distinct_event_count": 1,
        "overall_sentiment": "positive",
        "events": [
            {
                "event_id": "event_1",
                "event_type": "earnings",
                "headline": "Company reports stronger results",
                "summary": (
                    "Several reports describe the same "
                    "quarterly earnings development."
                ),
                "sentiment": "positive",
                "materiality": "high",
                "time_horizon": "medium_term",
                "supporting_article_ids": [
                    "article-1",
                    "article-2",
                    "article-3",
                ],
                "positive_factors": [
                    "Reported results improved."
                ],
                "negative_factors": [],
                "uncertainties": [
                    "Full filing details were not supplied."
                ],
            }
        ],
        "overall_summary": (
            "Recent coverage is dominated by one "
            "positive earnings event."
        ),
        "major_positive_developments": [
            "Improved quarterly results."
        ],
        "major_negative_developments": [],
        "limitations": [
            "Only supplied headlines and summaries were analyzed."
        ],
    }


def test_valid_news_output() -> None:
    result = NewsAgentOutput.model_validate(
        valid_output()
    )

    assert result.ticker == "TEST"
    assert len(result.events) == 1


def test_reject_buy_recommendation_field() -> None:
    data = valid_output()
    data["recommendation"] = "buy"

    with pytest.raises(ValidationError):
        NewsAgentOutput.model_validate(
            data
        )


def test_reject_invalid_materiality() -> None:
    data = valid_output()

    data["events"][0][
        "materiality"
    ] = "extremely_huge"

    with pytest.raises(ValidationError):
        NewsAgentOutput.model_validate(
            data
        )

