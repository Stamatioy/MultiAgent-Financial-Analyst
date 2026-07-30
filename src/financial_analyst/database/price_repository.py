from __future__ import annotations

from datetime import date

import duckdb
import pandas as pd


class PriceRepository:
    """Persistence layer for normalized daily market prices."""

    def __init__(
        self,
        connection: duckdb.DuckDBPyConnection,
    ) -> None:
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS prices_daily (
                ticker VARCHAR NOT NULL,
                trading_date DATE NOT NULL,
                open DOUBLE NOT NULL,
                high DOUBLE NOT NULL,
                low DOUBLE NOT NULL,
                close DOUBLE NOT NULL,
                adjusted_close DOUBLE NOT NULL,
                volume BIGINT NOT NULL,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ticker, trading_date)
            )
            """
        )

    def upsert_prices(self, prices: pd.DataFrame) -> int:
        """Insert new rows and replace existing ticker/date rows."""

        if prices.empty:
            return 0

        required_columns = [
            "ticker",
            "trading_date",
            "open",
            "high",
            "low",
            "close",
            "adjusted_close",
            "volume",
        ]

        missing = set(required_columns).difference(prices.columns)

        if missing:
            raise ValueError(
                f"Price DataFrame is missing columns: {sorted(missing)}"
            )

        upload_frame = prices[required_columns].copy()

        self.connection.register(
            "incoming_prices",
            upload_frame,
        )

        try:
            self.connection.execute(
                """
                INSERT OR REPLACE INTO prices_daily (
                    ticker,
                    trading_date,
                    open,
                    high,
                    low,
                    close,
                    adjusted_close,
                    volume,
                    updated_at
                )
                SELECT
                    ticker,
                    trading_date,
                    open,
                    high,
                    low,
                    close,
                    adjusted_close,
                    volume,
                    CURRENT_TIMESTAMP
                FROM incoming_prices
                """
            )
        finally:
            self.connection.unregister("incoming_prices")

        return len(upload_frame)

    def get_prices(
        self,
        *,
        ticker: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """Load stored daily prices inclusively between two dates."""

        return self.connection.execute(
            """
            SELECT
                ticker,
                trading_date,
                open,
                high,
                low,
                close,
                adjusted_close,
                volume
            FROM prices_daily
            WHERE ticker = ?
              AND trading_date >= ?
              AND trading_date <= ?
            ORDER BY trading_date
            """,
            [ticker, start_date, end_date],
        ).fetchdf()

    def get_latest_date(self, ticker: str) -> date | None:
        result = self.connection.execute(
            """
            SELECT MAX(trading_date)
            FROM prices_daily
            WHERE ticker = ?
            """,
            [ticker],
        ).fetchone()

        if result is None or result[0] is None:
            return None

        return result[0]