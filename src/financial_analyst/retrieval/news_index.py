from __future__ import annotations

import json
from pathlib import Path

import faiss

from financial_analyst.config import get_settings
from financial_analyst.news.models import NewsArticle
from financial_analyst.retrieval.embedding import (
    EmbeddingService,
)
from financial_analyst.retrieval.models import (
    NewsVectorMetadata,
)


def build_article_embedding_text(
    article: NewsArticle,
) -> str:
    parts = [
        article.title.strip(),
    ]

    if article.summary:
        summary = article.summary.strip()

        if summary:
            parts.append(summary)

    return "\n\n".join(parts)


class NewsVectorIndex:
    """
    Persistent FAISS index for news articles.

    DuckDB remains the source of truth.
    """

    def __init__(
        self,
        *,
        embedding_service: EmbeddingService,
        index_path: Path | None = None,
        metadata_path: Path | None = None,
    ) -> None:
        settings = get_settings()

        self.embedding_service = embedding_service

        self.index_path = (
            index_path
            or settings.news_faiss_index_path
        )

        self.metadata_path = (
            metadata_path
            or settings.news_faiss_metadata_path
        )

        self.index: faiss.Index | None = None
        self.metadata: list[
            NewsVectorMetadata
        ] = []

    def build(
        self,
        articles: list[NewsArticle],
    ) -> None:
        if not articles:
            raise ValueError(
                "Cannot build news index without articles."
            )

        texts = [
            build_article_embedding_text(article)
            for article in articles
        ]

        embeddings = (
            self.embedding_service.encode(texts)
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(embeddings)

        metadata = [
            NewsVectorMetadata(
                vector_id=index_position,
                article_id=article.article_id,
                ticker=article.ticker,
                published_at=article.published_at,
            )
            for index_position, article
            in enumerate(articles)
        ]

        self.index = index
        self.metadata = metadata

    def save(self) -> None:
        if self.index is None:
            raise RuntimeError(
                "No FAISS index has been built."
            )

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        payload = [
            item.model_dump(
                mode="json"
            )
            for item in self.metadata
        ]

        self.metadata_path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: "
                f"{self.index_path}"
            )

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"FAISS metadata not found: "
                f"{self.metadata_path}"
            )

        self.index = faiss.read_index(
            str(self.index_path)
        )

        raw_metadata = json.loads(
            self.metadata_path.read_text(
                encoding="utf-8"
            )
        )

        self.metadata = [
            NewsVectorMetadata.model_validate(
                item
            )
            for item in raw_metadata
        ]

        if self.index.ntotal != len(
            self.metadata
        ):
            raise RuntimeError(
                "FAISS index and metadata are inconsistent."
            )

    def search(
        self,
        *,
        query: str,
        top_k: int,
    ) -> list[
        tuple[NewsVectorMetadata, float]
    ]:
        if self.index is None:
            raise RuntimeError(
                "FAISS index has not been loaded."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be positive."
            )

        if self.index.ntotal == 0:
            return []

        query_vector = (
            self.embedding_service.encode_query(
                query
            )
        )

        search_k = min(
            top_k,
            self.index.ntotal,
        )

        scores, indexes = self.index.search(
            query_vector,
            search_k,
        )

        results: list[
            tuple[NewsVectorMetadata, float]
        ] = []

        for index_position, score in zip(
            indexes[0],
            scores[0],
        ):
            if index_position < 0:
                continue

            metadata = self.metadata[
                int(index_position)
            ]

            results.append(
                (
                    metadata,
                    float(score),
                )
            )

        return results