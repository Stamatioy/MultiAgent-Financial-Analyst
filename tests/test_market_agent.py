from __future__ import annotations

from datetime import date
from typing import Any

import pytest

from financial_analyst.agents.market_agent import (
    MarketAgentOutput,
    MarketAnalystAgent,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
    MarketTrend,
)


def make_metrics() -> MarketMetrics:
    return MarketMetrics(
        ticker="TEST",
        start_date=date(2021, 1, 4),
        end_date=date(2025, 12, 31),
        observations=1250,
        latest_close=150.0,
        total_return=0.50,
        annualized_return=0.084,
        annualized_volatility=0.42,
        maximum_drawdown=-0.38,
        return_1_month=0.04,
        return_3_months=0.10,
        return_6_months=0.18,
        return_1_year=0.25,
        moving_average_20=145.0,
        moving_average_50=140.0,
        moving_average_200=125.0,
        distance_from_20_day_average=0.0345,
        distance_from_50_day_average=0.0714,
        distance_from_200_day_average=0.20,
        trend=MarketTrend.BULLISH,
    )


def make_output() -> MarketAgentOutput:
    return MarketAgentOutput(
        ticker="TEST",
        momentum="positive",
        risk_level="high",
        trend_summary="The observed trend is positive.",
        short_term_view="Recent horizons are positive.",
        long_term_price_view="Long-term returns are positive.",
        positive_signals=[
            "Price is above the 200-day moving average.",
        ],
        negative_signals=[
            "Historical volatility is elevated.",
        ],
        evidence=[
            {
                "metric": "return_1_year",
                "value": "25%",
                "interpretation": "One-year performance was positive.",
            },
            {
                "metric": "maximum_drawdown",
                "value": "-38%",
                "interpretation": "The history includes a deep decline.",
            },
        ],
        limitations=[
            "No fundamental or valuation data was supplied.",
        ],
        data_start_date="2021-01-04",
        data_end_date="2025-12-31",
        conclusion=(
            "Momentum is positive, but historical risk was substantial."
        ),
    )


class FakeLLMClient:
    def __init__(
        self,
        result: MarketAgentOutput,
    ) -> None:
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def generate_structured(self, **kwargs: Any) -> MarketAgentOutput:
        self.calls.append(kwargs)
        return self.result


def test_market_agent_uses_validated_metrics() -> None:
    fake_client = FakeLLMClient(make_output())

    agent = MarketAnalystAgent(
        llm_client=fake_client,  # type: ignore[arg-type]
    )

    result = agent.analyze(make_metrics())

    assert result.ticker == "TEST"
    assert result.risk_level.value == "high"
    assert len(fake_client.calls) == 1

    call = fake_client.calls[0]

    assert call["response_model"] is MarketAgentOutput
    assert '"return_1_year": 0.25' in call["user_prompt"]
    assert '"maximum_drawdown": -0.38' in call["user_prompt"]


def test_market_agent_rejects_wrong_ticker() -> None:
    output = make_output().model_copy(
        update={"ticker": "WRONG"}
    )

    fake_client = FakeLLMClient(output)

    agent = MarketAnalystAgent(
        llm_client=fake_client,  # type: ignore[arg-type]
    )

    with pytest.raises(
        ValueError,
        match="different ticker",
    ):
        agent.analyze(make_metrics())


def test_market_agent_rejects_wrong_end_date() -> None:
    output = make_output().model_copy(
        update={"data_end_date": "2099-01-01"}
    )

    fake_client = FakeLLMClient(output)

    agent = MarketAnalystAgent(
        llm_client=fake_client,  # type: ignore[arg-type]
    )

    with pytest.raises(
        ValueError,
        match="incorrect data_end_date",
    ):
        agent.analyze(make_metrics())