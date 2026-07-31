from __future__ import annotations

from datetime import datetime

import duckdb
import pandas as pd

from financial_analyst.news.models import NewsArticle


class NewsRepository:

    def __init__(
        self,
        connection: duckdb.DuckDBPyConnection,
    ) -> None:
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS news_articles (
                article_id VARCHAR PRIMARY KEY,
                ticker VARCHAR NOT NULL,

                title VARCHAR NOT NULL,
                summary VARCHAR,
                publisher VARCHAR,
                url VARCHAR,

                published_at TIMESTAMP,
                source VARCHAR NOT NULL,

                relevance_score DOUBLE NOT NULL,

                fetched_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
                idx_news_ticker_published
            ON news_articles (
                ticker,
                published_at
            )
            """
        )

    def upsert_articles(
        self,
        articles: list[NewsArticle],
    ) -> int:
        if not articles:
            return 0

        rows = [
            article.model_dump(mode="python")
            for article in articles
        ]

        frame = pd.DataFrame(rows)

        self.connection.register(
            "incoming_news_articles",
            frame,
        )

        try:
            self.connection.execute(
                """
                INSERT OR REPLACE INTO news_articles
                SELECT
                    article_id,
                    ticker,
                    title,
                    summary,
                    publisher,
                    url,
                    published_at,
                    source,
                    relevance_score,
                    fetched_at,
                    CURRENT_TIMESTAMP
                FROM incoming_news_articles
                """
            )
        finally:
            self.connection.unregister(
                "incoming_news_articles"
            )

        return len(frame)

    def get_recent_articles(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> pd.DataFrame:
        return self.connection.execute(
            """
            SELECT
                article_id,
                ticker,
                title,
                summary,
                publisher,
                url,
                published_at,
                source,
                fetched_at
            FROM news_articles
            WHERE ticker = ?
            ORDER BY
                published_at DESC NULLS LAST,
                fetched_at DESC
            LIMIT ?
            """,
            [ticker, limit],
        ).fetchdf()

    def count_articles(
        self,
        ticker: str,
    ) -> int:
        result = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM news_articles
            WHERE ticker = ?
            """,
            [ticker],
        ).fetchone()

        assert result is not None

        return int(result[0])