from __future__ import annotations

from datetime import date, datetime, timezone

from financial_analyst.analytics.market_metrics import (
    calculate_market_metrics,
)
from financial_analyst.database.price_repository import PriceRepository
from financial_analyst.market_data.models import MarketAnalysisResult
from financial_analyst.market_data.provider import MarketDataProvider
from financial_analyst.validation.ticker import normalize_ticker


class MarketDataService:
    """Coordinates retrieval, persistence and deterministic analysis."""

    def __init__(
        self,
        *,
        provider: MarketDataProvider,
        repository: PriceRepository,
    ) -> None:
        self.provider = provider
        self.repository = repository

    def analyze(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
        refresh: bool = True,
    ) -> MarketAnalysisResult:
        normalized_ticker = normalize_ticker(ticker)

        if start_date >= end_date:
            raise ValueError("start_date must be before end_date.")

        if refresh:
            downloaded = self.provider.get_daily_prices(
                ticker=normalized_ticker,
                start_date=start_date,
                end_date=end_date,
            )

            self.repository.upsert_prices(downloaded)

        stored_prices = self.repository.get_prices(
            ticker=normalized_ticker,
            start_date=start_date,
            end_date=end_date,
        )

        if stored_prices.empty:
            raise RuntimeError(
                f"No cached market data exists for {normalized_ticker}."
            )

        metrics = calculate_market_metrics(
            ticker=normalized_ticker,
            prices=stored_prices,
        )

        return MarketAnalysisResult(
            ticker=normalized_ticker,
            fetched_at=datetime.now(timezone.utc),
            source=self.provider.name,
            metrics=metrics,
        )

    def get_cached_prices(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
    ):
        normalized_ticker = (
            normalize_ticker(
                ticker
            )
        )

        return (
            self.repository.get_prices(
                ticker=(
                    normalized_ticker
                ),
                start_date=start_date,
                end_date=end_date,
            )
        )

    def get_prices(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
    ):
        normalized_ticker = (
            normalize_ticker(
                ticker
            )
        )

        return self.repository.get_prices(
            ticker=normalized_ticker,
            start_date=start_date,
            end_date=end_date,
        )