from __future__ import annotations

from typing import Any

import pytest

from financial_analyst.agents.valuation_agent import (
    ValuationAgentOutput,
    ValuationAnalystAgent,
)
from tests.test_valuation_metrics import (
    make_fundamentals,
    make_market_metrics,
)
from financial_analyst.valuation.metrics import (
    calculate_valuation_metrics,
)
from financial_analyst.agents.valuation_agent import (
    ValuationEvidenceItem,
)

def make_output() -> ValuationAgentOutput:
    return ValuationAgentOutput(
        ticker="TEST",
        fiscal_year=2025,

        overall_valuation="fair",
        valuation_risk="moderate",

        earnings_valuation_summary=(
            "The earnings multiple is moderate."
        ),

        revenue_valuation_summary=(
            "The sales multiple is meaningful."
        ),

        cash_flow_valuation_summary=(
            "Free-cash-flow yield offers some support."
        ),

        enterprise_valuation_summary=(
            "Enterprise-value ratios are consistent "
            "with the other valuation measures."
        ),

        valuation_supports=[
            "Positive earnings yield.",
        ],

        valuation_concerns=[
            "No peer comparison is available.",
        ],

        evidence=[
            {
                "metric": "trailing_pe",
                "interpretation": (
                    "The earnings multiple is usable."
                ),
            },
            {
                "metric": "free_cash_flow_yield",
                "interpretation": (
                    "Cash generation supports valuation."
                ),
            },
        ],

        limitations=[
            "No peer or historical comparison was provided."
        ],

        conclusion=(
            "The available absolute valuation metrics "
            "appear broadly balanced."
        ),
    )


class FakeLLMClient:
    def __init__(
        self,
        result: ValuationAgentOutput,
    ) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def generate_structured(
        self,
        **kwargs: Any,
    ) -> ValuationAgentOutput:
        self.calls.append(kwargs)
        return self.result


def make_valuation():
    return calculate_valuation_metrics(
        market=make_market_metrics(),
        fundamentals=make_fundamentals(),
    )


def test_valuation_agent_receives_metrics() -> None:
    client = FakeLLMClient(
        make_output()
    )

    agent = ValuationAnalystAgent(
        llm_client=client
    )

    result = agent.analyze(
        valuation=make_valuation(),
        fundamentals=make_fundamentals(),
    )

    assert result.ticker == "TEST"
    assert len(client.calls) == 1

    prompt = client.calls[0]["user_prompt"]

    assert '"trailing_pe": 20.0' in prompt
    assert '"free_cash_flow_yield": 0.06' in prompt


def test_reject_wrong_ticker() -> None:
    output = make_output().model_copy(
        update={
            "ticker": "WRONG",
        }
    )

    agent = ValuationAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="different ticker",
    ):
        agent.analyze(
            valuation=make_valuation(),
            fundamentals=make_fundamentals(),
        )


def test_reject_unknown_evidence_metric() -> None:
    output = make_output().model_copy(
        update={
            "evidence": [
                ValuationEvidenceItem(
                    metric="trailing_pe",
                    interpretation="The earnings multiple is usable.",
                ),
                ValuationEvidenceItem(
                    metric="invented_metric",
                    interpretation="Invented evidence.",
                ),
            ]
        }
    )

    agent = ValuationAnalystAgent(
        llm_client=FakeLLMClient(output)
    )

    with pytest.raises(
        ValueError,
        match="unsupported metric",
    ):
        agent.analyze(
            valuation=make_valuation(),
            fundamentals=make_fundamentals(),
        )