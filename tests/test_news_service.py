from datetime import datetime, timezone

import duckdb

from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.news.service import (
    NewsService,
)


class FakeNewsProvider:

    @property
    def name(self) -> str:
        return "fake"

    def get_news(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> list[NewsArticle]:
        now = datetime.now(
            timezone.utc
        )

        return [
            NewsArticle(
                article_id="1",
                ticker=ticker,
                title="AMD Reports Strong Earnings",
                summary=None,
                publisher="A",
                url="https://a.com/1",
                published_at=now,
                source="fake",
                fetched_at=now,
            ),
            NewsArticle(
                article_id="2",
                ticker=ticker,
                title="AMD reports strong earnings!",
                summary=None,
                publisher="B",
                url="https://b.com/2",
                published_at=now,
                source="fake",
                fetched_at=now,
            ),
        ]


def test_duplicate_titles_removed() -> None:
    connection = duckdb.connect(
        ":memory:"
    )

    try:
        repository = NewsRepository(
            connection
        )

        service = NewsService(
            provider=FakeNewsProvider(),
            repository=repository,
        )

        articles = service.refresh(
            ticker="AMD"
        )

        assert len(articles) == 1
        assert repository.count_articles(
            "AMD"
        ) == 1

    finally:
        connection.close()