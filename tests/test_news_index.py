from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.retrieval.news_index import (
    NewsVectorIndex,
)


class FakeEmbeddingService:

    @property
    def dimension(self) -> int:
        return 3

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
                    1.0
                    if "regulation" in lowered
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

        return np.vstack(
            vectors
        )

    def encode_query(
        self,
        query: str,
    ) -> np.ndarray:
        return self.encode(
            [query]
        )


def make_article(
    article_id: str,
    title: str,
) -> NewsArticle:
    now = datetime.now(
        timezone.utc
    )

    return NewsArticle(
        article_id=article_id,
        ticker="AMD",
        title=title,
        summary=None,
        publisher=None,
        url=None,
        published_at=now,
        source="test",
        fetched_at=now,
    )


def test_faiss_search(
    tmp_path: Path,
) -> None:
    service = FakeEmbeddingService()

    index = NewsVectorIndex(
        embedding_service=service,
        index_path=tmp_path / "news.faiss",
        metadata_path=tmp_path / "metadata.json",
    )

    index.build(
        [
            make_article(
                "ai",
                "AI product launch",
            ),
            make_article(
                "earnings",
                "Quarterly earnings report",
            ),
        ]
    )

    results = index.search(
        query="AI",
        top_k=1,
    )

    assert len(results) == 1

    metadata, score = results[0]

    assert metadata.article_id == "ai"
    assert score > 0.9

def test_save_and_load_index(
    tmp_path: Path,
) -> None:
    service = FakeEmbeddingService()

    first = NewsVectorIndex(
        embedding_service=service,
        index_path=tmp_path / "news.faiss",
        metadata_path=tmp_path / "metadata.json",
    )

    first.build(
        [
            make_article(
                "article-1",
                "AI product launch",
            )
        ]
    )

    first.save()

    second = NewsVectorIndex(
        embedding_service=service,
        index_path=tmp_path / "news.faiss",
        metadata_path=tmp_path / "metadata.json",
    )

    second.load()

    assert second.index is not None
    assert second.index.ntotal == 1
    assert (
        second.metadata[0].article_id
        == "article-1"
    )