from __future__ import annotations

import duckdb
import pandas as pd

from financial_analyst.fundamentals.models import FinancialFact


class FundamentalRepository:
    def __init__(
        self,
        connection: duckdb.DuckDBPyConnection,
    ) -> None:
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS financial_facts (
                ticker VARCHAR NOT NULL,
                cik BIGINT NOT NULL,

                concept VARCHAR NOT NULL,
                unit VARCHAR NOT NULL,

                fiscal_year INTEGER,
                fiscal_period VARCHAR,

                form VARCHAR NOT NULL,
                filing_date DATE NOT NULL,
                period_start DATE,
                period_end DATE NOT NULL,

                accession_number VARCHAR NOT NULL,

                value DOUBLE NOT NULL,

                updated_at TIMESTAMP
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (
                    ticker,
                    concept,
                    unit,
                    period_end,
                    accession_number
                )
            )
            """
        )

    def upsert_facts(
        self,
        facts: list[FinancialFact],
    ) -> int:
        if not facts:
            return 0

        rows = [
            fact.model_dump(mode="python")
            for fact in facts
        ]

        frame = pd.DataFrame(rows)

        self.connection.register(
            "incoming_financial_facts",
            frame,
        )

        try:
            self.connection.execute(
                """
                INSERT OR REPLACE INTO financial_facts
                SELECT
                    ticker,
                    cik,
                    concept,
                    unit,
                    fiscal_year,
                    fiscal_period,
                    form,
                    filing_date,
                    period_start,
                    period_end,
                    accession_number,
                    value,
                    CURRENT_TIMESTAMP
                FROM incoming_financial_facts
                """
            )
        finally:
            self.connection.unregister(
                "incoming_financial_facts"
            )

        return len(frame)

    def get_facts(
        self,
        *,
        ticker: str,
    ) -> pd.DataFrame:
        return self.connection.execute(
            """
            SELECT
                ticker,
                cik,
                concept,
                unit,
                fiscal_year,
                fiscal_period,
                form,
                filing_date,
                period_start,
                period_end,
                accession_number,
                value
            FROM financial_facts
            WHERE ticker = ?
            ORDER BY
                fiscal_year,
                period_end,
                filing_date
            """,
            [ticker],
        ).fetchdf()