from __future__ import annotations

from pathlib import Path

import duckdb

from financial_analyst.config import get_settings


def get_database_connection(
    database_path: Path | None = None,
) -> duckdb.DuckDBPyConnection:
    """Create a connection to the local DuckDB database."""

    path = database_path or get_settings().market_database_path
    path.parent.mkdir(parents=True, exist_ok=True)

    return duckdb.connect(str(path))