from __future__ import annotations

import duckdb

from financial_analyst.agents.investment_committee import (
    InvestmentCommitteeAgent,
)
from financial_analyst.committee.pipeline import (
    InvestmentResearchPipeline,
)
from financial_analyst.committee.service import (
    InvestmentCommitteeService,
)
from financial_analyst.research.factory import (
    build_research_coordinator,
)
from financial_analyst.sec.client import (
    SECClient,
)


def build_investment_pipeline(
    *,
    connection: duckdb.DuckDBPyConnection,
    sec_client: SECClient,
) -> InvestmentResearchPipeline:
    coordinator = build_research_coordinator(
        connection=connection,
        sec_client=sec_client,
    )

    committee = InvestmentCommitteeService(
        agent=InvestmentCommitteeAgent()
    )

    return InvestmentResearchPipeline(
        coordinator=coordinator,
        committee=committee,
    )