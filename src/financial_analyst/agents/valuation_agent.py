from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.llm.client import (
    LocalLLMClient,
)
from financial_analyst.llm.protocol import (
    StructuredLLMClient,
)
from financial_analyst.prompts.valuation_agent import (
    VALUATION_AGENT_SYSTEM_PROMPT,
    build_valuation_agent_prompt,
)
from financial_analyst.valuation.models import (
    ValuationMetrics,
)


class StrictAgentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ValuationAssessment(str, Enum):
    VERY_CHEAP = "very_cheap"
    CHEAP = "cheap"
    FAIR = "fair"
    EXPENSIVE = "expensive"
    VERY_EXPENSIVE = "very_expensive"
    INSUFFICIENT_DATA = "insufficient_data"


class ValuationRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    INSUFFICIENT_DATA = "insufficient_data"


class ValuationEvidenceItem(StrictAgentModel):
    metric: str = Field(
        min_length=1,
        max_length=80,
    )

    interpretation: str = Field(
        min_length=1,
        max_length=350,
    )


class ValuationAgentOutput(StrictAgentModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    fiscal_year: int

    overall_valuation: ValuationAssessment
    valuation_risk: ValuationRisk

    earnings_valuation_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    revenue_valuation_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    cash_flow_valuation_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    enterprise_valuation_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    valuation_supports: list[str] = Field(
        max_length=6,
    )

    valuation_concerns: list[str] = Field(
        max_length=6,
    )

    evidence: list[ValuationEvidenceItem] = Field(
        min_length=2,
        max_length=10,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=8,
    )

    conclusion: str = Field(
        min_length=1,
        max_length=900,
    )


class ValuationAnalystAgent:
    ALLOWED_EVIDENCE_METRICS = {
        "share_price",
        "shares_outstanding",
        "market_cap",
        "enterprise_value",
        "trailing_pe",
        "earnings_yield",
        "price_to_sales",
        "price_to_book",
        "ev_to_sales",
        "ev_to_operating_income",
        "free_cash_flow_yield",
        "net_cash",
        "revenue_growth",
        "net_income_growth",
        "operating_margin",
        "net_margin",
        "return_on_equity",
    }

    def __init__(
        self,
        llm_client: StructuredLLMClient | None = None,
    ) -> None:
        self.llm_client = (
            llm_client
            or LocalLLMClient()
        )

    def analyze(
        self,
        *,
        valuation: ValuationMetrics,
        fundamentals: FundamentalMetrics,
    ) -> ValuationAgentOutput:
        if valuation.ticker != fundamentals.ticker:
            raise ValueError(
                "Valuation and fundamental ticker mismatch."
            )

        result = (
            self.llm_client.generate_structured(
                system_prompt=(
                    VALUATION_AGENT_SYSTEM_PROMPT
                ),
                user_prompt=(
                    build_valuation_agent_prompt(
                        valuation=valuation,
                        fundamentals=fundamentals,
                    )
                ),
                response_model=(
                    ValuationAgentOutput
                ),
                temperature=0.1,
                max_tokens=2400,
            )
        )

        self._validate_grounding(
            valuation=valuation,
            result=result,
        )

        return result

    @classmethod
    def _validate_grounding(
        cls,
        *,
        valuation: ValuationMetrics,
        result: ValuationAgentOutput,
    ) -> None:
        if result.ticker != valuation.ticker:
            raise ValueError(
                "Valuation agent returned "
                "a different ticker."
            )

        if (
            result.fiscal_year
            != valuation.fiscal_year
        ):
            raise ValueError(
                "Valuation agent returned "
                "a different fiscal year."
            )

        for item in result.evidence:
            if (
                item.metric
                not in cls.ALLOWED_EVIDENCE_METRICS
            ):
                raise ValueError(
                    "Valuation agent referenced "
                    f"unsupported metric: {item.metric}"
                )