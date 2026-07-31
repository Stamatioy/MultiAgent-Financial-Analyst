from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

import yfinance as yf

from financial_analyst.news.models import NewsArticle
from financial_analyst.news.provider import (
    NewsProvider,
    NewsProviderError,
)
from financial_analyst.validation.ticker import normalize_ticker

def _build_article_id(
    *,
    url: str | None,
    title: str,
    publisher: str | None,
    published_at: datetime | None,
) -> str:
    if url:
        identity = url.strip().lower()
    else:
        timestamp = (
            published_at.isoformat()
            if published_at
            else ""
        )

        identity = "|".join(
            [
                title.strip().lower(),
                (publisher or "").strip().lower(),
                timestamp,
            ]
        )

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()

class YahooNewsProvider(NewsProvider):
    """Recent company news retrieved through yfinance."""

    @property
    def name(self) -> str:
        return "yahoo_finance"

    def get_news(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> list[NewsArticle]:
        normalized_ticker = normalize_ticker(ticker)

        if limit < 1 or limit > 100:
            raise ValueError(
                "limit must be between 1 and 100."
            )

        try:
            raw_articles = yf.Ticker(
                normalized_ticker
            ).news
        except Exception as exc:
            raise NewsProviderError(
                f"Failed to retrieve news for "
                f"{normalized_ticker}: {exc}"
            ) from exc

        if not raw_articles:
            return []

        articles: list[NewsArticle] = []

        for raw in raw_articles[:limit]:
            article = self._normalize_article(
                ticker=normalized_ticker,
                raw=raw,
            )

            if article is not None:
                articles.append(article)

        return articles

    def _normalize_article(
        self,
        *,
        ticker: str,
        raw: dict[str, Any],
    ) -> NewsArticle | None:
        content = raw.get("content")

        if isinstance(content, dict):
            return self._normalize_nested_article(
                ticker=ticker,
                raw=raw,
                content=content,
            )

        return self._normalize_legacy_article(
            ticker=ticker,
            raw=raw,
        )

    def _normalize_nested_article(
        self,
        *,
        ticker: str,
        raw: dict[str, Any],
        content: dict[str, Any],
    ) -> NewsArticle | None:
        title = self._clean_text(
            content.get("title")
        )

        if not title:
            return None

        summary = self._clean_text(
            content.get("summary")
            or content.get("description")
        )

        publisher = None

        provider_data = content.get("provider")

        if isinstance(provider_data, dict):
            publisher = self._clean_text(
                provider_data.get("displayName")
            )

        url = self._extract_url(
            content.get("canonicalUrl")
        )

        if not url:
            url = self._extract_url(
                content.get("clickThroughUrl")
            )

        published_at = self._parse_datetime(
            content.get("pubDate")
            or content.get("displayTime")
        )

        article_id = _build_article_id(
            url=url,
            title=title,
            publisher=publisher,
            published_at=published_at,
        )

        return NewsArticle(
            article_id=article_id,
            ticker=ticker,
            title=title,
            summary=summary,
            publisher=publisher,
            url=url,
            published_at=published_at,
            source=self.name,
            fetched_at=datetime.now(timezone.utc),
        )

    def _normalize_legacy_article(
        self,
        *,
        ticker: str,
        raw: dict[str, Any],
    ) -> NewsArticle | None:
        title = self._clean_text(
            raw.get("title")
        )

        if not title:
            return None

        summary = self._clean_text(
            raw.get("summary")
        )

        publisher = self._clean_text(
            raw.get("publisher")
        )

        url = self._clean_text(
            raw.get("link")
        )

        published_at = self._parse_datetime(
            raw.get("providerPublishTime")
        )

        article_id = _build_article_id(
            url=url,
            title=title,
            publisher=publisher,
            published_at=published_at,
        )

        return NewsArticle(
            article_id=article_id,
            ticker=ticker,
            title=title,
            summary=summary,
            publisher=publisher,
            url=url,
            published_at=published_at,
            source=self.name,
            fetched_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _clean_text(
        value: Any,
    ) -> str | None:
        if value is None:
            return None

        text = str(value).strip()

        return text if text else None


    @staticmethod
    def _extract_url(
        value: Any,
    ) -> str | None:
        if isinstance(value, str):
            return value.strip() or None

        if isinstance(value, dict):
            url = value.get("url")

            if isinstance(url, str):
                return url.strip() or None

        return None


    @staticmethod
    def _parse_datetime(
        value: Any,
    ) -> datetime | None:
        if value is None:
            return None

        # Older Yahoo responses use Unix timestamps.
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(
                    value,
                    tz=timezone.utc,
                )
            except (ValueError, OSError):
                return None

        if isinstance(value, str):
            text = value.strip()

            if not text:
                return None

            try:
                if text.endswith("Z"):
                    text = text[:-1] + "+00:00"

                parsed = datetime.fromisoformat(text)

                if parsed.tzinfo is None:
                    parsed = parsed.replace(
                        tzinfo=timezone.utc
                    )

                return parsed.astimezone(
                    timezone.utc
                )

            except ValueError:
                return None

        return None