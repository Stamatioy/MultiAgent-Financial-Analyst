from __future__ import annotations

from typing import Any

import pytest

from financial_analyst.agents.fundamental_agent import (
    FundamentalAgentOutput,
    FundamentalAnalystAgent,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)


def make_metrics() -> FundamentalMetrics:
    return FundamentalMetrics(
        ticker="TEST",
        fiscal_year=2025,

        revenue=1200.0,
        net_income=150.0,
        operating_income=240.0,

        total_assets=3000.0,
        total_liabilities=1800.0,
        stockholders_equity=1200.0,

        cash_and_equivalents=500.0,

        operating_cash_flow=300.0,
        capital_expenditures=80.0,
        free_cash_flow=220.0,

        revenue_growth=0.20,
        net_income_growth=0.50,

        operating_margin=0.20,
        net_margin=0.125,

        return_on_assets=0.05,
        return_on_equity=0.125,

        liabilities_to_equity=1.50,
    )


def make_output() -> FundamentalAgentOutput:
    return FundamentalAgentOutput(
        ticker="TEST",
        fiscal_year=2025,

        growth="strong",
        profitability="moderate",
        cash_flow="strong",
        balance_sheet="moderate",

        growth_summary="Revenue and net income increased.",
        profitability_summary="Margins were positive.",
        cash_flow_summary="Free cash flow was positive.",
        balance_sheet_summary=(
            "Liabilities were meaningful relative to equity."
        ),

        strengths=[
            "Revenue growth was positive.",
            "Free cash flow was positive.",
        ],

        weaknesses=[
            "Liabilities were higher than equity.",
        ],

        evidence=[
            {
                "metric": "revenue_growth",
                "value": "20%",
                "interpretation": "Revenue increased.",
            },
            {
                "metric": "free_cash_flow",
                "value": "220",
                "interpretation": "Cash generation was positive.",
            },
        ],

        limitations=[
            "No valuation information was provided.",
        ],

        conclusion=(
            "The company shows positive growth and cash generation."
        ),
    )


class FakeLLMClient:
    def __init__(
        self,
        result: FundamentalAgentOutput,
    ) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def generate_structured(
        self,
        **kwargs: Any,
    ) -> FundamentalAgentOutput:
        self.calls.append(kwargs)
        return self.result


def test_agent_receives_metrics() -> None:
    fake_client = FakeLLMClient(make_output())

    agent = FundamentalAnalystAgent(
        llm_client=fake_client
    )

    result = agent.analyze(
        make_metrics()
    )

    assert result.ticker == "TEST"
    assert result.fiscal_year == 2025
    assert len(fake_client.calls) == 1

    prompt = fake_client.calls[0]["user_prompt"]

    assert '"revenue_growth": 0.2' in prompt
    assert '"free_cash_flow": 220.0' in prompt


def test_reject_wrong_ticker() -> None:
    output = make_output().model_copy(
        update={"ticker": "WRONG"}
    )

    agent = FundamentalAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="different ticker",
    ):
        agent.analyze(make_metrics())


def test_reject_wrong_fiscal_year() -> None:
    output = make_output().model_copy(
        update={"fiscal_year": 2024}
    )

    agent = FundamentalAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="different fiscal year",
    ):
        agent.analyze(make_metrics())


def test_reject_unknown_evidence_metric() -> None:
    output_data = make_output().model_dump()

    output_data["evidence"] = [
        {
            "metric": "revenue_growth",
            "value": "20%",
            "interpretation": "Revenue increased.",
        },
        {
            "metric": "EBITDA_growth",
            "value": "30%",
            "interpretation": "EBITDA increased.",
        },
    ]

    output = FundamentalAgentOutput.model_validate(
        output_data
    )

    agent = FundamentalAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="unsupported metric",
    ):
        agent.analyze(make_metrics())