from __future__ import annotations

from datetime import datetime, timezone

import duckdb
import numpy as np

from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.retrieval.news_index import (
    NewsVectorIndex,
)
from financial_analyst.retrieval.news_retriever import (
    NewsRetriever,
)


class FakeEmbeddingService:

    @property
    def dimension(self) -> int:
        return 2

    def encode(
        self,
        texts: list[str],
    ) -> np.ndarray:
        vectors = []

        for text in texts:
            lowered = text.lower()

            vector = np.array(
                [
                    1.0
                    if "ai" in lowered
                    else 0.0,
                    1.0
                    if "earnings" in lowered
                    else 0.0,
                ],
                dtype=np.float32,
            )

            norm = np.linalg.norm(
                vector
            )

            if norm > 0:
                vector /= norm

            vectors.append(
                vector
            )

        return np.vstack(vectors)

    def encode_query(
        self,
        query: str,
    ) -> np.ndarray:
        return self.encode(
            [query]
        )


def make_article(
    article_id: str,
    ticker: str,
    title: str,
) -> NewsArticle:
    now = datetime(
        2026,
        7,
        30,
        tzinfo=timezone.utc,
    )

    return NewsArticle(
        article_id=article_id,
        ticker=ticker,
        title=title,
        summary=None,
        publisher=None,
        url=None,
        published_at=now,
        source="test",
        fetched_at=now,
    )


def test_retrieval_filters_by_ticker() -> None:
    articles = [
        make_article(
            "amd-1",
            "AMD",
            "AI accelerator growth",
        ),
        make_article(
            "nvda-1",
            "NVDA",
            "AI accelerator demand",
        ),
    ]

    connection = duckdb.connect(
        ":memory:"
    )

    try:
        repository = NewsRepository(
            connection
        )

        repository.upsert_articles(
            articles
        )

        vector_index = NewsVectorIndex(
            embedding_service=FakeEmbeddingService()
        )

        vector_index.build(
            articles
        )

        retriever = NewsRetriever(
            vector_index=vector_index,
            repository=repository,
        )

        results = retriever.retrieve(
            query="AI accelerator",
            ticker="AMD",
            limit=5,
        )

        assert len(results) == 1

        assert (
            results[0].article.ticker
            == "AMD"
        )

    finally:
        connection.close()