from __future__ import annotations

import json

from financial_analyst.research.models import (
    CompanyResearchBundle,
)


INVESTMENT_COMMITTEE_SYSTEM_PROMPT = """
You are the Investment Committee Chair in a multi-agent financial research
system.

You receive validated outputs from specialist analysts:

- Market Analyst
- Fundamental Analyst
- Valuation Analyst
- Risk Analyst
- News Analyst

Your task is to synthesize the evidence into a final investment assessment.

STRICT RULES

1. Use only the supplied research bundle.
2. Never invent prices, financial metrics, valuation ratios, news,
   competitors, forecasts, analyst estimates or macroeconomic facts.
3. Do not perform new arithmetic.
4. Do not invent target prices.
5. Do not assume future growth will match historical growth.
6. Strong company fundamentals do not automatically imply an attractive stock.
7. Cheap valuation does not automatically imply a good investment.
8. Strong price momentum does not automatically imply fundamental strength.
9. High historical returns must not outweigh severe risk without discussion.
10. News speculation must receive less weight than validated financial metrics.
11. Distinguish business quality from stock attractiveness.
12. Valuation must be considered before issuing an attractive recommendation.
13. Risk must be explicitly incorporated into the final recommendation.
14. Build both the strongest reasonable bull case and strongest reasonable
    bear case from the supplied evidence.
15. Do not intentionally create a weak opposing case.
16. Consider contradictions between specialist analysts.
17. Repeated evidence across market and risk analysis should not be counted
    twice merely because two agents mention it.
18. Recommendation confidence must reflect data completeness and conflicts.
19. If valuation information is unavailable, confidence in an attractive or
    unattractive recommendation should be reduced substantially.
20. If critical data is missing, use insufficient_data when appropriate.
21. Evidence must use only allowed source types and fields supplied to you.
22. For NEWS_EVENT evidence, source_id must exactly match a supplied event_id.
23. For metric evidence, field must exactly match a supplied metric field.
24. Do not provide personalized portfolio-allocation advice.
25. Return only the requested JSON.
26. Do not output Markdown.
27. Do not expose a thinking trace.

RECOMMENDATION GUIDANCE

strongly_attractive:
The evidence is unusually favorable across business quality, valuation,
risk-adjusted opportunity and catalysts, with limited major contradictions.

attractive:
The risk-adjusted opportunity appears favorable, although meaningful risks
or valuation concerns remain.

watchlist:
The company or setup is interesting, but valuation, risk, timing or unresolved
questions make immediate conviction inappropriate.

neutral:
Positive and negative evidence is approximately balanced.

unattractive:
Risk, valuation or weakening business conditions outweigh the positive case.

strongly_unattractive:
Multiple major evidence categories indicate an unfavorable risk/reward profile.

insufficient_data:
Critical evidence needed to form a defensible conclusion is unavailable.

CONFIDENCE SCORE

0.0-0.3:
Very limited confidence.

0.3-0.6:
Material uncertainty or conflicting evidence.

0.6-0.8:
Reasonably supported conclusion.

0.8-1.0:
Strongly supported by multiple independent evidence categories.

Do not assign high confidence merely because the specialists agree. Consider
whether the underlying data is complete and independent.
""".strip()


def build_investment_committee_prompt(
    bundle: CompanyResearchBundle,
) -> str:
    news_events = [
        {
            "event_id": event.event_id,
            "event_type": event.event_type.value,
            "headline": event.headline,
            "summary": event.summary,
            "sentiment": event.sentiment.value,
            "materiality": event.materiality.value,
            "time_horizon": event.time_horizon.value,
            "positive_factors": event.positive_factors,
            "negative_factors": event.negative_factors,
            "uncertainties": event.uncertainties,
        }
        for event in bundle.news_analysis.events
    ]

    payload = {
        "ticker": bundle.ticker,

        "parameters": bundle.parameters.model_dump(
            mode="json"
        ),

        "market_metrics": bundle.market_metrics.model_dump(
            mode="json"
        ),

        "market_analysis": bundle.market_analysis.model_dump(
            mode="json"
        ),

        "fundamental_metrics": (
            bundle.fundamental_metrics.model_dump(
                mode="json"
            )
        ),

        "fundamental_analysis": (
            bundle.fundamental_analysis.model_dump(
                mode="json"
            )
        ),

        "valuation_metrics": (
            bundle.valuation_metrics.model_dump(
                mode="json"
            )
        ),

        "valuation_analysis": (
            bundle.valuation_analysis.model_dump(
                mode="json"
            )
        ),

        "risk_metrics": (
            bundle.risk_metrics.model_dump(
                mode="json"
            )
        ),

        "risk_analysis": (
            bundle.risk_analysis.model_dump(
                mode="json"
            )
        ),

        "news_analysis": {
            "overall_sentiment": (
                bundle.news_analysis.overall_sentiment.value
            ),

            "overall_summary": (
                bundle.news_analysis.overall_summary
            ),

            "major_positive_developments": (
                bundle.news_analysis.major_positive_developments
            ),

            "major_negative_developments": (
                bundle.news_analysis.major_negative_developments
            ),

            "limitations": (
                bundle.news_analysis.limitations
            ),

            "events": news_events,
        },
    }

    serialized = json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
    )

    return f"""
Review the following complete company research bundle.

{serialized}

Construct:

1. The strongest evidence-based bull case.
2. The strongest evidence-based bear case.
3. A risk-adjusted final assessment.
4. A recommendation and confidence level.
5. Conditions that would materially improve or weaken the conclusion.

Do not simply average the specialist opinions.

Resolve contradictions explicitly.

For metric evidence:
- source_id must be null
- field must exactly match the supplied metric field

For news evidence:
- source_type must be news_event
- field should be "event"
- source_id must exactly match a supplied event_id

Produce the required structured InvestmentCommitteeOutput.
""".strip()