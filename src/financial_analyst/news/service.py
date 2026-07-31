from __future__ import annotations

import re

from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.models import NewsArticle
from financial_analyst.news.provider import NewsProvider
from financial_analyst.news.relevance import (
    calculate_article_relevance,
)

from financial_analyst.validation.ticker import normalize_ticker


class NewsService:

    def __init__(
        self,
        *,
        provider: NewsProvider,
        repository: NewsRepository,
    ) -> None:
        self.provider = provider
        self.repository = repository

    def refresh(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> list[NewsArticle]:
        normalized_ticker = normalize_ticker(ticker)

        articles = self.provider.get_news(
            ticker=normalized_ticker,
            limit=limit,
        )

        relevant_articles: list[NewsArticle] = []

        for article in articles:
            relevance = calculate_article_relevance(
                article
            )

            article = article.model_copy(
                update={
                    "relevance_score": relevance
                }
            )

            if relevance >= 0.30:
                relevant_articles.append(article)

        unique_articles = self._deduplicate(
            relevant_articles
        )

        self.repository.upsert_articles(
            unique_articles
        )

        return unique_articles

    def _deduplicate(
        self,
        articles: list[NewsArticle],
    ) -> list[NewsArticle]:
        seen_ids: set[str] = set()
        seen_titles: set[str] = set()

        output: list[NewsArticle] = []

        for article in articles:
            title_key = self._normalize_title(
                article.title
            )

            if article.article_id in seen_ids:
                continue

            if title_key in seen_titles:
                continue

            seen_ids.add(article.article_id)
            seen_titles.add(title_key)

            output.append(article)

        return output

    @staticmethod
    def _normalize_title(
        title: str,
    ) -> str:
        normalized = title.lower()

        normalized = re.sub(
            r"[^a-z0-9]+",
            " ",
            normalized,
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()