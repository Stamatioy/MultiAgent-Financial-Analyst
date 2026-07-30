import pytest
from pydantic import ValidationError

from financial_analyst.agents.market_agent import (
    MarketAgentOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",
        "momentum": "positive",
        "risk_level": "high",
        "trend_summary": "Price momentum is positive but volatile.",
        "short_term_view": "Recent returns are positive.",
        "long_term_price_view": "The longer price history is positive.",
        "positive_signals": [
            "Positive one-year return.",
        ],
        "negative_signals": [
            "Annualized volatility is elevated.",
        ],
        "evidence": [
            {
                "metric": "return_1_year",
                "value": "25%",
                "interpretation": "The stock rose over the past year.",
            },
            {
                "metric": "annualized_volatility",
                "value": "42%",
                "interpretation": "Price variability was substantial.",
            },
        ],
        "limitations": [
            "Price history does not include company fundamentals.",
        ],
        "data_start_date": "2021-01-01",
        "data_end_date": "2025-12-31",
        "conclusion": (
            "Momentum is positive, but the price history indicates "
            "meaningful risk."
        ),
    }


def test_valid_market_agent_output() -> None:
    result = MarketAgentOutput.model_validate(valid_output())

    assert result.ticker == "TEST"
    assert result.momentum.value == "positive"
    assert len(result.evidence) == 2


def test_reject_unknown_agent_field() -> None:
    data = valid_output()
    data["recommendation"] = "buy"

    with pytest.raises(ValidationError):
        MarketAgentOutput.model_validate(data)


def test_reject_invalid_momentum() -> None:
    data = valid_output()
    data["momentum"] = "extremely_amazing"

    with pytest.raises(ValidationError):
        MarketAgentOutput.model_validate(data)


def test_evidence_requires_at_least_two_items() -> None:
    data = valid_output()
    data["evidence"] = data["evidence"][:1]

    with pytest.raises(ValidationError):
        MarketAgentOutput.model_validate(data)