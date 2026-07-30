from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class MarketDataProviderError(RuntimeError):
    """Raised when a market-data provider cannot return valid data."""


class MarketDataProvider(ABC):
    """Interface implemented by all market-price providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_daily_prices(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        Return normalized daily OHLCV data.

        Required columns:
            ticker
            trading_date
            open
            high
            low
            close
            adjusted_close
            volume
        """

        raise NotImplementedError