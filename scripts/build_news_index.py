from __future__ import annotations

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


def main() -> None:
    connection = get_database_connection()

    try:
        repository = NewsRepository(
            connection
        )

        articles = (
            repository.get_all_article_models()
        )

        if not articles:
            raise RuntimeError(
                "No cached news articles exist. "
                "Fetch news before building the index."
            )

        print(
            f"Embedding {len(articles)} articles..."
        )

        embeddings = EmbeddingService()

        index = NewsVectorIndex(
            embedding_service=embeddings
        )

        index.build(
            articles
        )

        index.save()

        print(
            f"Indexed {len(articles)} articles."
        )

        print(
            f"Embedding dimension: "
            f"{embeddings.dimension}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()