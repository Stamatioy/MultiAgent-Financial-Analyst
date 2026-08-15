from __future__ import annotations

from datetime import date
from typing import Any

import pytest

from financial_analyst.agents.risk_agent import (
    RiskAgentOutput,
    RiskAnalystAgent,
    RiskEvidenceItem,
)
from financial_analyst.risk.models import (
    RiskMetrics,
)


def make_metrics() -> RiskMetrics:
    return RiskMetrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        start_date=date(
            2021,
            1,
            1,
        ),

        end_date=date(
            2025,
            12,
            31,
        ),

        stock_observations=1250,

        aligned_benchmark_observations=1240,

        risk_free_rate_annual=0.0,

        annualized_volatility=0.45,
        downside_deviation=0.30,

        beta=1.50,
        benchmark_correlation=0.75,

        sharpe_ratio=0.80,
        sortino_ratio=1.20,

        daily_var_95=0.04,
        daily_cvar_95=0.065,

        worst_daily_return=-0.12,
        worst_weekly_return=-0.18,
        worst_monthly_return=-0.25,

        maximum_drawdown=-0.55,

        max_drawdown_duration_days=400,

        average_daily_volume_20=(
            20_000_000.0
        ),

        average_daily_dollar_volume_20=(
            3_000_000_000.0
        ),

        net_debt=-5_000_000_000.0,

        debt_to_free_cash_flow=0.30,

        benchmark_data_available=True,

        notes=[],
    )


def make_output() -> RiskAgentOutput:
    return RiskAgentOutput(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        overall_risk="high",
        market_risk="high",
        downside_risk="high",
        financial_risk="low",
        liquidity_risk="low",

        market_risk_summary=(
            "Market risk is elevated."
        ),

        downside_risk_summary=(
            "Historical downside was substantial."
        ),

        financial_risk_summary=(
            "Net cash reduces financial risk."
        ),

        liquidity_risk_summary=(
            "Historical trading liquidity was substantial."
        ),

        risk_factors=[
            "High historical volatility."
        ],

        risk_mitigants=[
            "Net cash position."
        ],

        evidence=[
            {
                "metric": "annualized_volatility",
                "interpretation": (
                    "Volatility was elevated."
                ),
            },
            {
                "metric": "maximum_drawdown",
                "interpretation": (
                    "Historical drawdown was severe."
                ),
            },
        ],

        limitations=[
            "Historical risk may not persist."
        ],

        conclusion=(
            "The stock has high historical market risk."
        ),
    )


class FakeLLMClient:
    def __init__(
        self,
        result: RiskAgentOutput,
    ) -> None:
        self.result = result
        self.calls: list[
            dict[str, Any]
        ] = []

    def generate_structured(
        self,
        **kwargs: Any,
    ) -> RiskAgentOutput:
        self.calls.append(
            kwargs
        )

        return self.result


def test_risk_agent_receives_metrics() -> None:
    client = FakeLLMClient(
        make_output()
    )

    agent = RiskAnalystAgent(
        llm_client=client
    )

    result = agent.analyze(
        make_metrics()
    )

    assert result.ticker == "TEST"

    assert len(
        client.calls
    ) == 1

    prompt = client.calls[0][
        "user_prompt"
    ]

    assert (
        '"beta": 1.5'
        in prompt
    )

    assert (
        '"maximum_drawdown": -0.55'
        in prompt
    )


def test_reject_wrong_ticker() -> None:
    output = make_output().model_copy(
        update={
            "ticker": "WRONG"
        }
    )

    agent = RiskAnalystAgent(
        llm_client=(
            FakeLLMClient(
                output
            )
        )
    )

    with pytest.raises(
        ValueError,
        match="different ticker",
    ):
        agent.analyze(
            make_metrics()
        )


def test_reject_unknown_metric() -> None:
    output = make_output().model_copy(
        update={
            "evidence": [
                RiskEvidenceItem(
                    metric="annualized_volatility",
                    interpretation=(
                        "Volatility was elevated."
                    ),
                ),
                RiskEvidenceItem(
                    metric="future_crash_probability",
                    interpretation=(
                        "Invented metric."
                    ),
                ),
            ]
        }
    )

    agent = RiskAnalystAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="unsupported metric",
    ):
        agent.analyze(
            make_metrics()
        )