from __future__ import annotations

import argparse
from datetime import datetime, timezone

from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.news_repository import (
    NewsRepository,
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


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Semantic search over cached news."
        )
    )

    parser.add_argument(
        "query",
        help="Natural-language search query.",
    )

    parser.add_argument(
        "--ticker",
        default=None,
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--as-of",
        default=None,
    )

    return parser.parse_args()


def parse_datetime(
    value: str | None,
) -> datetime | None:
    if value is None:
        return None

    text = value.strip()

    if text.endswith("Z"):
        text = (
            text[:-1]
            + "+00:00"
        )

    result = datetime.fromisoformat(
        text
    )

    if result.tzinfo is None:
        result = result.replace(
            tzinfo=timezone.utc
        )

    return result.astimezone(
        timezone.utc
    )


def main() -> None:
    args = parse_arguments()

    connection = (
        get_database_connection()
    )

    try:
        repository = NewsRepository(
            connection
        )

        embeddings = (
            EmbeddingService()
        )

        vector_index = NewsVectorIndex(
            embedding_service=embeddings
        )

        vector_index.load()

        retriever = NewsRetriever(
            vector_index=vector_index,
            repository=repository,
        )

        results = retriever.retrieve(
            query=args.query,
            ticker=args.ticker,
            limit=args.limit,
            as_of=parse_datetime(
                args.as_of
            ),
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):
            article = result.article

            print(
                f"\n#{rank} "
                f"score={result.semantic_score:.4f}"
            )

            print(
                f"{article.ticker} | "
                f"{article.published_at}"
            )

            print(
                article.title
            )

            if article.summary:
                print(
                    article.summary
                )

    finally:
        connection.close()


if __name__ == "__main__":
    main()