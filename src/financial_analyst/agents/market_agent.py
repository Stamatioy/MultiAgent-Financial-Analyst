from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from financial_analyst.llm.client import LocalLLMClient
from financial_analyst.llm.protocol import StructuredLLMClient
from financial_analyst.market_data.models import MarketMetrics
from financial_analyst.prompts.market_agent import (
    MARKET_AGENT_SYSTEM_PROMPT,
    build_market_agent_prompt,
)


class StrictAgentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MomentumAssessment(str, Enum):
    STRONGLY_POSITIVE = "strongly_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    STRONGLY_NEGATIVE = "strongly_negative"
    INSUFFICIENT_DATA = "insufficient_data"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    INSUFFICIENT_DATA = "insufficient_data"


class EvidenceItem(StrictAgentModel):
    metric: str = Field(
        min_length=1,
        max_length=80,
        description="Exact input metric supporting the interpretation.",
    )

    value: str = Field(
        min_length=1,
        max_length=80,
        description="Metric value formatted for human reading.",
    )

    interpretation: str = Field(
        min_length=1,
        max_length=300,
        description="Conservative explanation of what the value indicates.",
    )


class MarketAgentOutput(StrictAgentModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    momentum: MomentumAssessment

    risk_level: RiskLevel

    trend_summary: str = Field(
        min_length=1,
        max_length=600,
    )

    short_term_view: str = Field(
        min_length=1,
        max_length=500,
    )

    long_term_price_view: str = Field(
        min_length=1,
        max_length=500,
    )

    positive_signals: list[str] = Field(
        max_length=5,
    )

    negative_signals: list[str] = Field(
        max_length=5,
    )

    evidence: list[EvidenceItem] = Field(
        min_length=2,
        max_length=8,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=5,
    )

    data_start_date: str
    data_end_date: str

    conclusion: str = Field(
        min_length=1,
        max_length=700,
    )


class MarketAnalystAgent:
    """
    Interprets deterministic market metrics.

    This agent does not fetch prices, calculate metrics, or issue a final
    investment recommendation.
    """

    def __init__(
        self,
        llm_client: StructuredLLMClient | None = None,
    ) -> None:
        self.llm_client = llm_client or LocalLLMClient()

    def analyze(
        self,
        metrics: MarketMetrics,
    ) -> MarketAgentOutput:
        prompt = build_market_agent_prompt(metrics)

        result = self.llm_client.generate_structured(
            system_prompt=MARKET_AGENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            response_model=MarketAgentOutput,
            temperature=0.1,
            max_tokens=1800,
        )

        self._validate_grounding(
            metrics=metrics,
            result=result,
        )

        return result

    @staticmethod
    def _validate_grounding(
        *,
        metrics: MarketMetrics,
        result: MarketAgentOutput,
    ) -> None:
        """
        Validate facts that can be checked without another LLM call.
        """

        if result.ticker != metrics.ticker:
            raise ValueError(
                "Market agent returned a different ticker: "
                f"expected {metrics.ticker}, received {result.ticker}."
            )

        expected_start = metrics.start_date.isoformat()
        expected_end = metrics.end_date.isoformat()

        if result.data_start_date != expected_start:
            raise ValueError(
                "Market agent returned an incorrect data_start_date."
            )

        if result.data_end_date != expected_end:
            raise ValueError(
                "Market agent returned an incorrect data_end_date."
            )