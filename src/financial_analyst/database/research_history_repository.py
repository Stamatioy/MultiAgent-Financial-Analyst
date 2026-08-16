from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

import duckdb

from financial_analyst.committee.models import (
    CompanyInvestmentReport,
)


class ResearchHistoryRepository:
    def __init__(
        self,
        connection: duckdb.DuckDBPyConnection,
    ) -> None:
        self.connection = connection

        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS research_history (
                research_id VARCHAR PRIMARY KEY,
                ticker VARCHAR NOT NULL,

                generated_at TIMESTAMP NOT NULL,

                recommendation VARCHAR NOT NULL,
                conviction VARCHAR NOT NULL,
                confidence_score DOUBLE NOT NULL,
                investment_horizon VARCHAR NOT NULL,

                report_json VARCHAR NOT NULL,

                created_at TIMESTAMP
                    NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def save(
        self,
        report: CompanyInvestmentReport,
    ) -> str:
        research_id = str(
            uuid4()
        )

        committee = report.committee

        report_json = (
            report.model_dump_json()
        )

        self.connection.execute(
            """
            INSERT INTO research_history (
                research_id,
                ticker,
                generated_at,
                recommendation,
                conviction,
                confidence_score,
                investment_horizon,
                report_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                research_id,
                report.ticker,
                report.generated_at,
                committee.recommendation.value,
                committee.conviction.value,
                committee.confidence_score,
                committee.investment_horizon.value,
                report_json,
            ],
        )

        return research_id

    def list_history(
        self,
        *,
        limit: int = 50,
    ) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT
                research_id,
                ticker,
                generated_at,
                recommendation,
                conviction,
                confidence_score,
                investment_horizon
            FROM research_history
            ORDER BY generated_at DESC
            LIMIT ?
            """,
            [
                limit
            ],
        ).fetchall()

        return [
            {
                "research_id": row[0],
                "ticker": row[1],
                "generated_at": row[2],
                "recommendation": row[3],
                "conviction": row[4],
                "confidence_score": row[5],
                "investment_horizon": row[6],
            }
            for row in rows
        ]

    def get_report(
        self,
        research_id: str,
    ) -> CompanyInvestmentReport:
        row = self.connection.execute(
            """
            SELECT report_json
            FROM research_history
            WHERE research_id = ?
            """,
            [
                research_id
            ],
        ).fetchone()

        if row is None:
            raise KeyError(
                research_id
            )

        data = json.loads(
            row[0]
        )

        return (
            CompanyInvestmentReport
            .model_validate(
                data
            )
        )

    def delete(
        self,
        research_id: str,
    ) -> bool:
        exists = self.connection.execute(
            """
            SELECT 1
            FROM research_history
            WHERE research_id = ?
            """,
            [
                research_id
            ],
        ).fetchone()

        if exists is None:
            return False

        self.connection.execute(
            """
            DELETE FROM research_history
            WHERE research_id = ?
            """,
            [
                research_id
            ],
        )

        return True