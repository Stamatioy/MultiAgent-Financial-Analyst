import pytest
from pydantic import ValidationError

from financial_analyst.agents.fundamental_agent import (
    FundamentalAgentOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",
        "fiscal_year": 2025,
        "growth": "moderate",
        "profitability": "strong",
        "cash_flow": "strong",
        "balance_sheet": "moderate",
        "growth_summary": "Revenue increased during the year.",
        "profitability_summary": (
            "Operating and net margins were positive."
        ),
        "cash_flow_summary": (
            "Operating cash flow and free cash flow were positive."
        ),
        "balance_sheet_summary": (
            "Liabilities remain meaningful relative to equity."
        ),
        "strengths": [
            "Positive revenue growth.",
            "Positive free cash flow.",
        ],
        "weaknesses": [
            "Liabilities are substantial relative to equity.",
        ],
        "evidence": [
            {
                "metric": "revenue_growth",
                "value": "20%",
                "interpretation": "Revenue increased year over year.",
            },
            {
                "metric": "free_cash_flow",
                "value": "220",
                "interpretation": "Free cash flow was positive.",
            },
        ],
        "limitations": [
            "The analysis covers one fiscal year.",
        ],
        "conclusion": (
            "Fundamentals show positive growth, profitability and "
            "cash generation, with some balance-sheet leverage."
        ),
    }


def test_valid_output() -> None:
    result = FundamentalAgentOutput.model_validate(
        valid_output()
    )

    assert result.ticker == "TEST"
    assert result.growth.value == "moderate"


def test_reject_unknown_field() -> None:
    data = valid_output()
    data["recommendation"] = "buy"

    with pytest.raises(ValidationError):
        FundamentalAgentOutput.model_validate(data)


def test_reject_invalid_profitability() -> None:
    data = valid_output()
    data["profitability"] = "fantastic"

    with pytest.raises(ValidationError):
        FundamentalAgentOutput.model_validate(data)