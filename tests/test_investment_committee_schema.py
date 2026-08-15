import pytest
from pydantic import ValidationError

from financial_analyst.committee.models import (
    InvestmentCommitteeOutput,
)


def valid_output() -> dict:
    return {
        "ticker": "TEST",

        "recommendation": "attractive",

        "conviction": "moderate",

        "confidence_score": 0.72,

        "investment_horizon": "long_term",

        "thesis": (
            "Strong fundamentals and cash generation "
            "partially offset valuation and volatility risk."
        ),

        "bull_case": (
            "Growth and cash generation could support "
            "continued value creation."
        ),

        "bear_case": (
            "Elevated valuation and volatility could "
            "produce significant downside if growth slows."
        ),

        "market_view": (
            "Momentum is positive but volatile."
        ),

        "fundamental_view": (
            "Fundamentals show strong growth."
        ),

        "valuation_view": (
            "Valuation requires continued business execution."
        ),

        "risk_view": (
            "Historical downside risk is substantial."
        ),

        "news_view": (
            "Recent developments are mixed."
        ),

        "key_catalysts": [
            "Continued earnings growth."
        ],

        "key_risks": [
            "Valuation compression.",
            "Growth slowdown.",
        ],

        "evidence": [
            {
                "source_type": "market_metric",
                "field": "return_1_year",
                "source_id": None,
                "interpretation": (
                    "Recent market performance was strong."
                ),
            },
            {
                "source_type": "fundamental_metric",
                "field": "revenue_growth",
                "source_id": None,
                "interpretation": (
                    "Revenue growth supports the bull case."
                ),
            },
            {
                "source_type": "valuation_metric",
                "field": "trailing_pe",
                "source_id": None,
                "interpretation": (
                    "The earnings multiple affects "
                    "the margin of safety."
                ),
            },
            {
                "source_type": "risk_metric",
                "field": "maximum_drawdown",
                "source_id": None,
                "interpretation": (
                    "Historical downside was substantial."
                ),
            },
        ],

        "conditions_to_upgrade": [
            "Improved valuation while growth remains strong."
        ],

        "conditions_to_downgrade": [
            "Material deterioration in revenue growth."
        ],

        "limitations": [
            "No dedicated macroeconomic analysis was supplied."
        ],

        "final_summary": (
            "The company presents a favorable but "
            "risk-sensitive long-term opportunity."
        ),
    }


def test_valid_output() -> None:
    result = (
        InvestmentCommitteeOutput.model_validate(
            valid_output()
        )
    )

    assert (
        result.recommendation.value
        == "attractive"
    )

    assert result.confidence_score == 0.72


def test_reject_invalid_confidence() -> None:
    data = valid_output()

    data["confidence_score"] = 1.50

    with pytest.raises(
        ValidationError
    ):
        InvestmentCommitteeOutput.model_validate(
            data
        )


def test_reject_unknown_recommendation() -> None:
    data = valid_output()

    data["recommendation"] = (
        "guaranteed_winner"
    )

    with pytest.raises(
        ValidationError
    ):
        InvestmentCommitteeOutput.model_validate(
            data
        )


def test_reject_buy_field() -> None:
    data = valid_output()

    data["target_price"] = 999.0

    with pytest.raises(
        ValidationError
    ):
        InvestmentCommitteeOutput.model_validate(
            data
        )