from __future__ import annotations

from financial_analyst.committee.models import (
    EvidenceSourceType,
    InvestmentCommitteeOutput,
)
from financial_analyst.llm.client import (
    LocalLLMClient,
)
from financial_analyst.llm.protocol import (
    StructuredLLMClient,
)
from financial_analyst.prompts.investment_committee import (
    INVESTMENT_COMMITTEE_SYSTEM_PROMPT,
    build_investment_committee_prompt,
)
from financial_analyst.research.models import (
    CompanyResearchBundle,
)
COMMITTEE_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "ticker",
        "recommendation",
        "conviction",
        "confidence_score",
        "investment_horizon",
        "thesis",
        "bull_case",
        "bear_case",
        "market_view",
        "fundamental_view",
        "valuation_view",
        "risk_view",
        "news_view",
        "key_catalysts",
        "key_risks",
        "evidence",
        "conditions_to_upgrade",
        "conditions_to_downgrade",
        "limitations",
        "final_summary",
    ],
    "properties": {
        "ticker": {
            "type": "string",
        },

        "recommendation": {
            "type": "string",
            "enum": [
                "strongly_attractive",
                "attractive",
                "watchlist",
                "neutral",
                "unattractive",
                "strongly_unattractive",
                "insufficient_data",
            ],
        },

        "conviction": {
            "type": "string",
            "enum": [
                "low",
                "moderate",
                "high",
            ],
        },

        "confidence_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
        },

        "investment_horizon": {
            "type": "string",
            "enum": [
                "short_term",
                "medium_term",
                "long_term",
            ],
        },

        "thesis": {
            "type": "string",
        },

        "bull_case": {
            "type": "string",
        },

        "bear_case": {
            "type": "string",
        },

        "market_view": {
            "type": "string",
        },

        "fundamental_view": {
            "type": "string",
        },

        "valuation_view": {
            "type": "string",
        },

        "risk_view": {
            "type": "string",
        },

        "news_view": {
            "type": "string",
        },

        "key_catalysts": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "key_risks": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "source_type",
                    "field",
                    "source_id",
                    "interpretation",
                ],
                "properties": {
                    "source_type": {
                        "type": "string",
                        "enum": [
                            "market_metric",
                            "fundamental_metric",
                            "valuation_metric",
                            "risk_metric",
                            "news_event",
                        ],
                    },

                    "field": {
                        "type": "string",
                    },

                    "source_id": {
                        "type": [
                            "string",
                            "null",
                        ],
                    },

                    "interpretation": {
                        "type": "string",
                    },
                },
            },
        },

        "conditions_to_upgrade": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "conditions_to_downgrade": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "limitations": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },

        "final_summary": {
            "type": "string",
        },
    },
}

class InvestmentCommitteeAgent:
    """
    Synthesizes the complete validated research bundle into
    one final investment assessment.
    """

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
        bundle: CompanyResearchBundle,
    ) -> InvestmentCommitteeOutput:
        result = self.llm_client.generate_structured(
            system_prompt=(
                INVESTMENT_COMMITTEE_SYSTEM_PROMPT
            ),
            user_prompt=(
                build_investment_committee_prompt(
                    bundle
                )
            ),
            response_model=(
                InvestmentCommitteeOutput
            ),
            response_schema=(
                COMMITTEE_RESPONSE_SCHEMA
            ),
            temperature=0.0,
            max_tokens=6000,
        )

        self._validate_grounding(
            bundle=bundle,
            result=result,
        )

        return result

    @staticmethod
    def _validate_grounding(
        *,
        bundle: CompanyResearchBundle,
        result: InvestmentCommitteeOutput,
    ) -> None:
        if result.ticker != bundle.ticker:
            raise ValueError(
                "Investment committee returned "
                "a different ticker."
            )

        allowed_metric_fields = {
            EvidenceSourceType.MARKET_METRIC: set(
                bundle.market_metrics.__class__.model_fields
            ),

            EvidenceSourceType.FUNDAMENTAL_METRIC: set(
                bundle.fundamental_metrics.__class__.model_fields
            ),

            EvidenceSourceType.VALUATION_METRIC: set(
                bundle.valuation_metrics.__class__.model_fields
            ),

            EvidenceSourceType.RISK_METRIC: set(
                bundle.risk_metrics.__class__.model_fields
            ),
        }

        allowed_event_ids = {
            event.event_id
            for event in bundle.news_analysis.events
        }

        for evidence in result.evidence:
            if (
                evidence.source_type
                == EvidenceSourceType.NEWS_EVENT
            ):
                if evidence.field != "event":
                    raise ValueError(
                        "News-event evidence must use "
                        "field='event'."
                    )

                if evidence.source_id is None:
                    raise ValueError(
                        "News-event evidence requires source_id."
                    )

                if (
                    evidence.source_id
                    not in allowed_event_ids
                ):
                    raise ValueError(
                        "Investment committee referenced "
                        "an unknown news event."
                    )

                continue

            if evidence.source_id is not None:
                raise ValueError(
                    "Metric evidence must not contain source_id."
                )

            allowed_fields = allowed_metric_fields.get(
                evidence.source_type
            )

            if allowed_fields is None:
                raise ValueError(
                    "Unsupported committee evidence source."
                )

            if evidence.field not in allowed_fields:
                raise ValueError(
                    "Investment committee referenced "
                    f"unsupported field: {evidence.field}"
                )