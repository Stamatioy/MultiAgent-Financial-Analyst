from __future__ import annotations

from financial_analyst.agents.investment_committee import (
    InvestmentCommitteeAgent,
)
from financial_analyst.committee.models import (
    InvestmentCommitteeOutput,
)
from financial_analyst.research.models import (
    CompanyResearchBundle,
)
from datetime import (
    datetime,
    timezone,
)

from financial_analyst.committee.models import (
    CompanyInvestmentReport,
    InvestmentCommitteeOutput,
)

class InvestmentCommitteeService:
    def __init__(
        self,
        *,
        agent: InvestmentCommitteeAgent,
    ) -> None:
        self.agent = agent

    def evaluate(
        self,
        bundle: CompanyResearchBundle,
    ) -> InvestmentCommitteeOutput:
        self._validate_bundle(
            bundle
        )

        return self.agent.analyze(
            bundle
        )

    def create_report(
        self,
        bundle: CompanyResearchBundle,
    ) -> CompanyInvestmentReport:
        decision = self.evaluate(
            bundle
        )

        return CompanyInvestmentReport(
            ticker=bundle.ticker,

            generated_at=datetime.now(
                timezone.utc
            ),

            research=bundle,

            committee=decision,
        )
    
    @staticmethod
    def _validate_bundle(
        bundle: CompanyResearchBundle,
    ) -> None:
        ticker = bundle.ticker

        ticker_sources = [
            bundle.market_metrics.ticker,
            bundle.market_analysis.ticker,

            bundle.fundamental_metrics.ticker,
            bundle.fundamental_analysis.ticker,

            bundle.valuation_metrics.ticker,
            bundle.valuation_analysis.ticker,

            bundle.risk_metrics.ticker,
            bundle.risk_analysis.ticker,

            bundle.news_analysis.ticker,
        ]

        if any(
            source_ticker != ticker
            for source_ticker in ticker_sources
        ):
            raise ValueError(
                "Research bundle contains inconsistent tickers."
            )