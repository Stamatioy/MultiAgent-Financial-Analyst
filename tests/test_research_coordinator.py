from __future__ import annotations

from datetime import (
    date,
    datetime,
    timezone,
)

from financial_analyst.agents.fundamental_agent import (
    FundamentalAgentOutput,
)
from financial_analyst.agents.market_agent import (
    MarketAgentOutput,
)
from financial_analyst.agents.news_agent import (
    NewsAgentOutput,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketAnalysisResult,
    MarketMetrics,
    MarketTrend,
)
from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.research.coordinator import (
    ResearchCoordinator,
)
from financial_analyst.retrieval.models import (
    RetrievedNewsArticle,
)

def make_market_metrics() -> MarketMetrics:
    return MarketMetrics(
        ticker="TEST",
        start_date=date(2021, 1, 1),
        end_date=date(2025, 12, 31),
        observations=1200,
        latest_close=150.0,

        total_return=0.5,
        annualized_return=0.08,
        annualized_volatility=0.35,
        maximum_drawdown=-0.30,

        return_1_month=0.03,
        return_3_months=0.08,
        return_6_months=0.12,
        return_1_year=0.20,

        moving_average_20=145.0,
        moving_average_50=140.0,
        moving_average_200=130.0,

        distance_from_20_day_average=0.034,
        distance_from_50_day_average=0.071,
        distance_from_200_day_average=0.154,

        trend=MarketTrend.BULLISH,
    )

def make_fundamental_metrics() -> FundamentalMetrics:
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

class FakeMarketService:
    def analyze(
        self,
        **kwargs,
    ) -> MarketAnalysisResult:
        return MarketAnalysisResult(
            ticker="TEST",
            fetched_at=datetime.now(
                timezone.utc
            ),
            source="test",
            metrics=make_market_metrics(),
        )

class FakeFundamentalService:
    def analyze(
        self,
        **kwargs,
    ) -> FundamentalMetrics:
        return make_fundamental_metrics()

class FakeMarketAgent:
    def analyze(
        self,
        metrics: MarketMetrics,
    ) -> MarketAgentOutput:
        return MarketAgentOutput(
            ticker="TEST",
            momentum="positive",
            risk_level="moderate",
            trend_summary="Trend is positive.",
            short_term_view="Recent performance is positive.",
            long_term_price_view="Long-term price trend is positive.",
            positive_signals=[
                "Price is above moving averages."
            ],
            negative_signals=[
                "Volatility remains meaningful."
            ],
            evidence=[
                {
                    "metric": "return_1_year",
                    "value": "20%",
                    "interpretation": "One-year return was positive.",
                },
                {
                    "metric": "maximum_drawdown",
                    "value": "-30%",
                    "interpretation": "Historical drawdown was significant.",
                },
            ],
            limitations=[
                "No fundamentals included."
            ],
            data_start_date="2021-01-01",
            data_end_date="2025-12-31",
            conclusion="Positive momentum with material risk.",
        )

def make_article() -> NewsArticle:
    now = datetime(
        2025,
        12,
        1,
        tzinfo=timezone.utc,
    )

    return NewsArticle(
        article_id="article-1",
        ticker="TEST",
        title="Company reports new development",
        summary="Example financial development.",
        publisher="Example",
        url="https://example.com/story",
        published_at=now,
        source="test",
        fetched_at=now,
    )

class FakeFundamentalAgent:
    def analyze(
        self,
        metrics: FundamentalMetrics,
    ) -> FundamentalAgentOutput:
        return FundamentalAgentOutput(
            ticker="TEST",
            fiscal_year=2025,

            growth="strong",
            profitability="moderate",
            cash_flow="strong",
            balance_sheet="moderate",

            growth_summary=(
                "Revenue and net income increased."
            ),

            profitability_summary=(
                "The company remained profitable "
                "with positive operating and net margins."
            ),

            cash_flow_summary=(
                "Operating cash flow and free cash flow "
                "were positive."
            ),

            balance_sheet_summary=(
                "Liabilities were meaningful relative "
                "to stockholders' equity."
            ),

            strengths=[
                "Revenue growth was positive.",
                "Net income growth was positive.",
                "Free cash flow was positive.",
            ],

            weaknesses=[
                "Liabilities exceeded stockholders' equity."
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
                    "value": "220",
                    "interpretation": (
                        "The company generated positive "
                        "free cash flow."
                    ),
                },
            ],

            limitations=[
                "No valuation information was included."
            ],

            conclusion=(
                "The company shows positive growth, "
                "profitability and cash generation, "
                "while its liabilities remain material."
            ),
        )

class FakeNewsRetriever:
    def retrieve(
        self,
        **kwargs,
    ) -> list[RetrievedNewsArticle]:
        return [
            RetrievedNewsArticle(
                article=make_article(),
                semantic_score=0.85,
            )
        ]

class FakeNewsAgent:
    def analyze(
        self,
        *,
        ticker: str,
        articles: list[NewsArticle],
    ) -> NewsAgentOutput:
        return NewsAgentOutput(
            ticker="TEST",
            article_count=1,
            distinct_event_count=1,
            overall_sentiment="positive",
            events=[
                {
                    "event_id": "event_1",
                    "event_type": "product",
                    "headline": "New development",
                    "summary": "A material company development was reported.",
                    "sentiment": "positive",
                    "materiality": "moderate",
                    "time_horizon": "medium_term",
                    "supporting_article_ids": [
                        "article-1"
                    ],
                    "positive_factors": [
                        "Potential business benefit."
                    ],
                    "negative_factors": [],
                    "uncertainties": [
                        "Limited source detail."
                    ],
                }
            ],
            overall_summary="Recent news is positive.",
            major_positive_developments=[
                "New company development."
            ],
            major_negative_developments=[],
            limitations=[
                "Limited news sample."
            ],
        )

def test_research_coordinator_builds_bundle() -> None:
    coordinator = ResearchCoordinator(
        market_service=FakeMarketService(),
        market_agent=FakeMarketAgent(),
        fundamental_service=FakeFundamentalService(),
        fundamental_agent=FakeFundamentalAgent(),
        news_retriever=FakeNewsRetriever(),
        news_agent=FakeNewsAgent(),
    )

    result = coordinator.research(
        ticker="TEST",
        fiscal_year=2025,
        market_years=5,
        news_query="material developments",
        news_limit=10,
        as_of=datetime(
            2025,
            12,
            31,
            tzinfo=timezone.utc,
        ),
        refresh_market=False,
        refresh_fundamentals=False,
    )

    assert result.ticker == "TEST"

    assert (
        result.market_metrics.ticker
        == "TEST"
    )

    assert (
        result.fundamental_metrics.fiscal_year
        == 2025
    )

    assert len(
        result.retrieved_news
    ) == 1

    assert (
        result.news_analysis.distinct_event_count
        == 1
    )


class EmptyNewsRetriever:
    def retrieve(
        self,
        **kwargs,
    ):
        return []

import pytest


def test_coordinator_requires_news() -> None:
    coordinator = ResearchCoordinator(
        market_service=FakeMarketService(),
        market_agent=FakeMarketAgent(),
        fundamental_service=FakeFundamentalService(),
        fundamental_agent=FakeFundamentalAgent(),
        news_retriever=EmptyNewsRetriever(),
        news_agent=FakeNewsAgent(),
    )

    with pytest.raises(
        RuntimeError,
        match="No relevant news",
    ):
        coordinator.research(
            ticker="TEST",
            fiscal_year=2025,
            news_query="material developments",
            as_of=datetime(
                2025,
                12,
                31,
                tzinfo=timezone.utc,
            ),
            refresh_market=False,
            refresh_fundamentals=False,
        )