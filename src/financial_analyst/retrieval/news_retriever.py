from __future__ import annotations

from datetime import datetime

from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.retrieval.models import (
    RetrievedNewsArticle,
)
from financial_analyst.retrieval.news_index import (
    NewsVectorIndex,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)


class NewsRetriever:
    """
    Semantic retrieval over indexed articles with metadata filtering.
    """

    def __init__(
        self,
        *,
        vector_index: NewsVectorIndex,
        repository: NewsRepository,
    ) -> None:
        self.vector_index = vector_index
        self.repository = repository

    def retrieve(
        self,
        *,
        query: str,
        ticker: str | None = None,
        limit: int = 15,
        as_of: datetime | None = None,
        published_after: datetime | None = None,
        minimum_score: float | None = None,
    ) -> list[RetrievedNewsArticle]:
        if limit < 1 or limit > 100:
            raise ValueError(
                "limit must be between 1 and 100."
            )

        normalized_ticker = (
            normalize_ticker(ticker)
            if ticker
            else None
        )
        if self.vector_index.index is None:
            return []
        # Metadata filtering happens after FAISS search.
        #
        # When filtering by ticker, search the full index so
        # articles for that ticker cannot be excluded before
        # the ticker filter is applied.
        if (
            normalized_ticker
            and self.vector_index.index
            is not None
        ):
            candidate_count = (
                self.vector_index.index.ntotal
            )

        else:
            candidate_count = max(
                limit * 10,
                100,
            )

            candidate_count = min(
                candidate_count,
                self.vector_index.index.ntotal
                if self.vector_index.index
                is not None
                else candidate_count,
            )

        raw_results = (
            self.vector_index.search(
                query=query,
                top_k=candidate_count,
            )
        )
        matching_raw = [
            (
                metadata.article_id,
                metadata.published_at,
                score,
            )
            for metadata, score
            in raw_results
            if metadata.ticker
            == normalized_ticker
        ]

        print(
            f"[NEWS DEBUG] Raw FAISS results contain "
            f"{len(matching_raw)} matches "
            f"for {normalized_ticker}"
        )

        for item in matching_raw[:5]:
            print(
                "[NEWS DEBUG] Raw match:",
                item,
            )

        filtered: list[
            tuple[str, float]
        ] = []

        for metadata, score in raw_results:
            if (
                normalized_ticker
                and metadata.ticker
                != normalized_ticker
            ):
                continue

            if (
                minimum_score is not None
                and score < minimum_score
            ):
                continue

            published_at = (
                metadata.published_at
            )

            if as_of is not None:
                if published_at is None:
                    continue

                if published_at > as_of:
                    continue

            if published_after is not None:
                if published_at is None:
                    continue

                if published_at < published_after:
                    continue

            filtered.append(
                (
                    metadata.article_id,
                    score,
                )
            )

            if len(filtered) >= limit:
                break

        article_map = (
            self.repository.get_articles_by_ids(
                [
                    article_id
                    for article_id, _
                    in filtered
                ]
            )
        )

        output: list[
            RetrievedNewsArticle
        ] = []

        for article_id, score in filtered:
            article = article_map.get(
                article_id
            )

            if article is None:
                continue

            output.append(
                RetrievedNewsArticle(
                    article=article,
                    semantic_score=score,
                )
            )

        return output