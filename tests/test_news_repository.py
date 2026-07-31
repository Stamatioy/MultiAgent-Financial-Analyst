from datetime import datetime, timezone

import duckdb

from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.models import NewsArticle


def make_article(
    *,
    article_id: str,
    title: str,
) -> NewsArticle:
    return NewsArticle(
        article_id=article_id,
        ticker="TEST",
        title=title,
        summary="Example summary.",
        publisher="Example News",
        url=f"https://example.com/{article_id}",
        published_at=datetime(
            2026,
            7,
            30,
            12,
            0,
            tzinfo=timezone.utc,
        ),
        source="test",
        fetched_at=datetime.now(
            timezone.utc
        ),
    )


def test_store_news_article() -> None:
    connection = duckdb.connect(
        ":memory:"
    )

    try:
        repository = NewsRepository(
            connection
        )

        article = make_article(
            article_id="abc",
            title="Example article",
        )

        result = repository.upsert_articles(
            [article]
        )

        assert result == 1
        assert repository.count_articles(
            "TEST"
        ) == 1

    finally:
        connection.close()


def test_upsert_does_not_duplicate() -> None:
    connection = duckdb.connect(
        ":memory:"
    )

    try:
        repository = NewsRepository(
            connection
        )

        article = make_article(
            article_id="same-id",
            title="Example",
        )

        repository.upsert_articles(
            [article]
        )

        repository.upsert_articles(
            [article]
        )

        assert repository.count_articles(
            "TEST"
        ) == 1

    finally:
        connection.close()