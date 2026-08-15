from __future__ import annotations

from datetime import datetime, timezone

import pytest

from financial_analyst.committee.service import (
    InvestmentCommitteeService,
)
from tests.test_investment_committee import (
    make_committee_output,
    make_research_bundle,
)


class FakeInvestmentCommitteeAgent:
    def __init__(self) -> None:
        self.calls = []

    def analyze(
        self,
        bundle,
    ):
        self.calls.append(
            bundle
        )

        return make_committee_output()


def test_committee_service_evaluates_bundle() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    result = service.evaluate(
        bundle
    )

    assert result.ticker == "TEST"

    assert (
        result.recommendation.value
        == "attractive"
    )

    assert len(agent.calls) == 1

    assert agent.calls[0] is bundle


def test_committee_service_creates_report() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    result = service.create_report(
        bundle
    )

    assert result.ticker == "TEST"

    assert (
        result.research.ticker
        == "TEST"
    )

    assert (
        result.committee.recommendation.value
        == "attractive"
    )

    assert result.generated_at.tzinfo is not None


def test_committee_service_rejects_market_ticker_mismatch() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    bad_market_metrics = (
        bundle.market_metrics.model_copy(
            update={
                "ticker": "WRONG"
            }
        )
    )

    bad_bundle = bundle.model_copy(
        update={
            "market_metrics": (
                bad_market_metrics
            )
        }
    )

    with pytest.raises(
        ValueError,
        match="inconsistent tickers",
    ):
        service.evaluate(
            bad_bundle
        )


def test_committee_service_rejects_fundamental_ticker_mismatch() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    bad_fundamentals = (
        bundle.fundamental_metrics.model_copy(
            update={
                "ticker": "WRONG"
            }
        )
    )

    bad_bundle = bundle.model_copy(
        update={
            "fundamental_metrics": (
                bad_fundamentals
            )
        }
    )

    with pytest.raises(
        ValueError,
        match="inconsistent tickers",
    ):
        service.evaluate(
            bad_bundle
        )


def test_committee_service_rejects_valuation_ticker_mismatch() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    bad_valuation = (
        bundle.valuation_metrics.model_copy(
            update={
                "ticker": "WRONG"
            }
        )
    )

    bad_bundle = bundle.model_copy(
        update={
            "valuation_metrics": (
                bad_valuation
            )
        }
    )

    with pytest.raises(
        ValueError,
        match="inconsistent tickers",
    ):
        service.evaluate(
            bad_bundle
        )


def test_committee_service_rejects_risk_ticker_mismatch() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    bad_risk = (
        bundle.risk_metrics.model_copy(
            update={
                "ticker": "WRONG"
            }
        )
    )

    bad_bundle = bundle.model_copy(
        update={
            "risk_metrics": bad_risk
        }
    )

    with pytest.raises(
        ValueError,
        match="inconsistent tickers",
    ):
        service.evaluate(
            bad_bundle
        )


def test_committee_service_rejects_news_ticker_mismatch() -> None:
    agent = FakeInvestmentCommitteeAgent()

    service = InvestmentCommitteeService(
        agent=agent
    )

    bundle = make_research_bundle()

    bad_news = (
        bundle.news_analysis.model_copy(
            update={
                "ticker": "WRONG"
            }
        )
    )

    bad_bundle = bundle.model_copy(
        update={
            "news_analysis": bad_news
        }
    )

    with pytest.raises(
        ValueError,
        match="inconsistent tickers",
    ):
        service.evaluate(
            bad_bundle
        )