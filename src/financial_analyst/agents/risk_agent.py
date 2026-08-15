from __future__ import annotations

from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from financial_analyst.llm.client import (
    LocalLLMClient,
)
from financial_analyst.llm.protocol import (
    StructuredLLMClient,
)
from financial_analyst.prompts.risk_agent import (
    RISK_AGENT_SYSTEM_PROMPT,
    build_risk_agent_prompt,
)
from financial_analyst.risk.models import (
    RiskMetrics,
)


class StrictAgentModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )


class RiskAssessment(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    INSUFFICIENT_DATA = (
        "insufficient_data"
    )


class RiskEvidenceItem(StrictAgentModel):
    metric: str = Field(
        min_length=1,
        max_length=100,
    )

    interpretation: str = Field(
        min_length=1,
        max_length=400,
    )


class RiskAgentOutput(StrictAgentModel):
    ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    benchmark_ticker: str = Field(
        min_length=1,
        max_length=15,
    )

    overall_risk: RiskAssessment

    market_risk: RiskAssessment
    downside_risk: RiskAssessment
    financial_risk: RiskAssessment
    liquidity_risk: RiskAssessment

    market_risk_summary: str = Field(
        min_length=1,
        max_length=700,
    )

    downside_risk_summary: str = Field(
        min_length=1,
        max_length=700,
    )

    financial_risk_summary: str = Field(
        min_length=1,
        max_length=700,
    )

    liquidity_risk_summary: str = Field(
        min_length=1,
        max_length=700,
    )

    risk_factors: list[str] = Field(
        max_length=8,
    )

    risk_mitigants: list[str] = Field(
        max_length=8,
    )

    evidence: list[
        RiskEvidenceItem
    ] = Field(
        min_length=2,
        max_length=12,
    )

    limitations: list[str] = Field(
        min_length=1,
        max_length=8,
    )

    conclusion: str = Field(
        min_length=1,
        max_length=1000,
    )


class RiskAnalystAgent:
    ALLOWED_EVIDENCE_METRICS = {
        "annualized_volatility",
        "downside_deviation",
        "beta",
        "benchmark_correlation",
        "sharpe_ratio",
        "sortino_ratio",
        "daily_var_95",
        "daily_cvar_95",
        "worst_daily_return",
        "worst_weekly_return",
        "worst_monthly_return",
        "maximum_drawdown",
        "max_drawdown_duration_days",
        "average_daily_volume_20",
        "average_daily_dollar_volume_20",
        "net_debt",
        "debt_to_free_cash_flow",
    }

    def __init__(
        self,
        llm_client: (
            StructuredLLMClient
            | None
        ) = None,
    ) -> None:
        self.llm_client = (
            llm_client
            or LocalLLMClient()
        )

    def analyze(
        self,
        metrics: RiskMetrics,
    ) -> RiskAgentOutput:
        result = (
            self.llm_client.generate_structured(
                system_prompt=(
                    RISK_AGENT_SYSTEM_PROMPT
                ),
                user_prompt=(
                    build_risk_agent_prompt(
                        metrics
                    )
                ),
                response_model=(
                    RiskAgentOutput
                ),
                temperature=0.1,
                max_tokens=2600,
            )
        )

        self._validate_grounding(
            metrics=metrics,
            result=result,
        )

        return result

    @classmethod
    def _validate_grounding(
        cls,
        *,
        metrics: RiskMetrics,
        result: RiskAgentOutput,
    ) -> None:
        if result.ticker != metrics.ticker:
            raise ValueError(
                "Risk agent returned "
                "a different ticker."
            )

        if (
            result.benchmark_ticker
            != metrics.benchmark_ticker
        ):
            raise ValueError(
                "Risk agent returned "
                "a different benchmark ticker."
            )

        for item in result.evidence:
            if (
                item.metric
                not in cls.ALLOWED_EVIDENCE_METRICS
            ):
                raise ValueError(
                    "Risk agent referenced "
                    f"unsupported metric: "
                    f"{item.metric}"
                )