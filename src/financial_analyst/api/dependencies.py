from __future__ import annotations

from collections.abc import Generator

import duckdb

from financial_analyst.committee.factory import (
    build_investment_pipeline,
)
from financial_analyst.committee.pipeline import (
    InvestmentResearchPipeline,
)
from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.sec.client import (
    SECClient,
)


def get_database() -> Generator[
    duckdb.DuckDBPyConnection,
    None,
    None,
]:
    connection = get_database_connection()

    try:
        yield connection
    finally:
        connection.close()


def get_pipeline(
    connection: duckdb.DuckDBPyConnection,
) -> Generator[
    InvestmentResearchPipeline,
    None,
    None,
]:
    with SECClient() as sec_client:
        pipeline = build_investment_pipeline(
            connection=connection,
            sec_client=sec_client,
        )

        yield pipeline