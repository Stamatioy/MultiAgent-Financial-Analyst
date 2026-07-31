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

    embedding_service = EmbeddingService()

    vector_index = NewsVectorIndex(
        embedding_service=embedding_service
    )

    vector_index.load()

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

        news_retriever=news_retriever,
        news_agent=NewsAnalystAgent(),
    )