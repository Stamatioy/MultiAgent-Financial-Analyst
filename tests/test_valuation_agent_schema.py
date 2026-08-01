import pytest
from pydantic import ValidationError

from financial_analyst.agents.valuation_agent import (
    ValuationAgentOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",
        "fiscal_year": 2025,

        "overall_valuation": "fair",
        "valuation_risk": "moderate",

        "earnings_valuation_summary": (
            "The earnings multiple is moderate."
        ),

        "revenue_valuation_summary": (
            "The revenue multiple is not unusually low."
        ),

        "cash_flow_valuation_summary": (
            "Free-cash-flow yield provides some support."
        ),

        "enterprise_valuation_summary": (
            "Enterprise-value ratios are broadly consistent "
            "with the other measures."
        ),

        "valuation_supports": [
            "Positive earnings yield.",
            "Positive free-cash-flow yield.",
        ],

        "valuation_concerns": [
            "No peer comparison is available.",
        ],

        "evidence": [
            {
                "metric": "trailing_pe",
                "interpretation": (
                    "The earnings multiple is meaningful."
                ),
            },
            {
                "metric": "free_cash_flow_yield",
                "interpretation": (
                    "The company produces cash relative "
                    "to its market value."
                ),
            },
        ],

        "limitations": [
            "No peer or historical valuation comparison "
            "was supplied."
        ],

        "conclusion": (
            "The absolute valuation appears balanced, but "
            "comparison data is required for stronger confidence."
        ),
    }


def test_valid_valuation_output() -> None:
    result = ValuationAgentOutput.model_validate(
        valid_output()
    )

    assert result.ticker == "TEST"
    assert result.overall_valuation.value == "fair"


def test_reject_unknown_field() -> None:
    data = valid_output()
    data["recommendation"] = "buy"

    with pytest.raises(ValidationError):
        ValuationAgentOutput.model_validate(
            data
        )


def test_reject_invalid_assessment() -> None:
    data = valid_output()
    data["overall_valuation"] = "amazing"

    with pytest.raises(ValidationError):
        ValuationAgentOutput.model_validate(
            data
        )