from __future__ import annotations

from abc import ABC, abstractmethod

from financial_analyst.news.models import NewsArticle


class NewsProviderError(RuntimeError):
    """Raised when a news provider fails."""


class NewsProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_news(
        self,
        *,
        ticker: str,
        limit: int = 20,
    ) -> list[NewsArticle]:
        raise NotImplementedError