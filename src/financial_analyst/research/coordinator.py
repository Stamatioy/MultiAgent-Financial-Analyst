from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from financial_analyst.agents.fundamental_agent import (
    FundamentalAnalystAgent,
)
from financial_analyst.agents.market_agent import (
    MarketAnalystAgent,
)
from financial_analyst.agents.news_agent import (
    NewsAnalystAgent,
)
from financial_analyst.fundamentals.service import (
    FundamentalDataService,
)
from financial_analyst.market_data.service import (
    MarketDataService,
)
from financial_analyst.research.models import (
    CompanyResearchBundle,
    ResearchParameters,
)
from financial_analyst.retrieval.news_retriever import (
    NewsRetriever,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)
from financial_analyst.agents.valuation_agent import (
    ValuationAnalystAgent,
)
from financial_analyst.valuation.service import (
    ValuationService,
)
from financial_analyst.agents.risk_agent import (
    RiskAnalystAgent,
)
from financial_analyst.risk.service import (
    RiskService,
)
from collections.abc import Callable
from typing import Any
from financial_analyst.visualization.chart_data import (
    build_drawdown_history,
    build_financial_history,
    build_price_history,
)

ProgressCallback = Callable[
    [str, str, Any | None],
    None,
]

class ResearchCoordinator:
    """
    Deterministically orchestrates specialist financial research branches.
    """

    def __init__(
        self,
        *,
        market_service: MarketDataService,
        market_agent: MarketAnalystAgent,
        fundamental_service: FundamentalDataService,
        fundamental_agent: FundamentalAnalystAgent,
        valuation_service: ValuationService,
        valuation_agent: ValuationAnalystAgent,
        risk_service: RiskService,
        risk_agent: RiskAnalystAgent,
        news_retriever: NewsRetriever,
        news_agent: NewsAnalystAgent,
    ) -> None:
        self.market_service = market_service
        self.market_agent = market_agent

        self.fundamental_service = (
            fundamental_service
        )

        self.fundamental_agent = (
            fundamental_agent
        )

        self.news_retriever = news_retriever
        self.news_agent = news_agent

        self.valuation_service = valuation_service
        self.valuation_agent = valuation_agent

        self.risk_service = risk_service
        self.risk_agent = risk_agent

    def research(
        self,
        *,
        ticker: str,
        fiscal_year: int,
        market_years: int = 5,
        benchmark_ticker: str = "^GSPC",
        risk_free_rate_annual: float = 0.0,
        news_query: str = (
            "material company developments, earnings, "
            "guidance, products, regulation and risks"
        ),
        news_limit: int = 15,
        as_of: datetime | None = None,
        refresh_market: bool = True,
        refresh_fundamentals: bool = True,
        progress_callback: (
            ProgressCallback | None
        ) = None,
    ) -> CompanyResearchBundle:
        
        def progress(
            step: str,
            status: str,
            result: Any | None = None,
        ) -> None:
            if progress_callback is not None:
                progress_callback(
                    step,
                    status,
                    result,
                )
        
        normalized_ticker = normalize_ticker(
            ticker
        )

        if (
            as_of is not None
            and as_of.tzinfo is None
        ):
            raise ValueError(
                "as_of must be timezone-aware."
            )

        if market_years < 1 or market_years > 30:
            raise ValueError(
                "market_years must be between 1 and 30."
            )

        if news_limit < 1 or news_limit > 50:
            raise ValueError(
                "news_limit must be between 1 and 50."
            )

        query = news_query.strip()

        if not query:
            raise ValueError(
                "news_query cannot be empty."
            )

        resolved_as_of = (
            as_of
            or datetime.now(timezone.utc)
        )

        market_end_date = (
            resolved_as_of.date()
        )

        market_start_date = (
            market_end_date
            - timedelta(
                days=round(
                    market_years * 365.25
                )
            )
        )
        progress(
            "market",
            "running",
        )
        market_result = (
            self.market_service.analyze(
                ticker=normalized_ticker,
                start_date=market_start_date,
                end_date=market_end_date,
                refresh=refresh_market,
            )
        )

        market_analysis = (
            self.market_agent.analyze(
                market_result.metrics
            )
        )

        market_prices = (
            self.market_service
            .get_cached_prices(
                ticker=normalized_ticker,
                start_date=market_start_date,
                end_date=market_end_date,
            )
        )

        market_progress_result = (
            market_analysis.model_dump(
                mode="json"
            )
        )

        market_progress_result[
            "_charts"
        ] = {
            "price_history": (
                build_price_history(
                    market_prices
                )
            ),
        }

        progress(
            "market",
            "completed",
            market_progress_result,
        )

        progress(
            "fundamentals",
            "running",
        )
        fundamental_metrics = (
            self.fundamental_service.analyze(
                ticker=normalized_ticker,
                fiscal_year=fiscal_year,
                refresh=refresh_fundamentals,
            )
        )

        fundamental_analysis = (
            self.fundamental_agent.analyze(
                fundamental_metrics
            )
        )
        fundamental_facts = (
            self.fundamental_service
            .get_cached_facts(
                ticker=normalized_ticker
            )
        )

        fundamental_progress_result = (
            fundamental_analysis.model_dump(
                mode="json"
            )
        )

        fundamental_progress_result[
            "_charts"
        ] = {
            "financial_history": (
                build_financial_history(
                    fundamental_facts
                )
            ),
        }

        progress(
            "fundamentals",
            "completed",
            fundamental_progress_result,
        )

        progress(
            "valuation",
            "running",
        )
        valuation_metrics = (
            self.valuation_service.analyze(
                market_metrics=market_result.metrics,
                fundamental_metrics=fundamental_metrics,
            )
        )

        valuation_analysis = (
            self.valuation_agent.analyze(
                valuation=valuation_metrics,
                fundamentals=fundamental_metrics,
            )
        )
        progress(
            "valuation",
            "completed",
            valuation_analysis,
        )

        progress(
            "risk",
            "running",
        )
        risk_metrics = (
            self.risk_service.analyze(
                ticker=normalized_ticker,
                benchmark_ticker=(
                    benchmark_ticker
                ),
                start_date=(
                    market_start_date
                ),
                end_date=(
                    market_end_date
                ),
                fundamentals=(
                    fundamental_metrics
                ),
                risk_free_rate_annual=(
                    risk_free_rate_annual
                ),
                refresh_company=False,
                refresh_benchmark=(
                    refresh_market
                ),
            )
        )

        risk_analysis = (
            self.risk_agent.analyze(
                risk_metrics
            )
        )
        risk_progress_result = (
            risk_analysis.model_dump(
                mode="json"
            )
        )

        risk_progress_result[
            "_charts"
        ] = {
            "drawdown_history": (
                build_drawdown_history(
                    market_prices
                )
            ),
        }

        progress(
            "risk",
            "completed",
            risk_progress_result,
        )

        progress(
            "news",
            "running",
        )
        retrieved_news = (
            self.news_retriever.retrieve(
                query=query,
                ticker=normalized_ticker,
                limit=news_limit,
                as_of=resolved_as_of,
            )
        )

        if not retrieved_news:
            raise RuntimeError(
                "No relevant news articles were retrieved "
                f"for {normalized_ticker}."
            )

        articles = [
            result.article
            for result in retrieved_news
        ]

        news_analysis = (
            self.news_agent.analyze(
                ticker=normalized_ticker,
                articles=articles,
            )
        )

        news_progress_result = (
            news_analysis.model_dump(
                mode="json"
            )
        )

        news_progress_result[
            "_sources"
        ] = [
            {
                "article_id": (
                    retrieved.article.article_id
                ),
                "title": (
                    retrieved.article.title
                ),
                "publisher": (
                    retrieved.article.publisher
                ),
                "url": (
                    retrieved.article.url
                ),
            }
            for retrieved in retrieved_news
        ]

        progress(
            "news",
            "completed",
            news_progress_result,
        )

        parameters = ResearchParameters(
            ticker=normalized_ticker,
            fiscal_year=fiscal_year,
            market_years=market_years,
            news_query=query,
            news_limit=news_limit,
            as_of=resolved_as_of,
            benchmark_ticker=benchmark_ticker,
            risk_free_rate_annual=(
                risk_free_rate_annual
            ),
        )

        bundle = CompanyResearchBundle(
            ticker=normalized_ticker,
            generated_at=datetime.now(
                timezone.utc
            ),
            parameters=parameters,

            market_metrics=(
                market_result.metrics
            ),

            market_analysis=(
                market_analysis
            ),

            fundamental_metrics=(
                fundamental_metrics
            ),

            fundamental_analysis=(
                fundamental_analysis
            ),

            valuation_metrics=valuation_metrics,
            valuation_analysis=valuation_analysis,

            risk_metrics=risk_metrics,
            risk_analysis=risk_analysis,

            retrieved_news=(
                retrieved_news
            ),

            news_analysis=(
                news_analysis
            ),
        )

        self._validate_bundle(
            bundle
        )

        return bundle

    @staticmethod
    def _validate_bundle(
        bundle: CompanyResearchBundle,
    ) -> None:
        ticker = bundle.ticker

        if (
            bundle.market_metrics.ticker
            != ticker
        ):
            raise ValueError(
                "Market metrics ticker mismatch."
            )

        if (
            bundle.market_analysis.ticker
            != ticker
        ):
            raise ValueError(
                "Market analysis ticker mismatch."
            )

        if (
            bundle.fundamental_metrics.ticker
            != ticker
        ):
            raise ValueError(
                "Fundamental metrics ticker mismatch."
            )

        if (
            bundle.fundamental_analysis.ticker
            != ticker
        ):
            raise ValueError(
                "Fundamental analysis ticker mismatch."
            )

        if bundle.valuation_metrics.ticker != ticker:
            raise ValueError(
                "Valuation metrics ticker mismatch."
            )

        if bundle.valuation_analysis.ticker != ticker:
            raise ValueError(
                "Valuation analysis ticker mismatch."
            )

        if (
            bundle.risk_metrics.ticker
            != ticker
        ):
            raise ValueError(
                "Risk metrics ticker mismatch."
            )

        if (
            bundle.risk_analysis.ticker
            != ticker
        ):
            raise ValueError(
                "Risk analysis ticker mismatch."
            )

        if (
            bundle.risk_metrics.benchmark_ticker
            != bundle.risk_analysis.benchmark_ticker
        ):
            raise ValueError(
                "Risk benchmark ticker mismatch."
            )
        
        if (
            bundle.news_analysis.ticker
            != ticker
        ):
            raise ValueError(
                "News analysis ticker mismatch."
            )

        for retrieved in (
            bundle.retrieved_news
        ):
            if (
                retrieved.article.ticker
                != ticker
            ):
                raise ValueError(
                    "Retrieved news ticker mismatch."
                )