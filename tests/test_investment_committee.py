from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

import pytest

from financial_analyst.agents.fundamental_agent import (
    FundamentalAgentOutput,
)
from financial_analyst.agents.investment_committee import (
    InvestmentCommitteeAgent,
)
from financial_analyst.agents.market_agent import (
    MarketAgentOutput,
)
from financial_analyst.agents.news_agent import (
    NewsAgentOutput,
)
from financial_analyst.agents.risk_agent import (
    RiskAgentOutput,
)
from financial_analyst.agents.valuation_agent import (
    ValuationAgentOutput,
)
from financial_analyst.committee.models import (
    InvestmentCommitteeOutput,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
    MarketTrend,
)
from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.research.models import (
    CompanyResearchBundle,
    ResearchParameters,
)
from financial_analyst.retrieval.models import (
    RetrievedNewsArticle,
)
from financial_analyst.risk.models import (
    RiskMetrics,
)
from financial_analyst.valuation.models import (
    ValuationMetrics,
)


def make_research_bundle() -> CompanyResearchBundle:
    now = datetime(
        2026,
        7,
        31,
        tzinfo=timezone.utc,
    )

    market_metrics = MarketMetrics(
        ticker="TEST",
        start_date=date(2021, 1, 1),
        end_date=date(2025, 12, 31),
        observations=1200,
        latest_close=100.0,

        total_return=0.50,
        annualized_return=0.10,
        annualized_volatility=0.40,
        maximum_drawdown=-0.50,

        return_1_month=0.02,
        return_3_months=0.08,
        return_6_months=0.15,
        return_1_year=0.25,

        moving_average_20=98.0,
        moving_average_50=95.0,
        moving_average_200=90.0,

        distance_from_20_day_average=0.0204,
        distance_from_50_day_average=0.0526,
        distance_from_200_day_average=0.1111,

        trend=MarketTrend.BULLISH,
    )

    market_analysis = MarketAgentOutput(
        ticker="TEST",
        momentum="positive",
        risk_level="high",

        trend_summary=(
            "The historical trend is positive."
        ),

        short_term_view=(
            "Recent momentum is positive."
        ),

        long_term_price_view=(
            "Long-term performance is positive "
            "but volatile."
        ),

        positive_signals=[
            "Positive one-year return.",
        ],

        negative_signals=[
            "Historical volatility is elevated.",
        ],

        evidence=[
            {
                "metric": "return_1_year",
                "value": "25%",
                "interpretation": (
                    "The stock produced a positive "
                    "one-year return."
                ),
            },
            {
                "metric": "maximum_drawdown",
                "value": "-50%",
                "interpretation": (
                    "Historical downside was substantial."
                ),
            },
        ],

        limitations=[
            "Historical returns do not guarantee "
            "future performance."
        ],

        data_start_date="2021-01-01",
        data_end_date="2025-12-31",

        conclusion=(
            "Momentum is positive but historical "
            "risk remains material."
        ),
    )

    fundamental_metrics = FundamentalMetrics(
        ticker="TEST",
        fiscal_year=2025,

        revenue=500.0,
        net_income=50.0,
        operating_income=60.0,

        total_assets=800.0,
        total_liabilities=300.0,
        stockholders_equity=500.0,

        cash_and_equivalents=40.0,

        shares_outstanding=10.0,

        current_debt=5.0,
        noncurrent_debt=15.0,
        total_debt=20.0,

        operating_cash_flow=80.0,
        capital_expenditures=20.0,
        free_cash_flow=60.0,

        revenue_growth=0.20,
        net_income_growth=0.25,

        operating_margin=0.12,
        net_margin=0.10,

        return_on_assets=0.07,
        return_on_equity=0.11,

        liabilities_to_equity=0.60,
    )

    fundamental_analysis = FundamentalAgentOutput(
        ticker="TEST",
        fiscal_year=2025,

        growth="strong",
        profitability="moderate",
        cash_flow="strong",
        balance_sheet="moderate",

        growth_summary=(
            "Revenue and earnings increased."
        ),

        profitability_summary=(
            "The company remains profitable."
        ),

        cash_flow_summary=(
            "Operating and free cash flow are positive."
        ),

        balance_sheet_summary=(
            "The balance sheet remains manageable."
        ),

        strengths=[
            "Positive revenue growth.",
            "Positive free cash flow.",
        ],

        weaknesses=[
            "Liabilities remain meaningful."
        ],

        evidence=[
            {
                "metric": "revenue_growth",
                "value": "20%",
                "interpretation": (
                    "Revenue increased year over year."
                ),
            },
            {
                "metric": "free_cash_flow",
                "value": "60",
                "interpretation": (
                    "Free cash flow remained positive."
                ),
            },
        ],

        limitations=[
            "The analysis uses historical financial data."
        ],

        conclusion=(
            "Fundamentals are generally positive."
        ),
    )

    valuation_metrics = ValuationMetrics(
        ticker="TEST",
        fiscal_year=2025,
        price_date=date(2025, 12, 31),

        share_price=100.0,
        shares_outstanding=10.0,

        market_cap=1000.0,
        enterprise_value=980.0,

        trailing_pe=20.0,
        earnings_yield=0.05,

        price_to_sales=2.0,
        price_to_book=2.0,

        ev_to_sales=1.96,
        ev_to_operating_income=(
            980.0 / 60.0
        ),

        free_cash_flow_yield=0.06,

        net_cash=20.0,

        debt_used=20.0,
        cash_used=40.0,

        shares_missing=False,
        debt_missing=False,
        cash_missing=False,

        notes=[],
    )

    valuation_analysis = ValuationAgentOutput(
        ticker="TEST",
        fiscal_year=2025,

        overall_valuation="fair",
        valuation_risk="moderate",

        earnings_valuation_summary=(
            "The earnings valuation appears moderate."
        ),

        revenue_valuation_summary=(
            "The sales valuation appears reasonable "
            "on an absolute basis."
        ),

        cash_flow_valuation_summary=(
            "Free cash flow provides valuation support."
        ),

        enterprise_valuation_summary=(
            "Enterprise-value ratios are consistent "
            "with the other valuation measures."
        ),

        valuation_supports=[
            "Positive earnings yield.",
            "Positive free-cash-flow yield.",
        ],

        valuation_concerns=[
            "No peer comparison is available."
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
            "No peer or historical valuation comparison "
            "was supplied."
        ],

        conclusion=(
            "Absolute valuation appears broadly balanced."
        ),
    )

    risk_metrics = RiskMetrics(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        start_date=date(2021, 1, 1),
        end_date=date(2025, 12, 31),

        stock_observations=1200,
        aligned_benchmark_observations=1180,

        risk_free_rate_annual=0.0,

        annualized_volatility=0.40,
        downside_deviation=0.25,

        beta=1.40,
        benchmark_correlation=0.75,

        sharpe_ratio=0.80,
        sortino_ratio=1.10,

        daily_var_95=0.04,
        daily_cvar_95=0.06,

        worst_daily_return=-0.10,
        worst_weekly_return=-0.15,
        worst_monthly_return=-0.22,

        maximum_drawdown=-0.50,
        max_drawdown_duration_days=300,

        average_daily_volume_20=20_000_000.0,

        average_daily_dollar_volume_20=(
            2_000_000_000.0
        ),

        net_debt=-20.0,
        debt_to_free_cash_flow=0.30,

        benchmark_data_available=True,

        notes=[],
    )

    risk_analysis = RiskAgentOutput(
        ticker="TEST",
        benchmark_ticker="^GSPC",

        overall_risk="high",
        market_risk="high",
        downside_risk="high",
        financial_risk="low",
        liquidity_risk="low",

        market_risk_summary=(
            "Historical market risk is elevated."
        ),

        downside_risk_summary=(
            "Historical drawdowns were substantial."
        ),

        financial_risk_summary=(
            "The company has relatively low "
            "financial risk."
        ),

        liquidity_risk_summary=(
            "Historical trading liquidity was strong."
        ),

        risk_factors=[
            "High historical volatility.",
            "Large maximum drawdown.",
        ],

        risk_mitigants=[
            "Net cash position.",
            "Positive free cash flow.",
        ],

        evidence=[
            {
                "metric": "annualized_volatility",
                "interpretation": (
                    "Historical volatility was elevated."
                ),
            },
            {
                "metric": "maximum_drawdown",
                "interpretation": (
                    "Historical downside was substantial."
                ),
            },
        ],

        limitations=[
            "Historical risk may not represent future risk."
        ],

        conclusion=(
            "The stock has substantial market and downside "
            "risk despite financial-risk mitigants."
        ),
    )

    article = NewsArticle(
        article_id="article-1",
        ticker="TEST",

        title="Company reports strong demand",

        summary=(
            "The company reported strong demand "
            "for a major product."
        ),

        publisher="Example News",

        url="https://example.com/article-1",

        published_at=now,
        source="test",
        fetched_at=now,

        relevance_score=0.90,
    )

    retrieved_news = [
        RetrievedNewsArticle(
            article=article,
            semantic_score=0.90,
        )
    ]

    news_analysis = NewsAgentOutput(
        ticker="TEST",

        article_count=1,
        distinct_event_count=1,

        overall_sentiment="positive",

        events=[
            {
                "event_id": "event_1",

                "event_type": "product",

                "headline": (
                    "Company reports strong demand"
                ),

                "summary": (
                    "Reported demand was strong."
                ),

                "sentiment": "positive",

                "materiality": "high",

                "time_horizon": "medium_term",

                "supporting_article_ids": [
                    "article-1"
                ],

                "positive_factors": [
                    "Strong reported demand."
                ],

                "negative_factors": [],

                "uncertainties": [
                    "Future demand is uncertain."
                ],
            }
        ],

        overall_summary=(
            "Recent news is positive."
        ),

        major_positive_developments=[
            "Strong reported demand."
        ],

        major_negative_developments=[],

        limitations=[
            "Only a limited news sample was supplied."
        ],
    )

    parameters = ResearchParameters(
        ticker="TEST",
        fiscal_year=2025,

        market_years=5,

        benchmark_ticker="^GSPC",

        risk_free_rate_annual=0.0,

        news_query="material developments",

        news_limit=10,

        as_of=now,
    )

    return CompanyResearchBundle(
        ticker="TEST",
        generated_at=now,

        parameters=parameters,

        market_metrics=market_metrics,
        market_analysis=market_analysis,

        fundamental_metrics=fundamental_metrics,
        fundamental_analysis=(
            fundamental_analysis
        ),

        valuation_metrics=valuation_metrics,
        valuation_analysis=valuation_analysis,

        risk_metrics=risk_metrics,
        risk_analysis=risk_analysis,

        retrieved_news=retrieved_news,
        news_analysis=news_analysis,
    )


def make_committee_output() -> InvestmentCommitteeOutput:
    return InvestmentCommitteeOutput(
        ticker="TEST",

        recommendation="attractive",

        conviction="moderate",

        confidence_score=0.72,

        investment_horizon="long_term",

        thesis=(
            "Strong fundamentals and cash generation "
            "partially offset valuation and risk concerns."
        ),

        bull_case=(
            "Growth, profitability and cash generation "
            "support the positive investment case."
        ),

        bear_case=(
            "Elevated historical volatility and downside "
            "risk could reduce future returns."
        ),

        market_view=(
            "Market momentum is positive but volatile."
        ),

        fundamental_view=(
            "Fundamentals show healthy growth and "
            "cash generation."
        ),

        valuation_view=(
            "Valuation appears broadly balanced."
        ),

        risk_view=(
            "Historical risk remains substantial."
        ),

        news_view=(
            "Recent news contains a positive demand catalyst."
        ),

        key_catalysts=[
            "Continued revenue growth.",
            "Continued strong product demand.",
        ],

        key_risks=[
            "Valuation compression.",
            "High price volatility.",
        ],

        evidence=[
            {
                "source_type": "market_metric",
                "field": "return_1_year",
                "source_id": None,
                "interpretation": (
                    "Recent market performance was positive."
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
                    "The earnings multiple affects the "
                    "margin of safety."
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
            {
                "source_type": "news_event",
                "field": "event",
                "source_id": "event_1",
                "interpretation": (
                    "Reported product demand supports "
                    "the positive case."
                ),
            },
        ],

        conditions_to_upgrade=[
            "Improved valuation while growth remains strong."
        ],

        conditions_to_downgrade=[
            "Material deterioration in revenue growth."
        ],

        limitations=[
            "No dedicated macroeconomic analysis was supplied."
        ],

        final_summary=(
            "The available evidence supports an attractive "
            "long-term view, but meaningful risk remains."
        ),
    )


class FakeLLMClient:
    def __init__(
        self,
        result: InvestmentCommitteeOutput,
    ) -> None:
        self.result = result

        self.calls: list[
            dict[str, Any]
        ] = []

    def generate_structured(
        self,
        **kwargs: Any,
    ) -> InvestmentCommitteeOutput:
        self.calls.append(
            kwargs
        )

        return self.result


def test_committee_receives_research_bundle() -> None:
    client = FakeLLMClient(
        make_committee_output()
    )

    agent = InvestmentCommitteeAgent(
        llm_client=client
    )

    bundle = make_research_bundle()

    result = agent.analyze(
        bundle
    )

    assert result.ticker == "TEST"

    assert result.recommendation.value == (
        "attractive"
    )

    assert len(client.calls) == 1

    prompt = client.calls[0][
        "user_prompt"
    ]

    assert '"revenue_growth": 0.2' in prompt

    assert '"trailing_pe": 20.0' in prompt

    assert '"maximum_drawdown": -0.5' in prompt

    assert '"event_id": "event_1"' in prompt


def test_reject_wrong_ticker() -> None:
    output = make_committee_output().model_copy(
        update={
            "ticker": "WRONG"
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="different ticker",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_reject_invented_market_metric() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[0] = (
        evidence[0].model_copy(
            update={
                "source_type": (
                    "market_metric"
                ),
                "field": (
                    "future_price_target"
                ),
                "source_id": None,
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="unsupported field",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_reject_invented_fundamental_metric() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[1] = (
        evidence[1].model_copy(
            update={
                "source_type": (
                    "fundamental_metric"
                ),
                "field": (
                    "future_revenue_growth"
                ),
                "source_id": None,
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="unsupported field",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_reject_metric_source_id() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[0] = (
        evidence[0].model_copy(
            update={
                "source_id": "should-not-exist"
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="must not contain source_id",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_reject_unknown_news_event() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[-1] = (
        evidence[-1].model_copy(
            update={
                "source_type": "news_event",
                "field": "event",
                "source_id": "event_999",
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="unknown news event",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_news_event_requires_source_id() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[-1] = (
        evidence[-1].model_copy(
            update={
                "source_type": "news_event",
                "field": "event",
                "source_id": None,
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="requires source_id",
    ):
        agent.analyze(
            make_research_bundle()
        )


def test_news_event_requires_event_field() -> None:
    output = make_committee_output()

    evidence = list(
        output.evidence
    )

    evidence[-1] = (
        evidence[-1].model_copy(
            update={
                "source_type": "news_event",
                "field": "headline",
                "source_id": "event_1",
            }
        )
    )

    output = output.model_copy(
        update={
            "evidence": evidence
        }
    )

    agent = InvestmentCommitteeAgent(
        llm_client=FakeLLMClient(
            output
        )
    )

    with pytest.raises(
        ValueError,
        match="field='event'",
    ):
        agent.analyze(
            make_research_bundle()
        )