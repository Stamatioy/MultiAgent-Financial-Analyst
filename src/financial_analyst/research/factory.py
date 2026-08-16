from __future__ import annotations

import duckdb

from financial_analyst.agents.fundamental_agent import (
    FundamentalAnalystAgent,
)
from financial_analyst.agents.market_agent import (
    MarketAnalystAgent,
)
from financial_analyst.agents.news_agent import (
    NewsAnalystAgent,
)
from financial_analyst.database.fundamental_repository import (
    FundamentalRepository,
)
from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.database.price_repository import (
    PriceRepository,
)
from financial_analyst.fundamentals.service import (
    FundamentalDataService,
)
from financial_analyst.market_data.service import (
    MarketDataService,
)
from financial_analyst.market_data.yahoo_provider import (
    YahooFinanceProvider,
)
from financial_analyst.research.coordinator import (
    ResearchCoordinator,
)
from financial_analyst.retrieval.embedding import (
    EmbeddingService,
)
from financial_analyst.retrieval.news_index import (
    NewsVectorIndex,
)
from financial_analyst.retrieval.news_retriever import (
    NewsRetriever,
)
from financial_analyst.sec.client import (
    SECClient,
)
from financial_analyst.sec.company_facts import (
    SECCompanyFactsParser,
)
from financial_analyst.sec.ticker_map import (
    SECTickerMapper,
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
from financial_analyst.news.service import (
    NewsService,
)
from financial_analyst.news.yahoo_provider import (
    YahooNewsProvider,
)


def build_research_coordinator(
    *,
    connection: duckdb.DuckDBPyConnection,
    sec_client: SECClient,
) -> ResearchCoordinator:
    price_repository = PriceRepository(
        connection
    )

    fundamental_repository = (
        FundamentalRepository(
            connection
        )
    )

    news_repository = NewsRepository(
        connection
    )
    news_service = NewsService(
        provider=YahooNewsProvider(),
        repository=news_repository,
    )

    market_service = MarketDataService(
        provider=YahooFinanceProvider(),
        repository=price_repository,
    )

    fundamental_service = (
        FundamentalDataService(
            ticker_mapper=SECTickerMapper(
                sec_client
            ),
            company_facts=(
                SECCompanyFactsParser(
                    sec_client
                )
            ),
            repository=(
                fundamental_repository
            ),
        )
    )

    valuation_service=ValuationService(),
    valuation_agent=ValuationAnalystAgent(),

    risk_service = RiskService(
        market_service=market_service,
        repository=price_repository,
    )

    embedding_service = EmbeddingService()

    vector_index = NewsVectorIndex(
        embedding_service=embedding_service
    )

    try:
        vector_index.load()

    except FileNotFoundError:
        articles = (
            news_repository
            .get_all_article_models()
        )

        if articles:
            vector_index.build(
                articles
            )

            vector_index.save()

    news_retriever = NewsRetriever(
        vector_index=vector_index,
        repository=news_repository,
    )

    return ResearchCoordinator(
        market_service=market_service,
        market_agent=MarketAnalystAgent(),

        fundamental_service=(
            fundamental_service
        ),

        fundamental_agent=(
            FundamentalAnalystAgent()
        ),

        risk_service=risk_service,
        risk_agent=RiskAnalystAgent(),

        valuation_service=ValuationService(),
        valuation_agent=ValuationAnalystAgent(),

        news_retriever=news_retriever,
        news_service=news_service,
        news_agent=NewsAnalystAgent(),
    )