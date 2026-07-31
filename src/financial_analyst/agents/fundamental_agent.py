from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.fundamentals.models import FundamentalMetrics
from financial_analyst.llm.client import LocalLLMClient
from financial_analyst.llm.protocol import StructuredLLMClient
from financial_analyst.prompts.fundamental_agent import (
    FUNDAMENTAL_AGENT_SYSTEM_PROMPT,
    build_fundamental_agent_prompt,
)


class StrictAgentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GrowthAssessment(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    DECLINING = "declining"
    MIXED = "mixed"
    INSUFFICIENT_DATA = "insufficient_data"


class ProfitabilityAssessment(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    LOSS_MAKING = "loss_making"
    INSUFFICIENT_DATA = "insufficient_data"


class BalanceSheetAssessment(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    INSUFFICIENT_DATA = "insufficient_data"


class CashFlowAssessment(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NEGATIVE = "negative"
    INSUFFICIENT_DATA = "insufficient_data"


class FundamentalEvidenceItem(StrictAgentModel):
    metric: str = Field(
        min_length=1,
        max_length=80,
    )

    value: str = Field(
        min_length=1,
        max_length=100,
    )

    interpretation: str = Field(
        min_length=1,
        max_length=350,
    )


class FundamentalAgentOutput(StrictAgentModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    fiscal_year: int

    growth: GrowthAssessment
    profitability: ProfitabilityAssessment
    cash_flow: CashFlowAssessment
    balance_sheet: BalanceSheetAssessment

    growth_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    profitability_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    cash_flow_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    balance_sheet_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    strengths: list[str] = Field(
        max_length=6,
    )

    weaknesses: list[str] = Field(
        max_length=6,
    )

    evidence: list[FundamentalEvidenceItem] = Field(
        min_length=2,
        max_length=10,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=6,
    )

    conclusion: str = Field(
        min_length=1,
        max_length=800,
    )


class FundamentalAnalystAgent:
    """
    Interprets validated fundamental metrics.

    It does not retrieve filings or calculate ratios itself.
    """

    ALLOWED_EVIDENCE_METRICS = {
        "revenue",
        "net_income",
        "operating_income",
        "total_assets",
        "total_liabilities",
        "stockholders_equity",
        "cash_and_equivalents",
        "operating_cash_flow",
        "capital_expenditures",
        "free_cash_flow",
        "revenue_growth",
        "net_income_growth",
        "operating_margin",
        "net_margin",
        "return_on_assets",
        "return_on_equity",
        "liabilities_to_equity",
    }

    def __init__(
        self,
        llm_client: StructuredLLMClient | None = None,
    ) -> None:
        self.llm_client = llm_client or LocalLLMClient()

    def analyze(
        self,
        metrics: FundamentalMetrics,
    ) -> FundamentalAgentOutput:
        result = self.llm_client.generate_structured(
            system_prompt=FUNDAMENTAL_AGENT_SYSTEM_PROMPT,
            user_prompt=build_fundamental_agent_prompt(metrics),
            response_model=FundamentalAgentOutput,
            temperature=0.1,
            max_tokens=2200,
        )

        self._validate_grounding(
            metrics=metrics,
            result=result,
        )

        return result

    @staticmethod
    def _validate_grounding(
        *,
        metrics: FundamentalMetrics,
        result: FundamentalAgentOutput,
    ) -> None:
        if result.ticker != metrics.ticker:
            raise ValueError(
                "Fundamental agent returned a different ticker: "
                f"expected {metrics.ticker}, got {result.ticker}."
            )

        if result.fiscal_year != metrics.fiscal_year:
            raise ValueError(
                "Fundamental agent returned a different fiscal year."
            )

        for item in result.evidence:
            if (
                item.metric
                not in FundamentalAnalystAgent.ALLOWED_EVIDENCE_METRICS
            ):
                raise ValueError(
                    "Fundamental agent referenced unsupported metric: "
                    f"{item.metric}"
                )