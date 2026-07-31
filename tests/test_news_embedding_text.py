from datetime import datetime, timezone

from financial_analyst.news.models import (
    NewsArticle,
)
from financial_analyst.retrieval.news_index import (
    build_article_embedding_text,
)


def test_build_embedding_text() -> None:
    now = datetime.now(
        timezone.utc
    )

    article = NewsArticle(
        article_id="abc",
        ticker="AMD",
        title="AMD launches new accelerator",
        summary="The product targets AI workloads.",
        publisher="Example",
        url="https://example.com",
        published_at=now,
        source="test",
        fetched_at=now,
    )

    text = build_article_embedding_text(
        article
    )

    assert text == (
        "AMD launches new accelerator\n\n"
        "The product targets AI workloads."
    )