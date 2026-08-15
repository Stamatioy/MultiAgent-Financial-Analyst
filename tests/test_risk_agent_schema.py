import pytest
from pydantic import ValidationError

from financial_analyst.agents.risk_agent import (
    RiskAgentOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",
        "benchmark_ticker": "^GSPC",

        "overall_risk": "high",
        "market_risk": "high",
        "downside_risk": "high",
        "financial_risk": "low",
        "liquidity_risk": "low",

        "market_risk_summary": (
            "Historical volatility and benchmark "
            "sensitivity are elevated."
        ),

        "downside_risk_summary": (
            "Historical drawdowns and tail losses "
            "were substantial."
        ),

        "financial_risk_summary": (
            "Cash exceeds debt and free cash flow "
            "provides financial support."
        ),

        "liquidity_risk_summary": (
            "Historical dollar trading volume "
            "indicates substantial market liquidity."
        ),

        "risk_factors": [
            "High volatility.",
            "Deep historical drawdown.",
        ],

        "risk_mitigants": [
            "Net cash position.",
            "Positive free cash flow.",
        ],

        "evidence": [
            {
                "metric": "annualized_volatility",
                "interpretation": (
                    "Historical price variability "
                    "was substantial."
                ),
            },
            {
                "metric": "maximum_drawdown",
                "interpretation": (
                    "The stock experienced a major "
                    "historical peak-to-trough decline."
                ),
            },
        ],

        "limitations": [
            "Historical risk may not represent future risk."
        ],

        "conclusion": (
            "The stock has substantial historical market "
            "and downside risk despite relatively strong "
            "financial risk mitigants."
        ),
    }


def test_valid_risk_output() -> None:
    result = (
        RiskAgentOutput.model_validate(
            valid_output()
        )
    )

    assert (
        result.overall_risk.value
        == "high"
    )


def test_reject_recommendation_field() -> None:
    data = valid_output()

    data["recommendation"] = "sell"

    with pytest.raises(
        ValidationError
    ):
        RiskAgentOutput.model_validate(
            data
        )


def test_reject_invalid_risk() -> None:
    data = valid_output()

    data["overall_risk"] = (
        "catastrophically_scary"
    )

    with pytest.raises(
        ValidationError
    ):
        RiskAgentOutput.model_validate(
            data
        )