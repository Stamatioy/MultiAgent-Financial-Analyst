from __future__ import annotations

from datetime import datetime

import duckdb


class WatchlistRepository:
    def __init__(
        self,
        connection: duckdb.DuckDBPyConnection,
    ) -> None:
        self.connection = connection

        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                ticker VARCHAR PRIMARY KEY,

                added_at TIMESTAMP
                    NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def add(
        self,
        ticker: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT OR IGNORE INTO watchlist (
                ticker
            )
            VALUES (?)
            """,
            [
                ticker
            ],
        )

    def remove(
        self,
        ticker: str,
    ) -> bool:
        exists = self.connection.execute(
            """
            SELECT 1
            FROM watchlist
            WHERE ticker = ?
            """,
            [
                ticker
            ],
        ).fetchone()

        if exists is None:
            return False

        self.connection.execute(
            """
            DELETE FROM watchlist
            WHERE ticker = ?
            """,
            [
                ticker
            ],
        )

        return True

    def exists(
        self,
        ticker: str,
    ) -> bool:
        row = self.connection.execute(
            """
            SELECT 1
            FROM watchlist
            WHERE ticker = ?
            """,
            [
                ticker
            ],
        ).fetchone()

        return row is not None

    def list_items(
        self,
    ) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT
                w.ticker,
                w.added_at,

                h.research_id,
                h.generated_at,
                h.recommendation,
                h.conviction,
                h.confidence_score,
                h.investment_horizon

            FROM watchlist w

            LEFT JOIN LATERAL (
                SELECT
                    research_id,
                    generated_at,
                    recommendation,
                    conviction,
                    confidence_score,
                    investment_horizon

                FROM research_history

                WHERE ticker = w.ticker

                ORDER BY generated_at DESC

                LIMIT 1
            ) h
                ON TRUE

            ORDER BY
                w.added_at DESC
            """
        ).fetchall()

        return [
            {
                "ticker": row[0],
                "added_at": row[1],

                "research_id": row[2],
                "last_researched_at": row[3],

                "recommendation": row[4],
                "conviction": row[5],
                "confidence_score": row[6],
                "investment_horizon": row[7],
            }
            for row in rows
        ]