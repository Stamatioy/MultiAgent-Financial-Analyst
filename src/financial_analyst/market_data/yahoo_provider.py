from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from financial_analyst.market_data.provider import (
    MarketDataProvider,
    MarketDataProviderError,
)
from financial_analyst.validation.ticker import normalize_ticker


class YahooFinanceProvider(MarketDataProvider):
    """Historical market-price provider implemented with yfinance."""

    @property
    def name(self) -> str:
        return "yahoo_finance"

    def get_daily_prices(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        normalized_ticker = normalize_ticker(ticker)

        if start_date >= end_date:
            raise ValueError("start_date must be before end_date.")

        try:
            raw = yf.download(
                tickers=normalized_ticker,
                start=start_date.isoformat(),
                # yfinance treats end as exclusive.
                end=(end_date + timedelta(days=1)).isoformat(),
                interval="1d",
                auto_adjust=False,
                actions=False,
                progress=False,
                threads=False,
                timeout=30,
            )
        except Exception as exc:
            raise MarketDataProviderError(
                f"Failed to download prices for {normalized_ticker}: {exc}"
            ) from exc

        if raw.empty:
            raise MarketDataProviderError(
                f"No daily price data was returned for {normalized_ticker}."
            )

        frame = self._normalize_dataframe(
            raw=raw,
            ticker=normalized_ticker,
        )

        if frame.empty:
            raise MarketDataProviderError(
                f"Returned data for {normalized_ticker} contained no valid rows."
            )

        return frame

    @staticmethod
    def _normalize_dataframe(
        *,
        raw: pd.DataFrame,
        ticker: str,
    ) -> pd.DataFrame:
        frame = raw.copy()

        # yfinance may return MultiIndex columns even for one ticker.
        if isinstance(frame.columns, pd.MultiIndex):
            frame.columns = frame.columns.get_level_values(0)

        frame = frame.reset_index()

        adjusted_column = (
            "Adj Close"
            if "Adj Close" in frame.columns
            else "Close"
        )

        required_columns = {
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            adjusted_column,
            "Volume",
        }

        missing = required_columns.difference(frame.columns)

        if missing:
            raise MarketDataProviderError(
                f"Provider response is missing columns: {sorted(missing)}"
            )

        normalized = pd.DataFrame(
            {
                "ticker": ticker,
                "trading_date": pd.to_datetime(
                    frame["Date"],
                    errors="coerce",
                    utc=True,
                ).dt.date,
                "open": pd.to_numeric(frame["Open"], errors="coerce"),
                "high": pd.to_numeric(frame["High"], errors="coerce"),
                "low": pd.to_numeric(frame["Low"], errors="coerce"),
                "close": pd.to_numeric(frame["Close"], errors="coerce"),
                "adjusted_close": pd.to_numeric(
                    frame[adjusted_column],
                    errors="coerce",
                ),
                "volume": pd.to_numeric(
                    frame["Volume"],
                    errors="coerce",
                ),
            }
        )

        normalized = normalized.dropna(
            subset=[
                "trading_date",
                "open",
                "high",
                "low",
                "close",
                "adjusted_close",
                "volume",
            ]
        )

        normalized = normalized[
            (normalized["open"] > 0)
            & (normalized["high"] > 0)
            & (normalized["low"] > 0)
            & (normalized["close"] > 0)
            & (normalized["adjusted_close"] > 0)
            & (normalized["volume"] >= 0)
        ]

        normalized["volume"] = normalized["volume"].astype("int64")

        return (
            normalized
            .drop_duplicates(
                subset=["ticker", "trading_date"],
                keep="last",
            )
            .sort_values("trading_date")
            .reset_index(drop=True)
        )