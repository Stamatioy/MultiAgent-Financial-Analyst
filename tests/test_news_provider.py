from datetime import timezone

from financial_analyst.news.yahoo_provider import (
    YahooNewsProvider,
)


def test_parse_nested_yahoo_article() -> None:
    raw = {
        "id": "abc",
        "content": {
            "title": "AMD announces new AI product",
            "summary": "The company announced a new accelerator.",
            "pubDate": "2026-07-30T14:30:00Z",
            "provider": {
                "displayName": "Example News"
            },
            "canonicalUrl": {
                "url": "https://example.com/article"
            },
        },
    }

    provider = YahooNewsProvider()

    result = provider._normalize_article(
        ticker="AMD",
        raw=raw,
    )

    assert result is not None

    assert result.ticker == "AMD"
    assert result.title == (
        "AMD announces new AI product"
    )
    assert result.publisher == "Example News"
    assert result.url == (
        "https://example.com/article"
    )

    assert result.published_at is not None

    assert (
        result.published_at.tzinfo
        == timezone.utc
    )


def test_parse_legacy_article() -> None:
    raw = {
        "title": "AMD quarterly results released",
        "publisher": "Example Publisher",
        "link": "https://example.com/results",
        "providerPublishTime": 1760000000,
    }

    provider = YahooNewsProvider()

    result = provider._normalize_article(
        ticker="AMD",
        raw=raw,
    )

    assert result is not None

    assert result.publisher == (
        "Example Publisher"
    )

    assert result.published_at is not None


def test_missing_title_is_rejected() -> None:
    provider = YahooNewsProvider()

    result = provider._normalize_article(
        ticker="AMD",
        raw={
            "content": {
                "summary": "No title exists."
            }
        },
    )

    assert result is None

from financial_analyst.news.yahoo_provider import (
    _build_article_id,
)


def test_same_url_has_same_id() -> None:
    first = _build_article_id(
        url="https://example.com/story",
        title="Title One",
        publisher="Publisher",
        published_at=None,
    )

    second = _build_article_id(
        url="https://example.com/story",
        title="Completely Different Title",
        publisher=None,
        published_at=None,
    )

    assert first == second