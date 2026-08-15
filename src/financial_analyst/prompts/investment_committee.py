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

        "market": {
            "metrics": {
                "latest_close": (
                    bundle.market_metrics.latest_close
                ),
                "annualized_return": (
                    bundle.market_metrics.annualized_return
                ),
                "annualized_volatility": (
                    bundle.market_metrics.annualized_volatility
                ),
                "maximum_drawdown": (
                    bundle.market_metrics.maximum_drawdown
                ),
                "return_1_month": (
                    bundle.market_metrics.return_1_month
                ),
                "return_3_months": (
                    bundle.market_metrics.return_3_months
                ),
                "return_6_months": (
                    bundle.market_metrics.return_6_months
                ),
                "return_1_year": (
                    bundle.market_metrics.return_1_year
                ),
                "trend": (
                    bundle.market_metrics.trend.value
                ),
            },

            "assessment": {
                "momentum": (
                    bundle.market_analysis.momentum.value
                ),
                "risk_level": (
                    bundle.market_analysis.risk_level.value
                ),
                "conclusion": (
                    bundle.market_analysis.conclusion
                ),
            },
        },

        "fundamentals": {
            "metrics": {
                "revenue": (
                    bundle.fundamental_metrics.revenue
                ),
                "net_income": (
                    bundle.fundamental_metrics.net_income
                ),
                "free_cash_flow": (
                    bundle.fundamental_metrics.free_cash_flow
                ),
                "revenue_growth": (
                    bundle.fundamental_metrics.revenue_growth
                ),
                "net_income_growth": (
                    bundle.fundamental_metrics.net_income_growth
                ),
                "operating_margin": (
                    bundle.fundamental_metrics.operating_margin
                ),
                "net_margin": (
                    bundle.fundamental_metrics.net_margin
                ),
                "return_on_equity": (
                    bundle.fundamental_metrics.return_on_equity
                ),
                "liabilities_to_equity": (
                    bundle.fundamental_metrics.liabilities_to_equity
                ),
            },

            "assessment": {
                "growth": (
                    bundle.fundamental_analysis.growth.value
                ),
                "profitability": (
                    bundle.fundamental_analysis.profitability.value
                ),
                "cash_flow": (
                    bundle.fundamental_analysis.cash_flow.value
                ),
                "balance_sheet": (
                    bundle.fundamental_analysis.balance_sheet.value
                ),
                "strengths": (
                    bundle.fundamental_analysis.strengths
                ),
                "weaknesses": (
                    bundle.fundamental_analysis.weaknesses
                ),
                "conclusion": (
                    bundle.fundamental_analysis.conclusion
                ),
            },
        },

        "valuation": {
            "metrics": {
                "market_cap": (
                    bundle.valuation_metrics.market_cap
                ),
                "enterprise_value": (
                    bundle.valuation_metrics.enterprise_value
                ),
                "trailing_pe": (
                    bundle.valuation_metrics.trailing_pe
                ),
                "earnings_yield": (
                    bundle.valuation_metrics.earnings_yield
                ),
                "price_to_sales": (
                    bundle.valuation_metrics.price_to_sales
                ),
                "price_to_book": (
                    bundle.valuation_metrics.price_to_book
                ),
                "ev_to_sales": (
                    bundle.valuation_metrics.ev_to_sales
                ),
                "ev_to_operating_income": (
                    bundle.valuation_metrics.ev_to_operating_income
                ),
                "free_cash_flow_yield": (
                    bundle.valuation_metrics.free_cash_flow_yield
                ),
            },

            "assessment": {
                "overall_valuation": (
                    bundle.valuation_analysis
                    .overall_valuation.value
                ),
                "valuation_risk": (
                    bundle.valuation_analysis
                    .valuation_risk.value
                ),
                "supports": (
                    bundle.valuation_analysis
                    .valuation_supports
                ),
                "concerns": (
                    bundle.valuation_analysis
                    .valuation_concerns
                ),
                "conclusion": (
                    bundle.valuation_analysis.conclusion
                ),
            },
        },

        "risk": {
            "metrics": {
                "annualized_volatility": (
                    bundle.risk_metrics.annualized_volatility
                ),
                "beta": (
                    bundle.risk_metrics.beta
                ),
                "sharpe_ratio": (
                    bundle.risk_metrics.sharpe_ratio
                ),
                "sortino_ratio": (
                    bundle.risk_metrics.sortino_ratio
                ),
                "daily_var_95": (
                    bundle.risk_metrics.daily_var_95
                ),
                "daily_cvar_95": (
                    bundle.risk_metrics.daily_cvar_95
                ),
                "worst_daily_return": (
                    bundle.risk_metrics.worst_daily_return
                ),
                "worst_monthly_return": (
                    bundle.risk_metrics.worst_monthly_return
                ),
                "maximum_drawdown": (
                    bundle.risk_metrics.maximum_drawdown
                ),
                "max_drawdown_duration_days": (
                    bundle.risk_metrics
                    .max_drawdown_duration_days
                ),
                "net_debt": (
                    bundle.risk_metrics.net_debt
                ),
            },

            "assessment": {
                "overall_risk": (
                    bundle.risk_analysis.overall_risk.value
                ),
                "risk_factors": (
                    bundle.risk_analysis.risk_factors
                ),
                "risk_mitigants": (
                    bundle.risk_analysis.risk_mitigants
                ),
                "conclusion": (
                    bundle.risk_analysis.conclusion
                ),
            },
        },

        "news": {
            "overall_sentiment": (
                bundle.news_analysis
                .overall_sentiment.value
            ),

            "positive_developments": (
                bundle.news_analysis
                .major_positive_developments
            ),

            "negative_developments": (
                bundle.news_analysis
                .major_negative_developments
            ),

            "events": news_events,
        },
    }

    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
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