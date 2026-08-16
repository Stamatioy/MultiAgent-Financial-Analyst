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

                published_at TIMESTAMPTZ,
                source VARCHAR NOT NULL,

                relevance_score DOUBLE NOT NULL,

                fetched_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL
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

    def get_recent_article_models(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> list[NewsArticle]:
        frame = self.get_recent_articles(
            ticker=ticker,
            limit=limit,
        )

        if frame.empty:
            return []

        articles: list[NewsArticle] = []

        for row in frame.to_dict(
            orient="records"
        ):
            articles.append(
                NewsArticle.model_validate(row)
            )

        return articles

    def get_article_models_as_of(
        self,
        *,
        ticker: str,
        as_of: datetime,
        limit: int = 20,
    ) -> list[NewsArticle]:
        frame = self.get_articles_as_of(
            ticker=ticker,
            as_of=as_of,
            limit=limit,
        )

        if frame.empty:
            return []

        return [
            NewsArticle.model_validate(row)
            for row in frame.to_dict(
                orient="records"
            )
        ]

    def get_all_article_models(
        self,
    ) -> list[NewsArticle]:
        frame = self.connection.execute(
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
            ORDER BY
                published_at ASC NULLS LAST,
                article_id
            """
        ).fetchdf()

        if frame.empty:
            return []

        return [
            NewsArticle.model_validate(row)
            for row in frame.to_dict(
                orient="records"
            )
        ]

    def get_articles_by_ids(
        self,
        article_ids: list[str],
    ) -> dict[str, NewsArticle]:
        if not article_ids:
            return {}

        placeholders = ", ".join(
            ["?"] * len(article_ids)
        )

        frame = self.connection.execute(
            f"""
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
            WHERE article_id IN ({placeholders})
            """,
            article_ids,
        ).fetchdf()

        return {
            article.article_id: article
            for article in (
                NewsArticle.model_validate(row)
                for row in frame.to_dict(
                    orient="records"
                )
            )
        }