from __future__ import annotations

from datetime import date

import duckdb
import pandas as pd

from financial_analyst.database.price_repository import PriceRepository


def make_frame(close_value: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ticker": ["TEST"],
            "trading_date": [date(2025, 1, 2)],
            "open": [100.0],
            "high": [105.0],
            "low": [98.0],
            "close": [close_value],
            "adjusted_close": [close_value],
            "volume": [1_000_000],
        }
    )


def test_upsert_and_load_prices() -> None:
    connection = duckdb.connect(":memory:")

    try:
        repository = PriceRepository(connection)

        inserted = repository.upsert_prices(
            make_frame(close_value=101.0)
        )

        assert inserted == 1

        result = repository.get_prices(
            ticker="TEST",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 3),
        )

        assert len(result) == 1
        assert result.iloc[0]["adjusted_close"] == 101.0
    finally:
        connection.close()


def test_upsert_replaces_existing_price() -> None:
    connection = duckdb.connect(":memory:")

    try:
        repository = PriceRepository(connection)

        repository.upsert_prices(
            make_frame(close_value=101.0)
        )
        repository.upsert_prices(
            make_frame(close_value=103.0)
        )

        result = repository.get_prices(
            ticker="TEST",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 3),
        )

        assert len(result) == 1
        assert result.iloc[0]["adjusted_close"] == 103.0
    finally:
        connection.close()