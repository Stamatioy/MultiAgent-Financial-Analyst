from datetime import date

import duckdb

from financial_analyst.database.fundamental_repository import (
    FundamentalRepository,
)
from financial_analyst.fundamentals.models import (
    FinancialFact,
)


def test_store_financial_fact() -> None:
    connection = duckdb.connect(":memory:")

    try:
        repository = FundamentalRepository(connection)

        fact = FinancialFact(
            ticker="TEST",
            cik=123456,
            concept="Revenues",
            unit="USD",
            fiscal_year=2025,
            fiscal_period="FY",
            form="10-K",
            filing_date=date(2026, 2, 1),
            period_start=date(2025, 1, 1),
            period_end=date(2025, 12, 31),
            accession_number="0001",
            value=1_000_000.0,
        )

        inserted = repository.upsert_facts(
            [fact]
        )

        assert inserted == 1

        frame = repository.get_facts(
            ticker="TEST"
        )

        assert len(frame) == 1
        assert frame.iloc[0]["value"] == 1_000_000.0

    finally:
        connection.close()