from __future__ import annotations

import re

from financial_analyst.news.company_aliases import (
    COMPANY_ALIASES,
)
from financial_analyst.news.models import NewsArticle


def normalize_text(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def calculate_article_relevance(
    article: NewsArticle,
) -> float:
    aliases = COMPANY_ALIASES.get(
        article.ticker,
        [article.ticker.lower()],
    )

    title = normalize_text(
        article.title
    )

    summary = normalize_text(
        article.summary or ""
    )

    score = 0.0

    for alias in aliases:
        normalized_alias = normalize_text(alias)

        if normalized_alias in title:
            score += 0.70

        if normalized_alias in summary:
            score += 0.30

    return min(score, 1.0)