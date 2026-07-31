from __future__ import annotations

import pandas as pd

from financial_analyst.fundamentals.concepts import (
    CONCEPT_ALIASES,
)
from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)


def _safe_divide(
    numerator: float | None,
    denominator: float | None,
) -> float | None:
    if (
        numerator is None
        or denominator is None
        or denominator == 0
    ):
        return None

    return float(numerator / denominator)


def _growth(
    current: float | None,
    previous: float | None,
) -> float | None:
    if (
        current is None
        or previous is None
        or previous == 0
    ):
        return None

    return float(current / previous - 1.0)


def select_annual_fact(
    facts: pd.DataFrame,
    *,
    logical_name: str,
    fiscal_year: int,
) -> float | None:
    aliases = CONCEPT_ALIASES[logical_name]

    subset = facts[
        (facts["concept"].isin(aliases))
        & (facts["fiscal_year"] == fiscal_year)
        & (facts["form"] == "10-K")
        & (facts["unit"] == "USD")
    ].copy()

    if subset.empty:
        return None

    # Prefer FY contexts.
    fy_rows = subset[
        subset["fiscal_period"] == "FY"
    ]

    if not fy_rows.empty:
        subset = fy_rows

    # Prefer alias order.
    alias_priority = {
        concept: index
        for index, concept in enumerate(aliases)
    }

    subset["concept_priority"] = (
        subset["concept"]
        .map(alias_priority)
        .fillna(999)
    )

    # Later filings win so amended/restated values supersede old ones.
    subset = subset.sort_values(
        by=[
            "concept_priority",
            "filing_date",
        ],
        ascending=[True, False],
    )

    return float(subset.iloc[0]["value"])


def calculate_fundamental_metrics(
    *,
    ticker: str,
    facts: pd.DataFrame,
    fiscal_year: int,
) -> FundamentalMetrics:
    revenue = select_annual_fact(
        facts,
        logical_name="revenue",
        fiscal_year=fiscal_year,
    )

    previous_revenue = select_annual_fact(
        facts,
        logical_name="revenue",
        fiscal_year=fiscal_year - 1,
    )

    net_income = select_annual_fact(
        facts,
        logical_name="net_income",
        fiscal_year=fiscal_year,
    )

    previous_net_income = select_annual_fact(
        facts,
        logical_name="net_income",
        fiscal_year=fiscal_year - 1,
    )

    operating_income = select_annual_fact(
        facts,
        logical_name="operating_income",
        fiscal_year=fiscal_year,
    )

    assets = select_annual_fact(
        facts,
        logical_name="total_assets",
        fiscal_year=fiscal_year,
    )

    liabilities = select_annual_fact(
        facts,
        logical_name="total_liabilities",
        fiscal_year=fiscal_year,
    )

    equity = select_annual_fact(
        facts,
        logical_name="stockholders_equity",
        fiscal_year=fiscal_year,
    )

    cash = select_annual_fact(
        facts,
        logical_name="cash_and_equivalents",
        fiscal_year=fiscal_year,
    )

    operating_cash_flow = select_annual_fact(
        facts,
        logical_name="operating_cash_flow",
        fiscal_year=fiscal_year,
    )

    capex = select_annual_fact(
        facts,
        logical_name="capital_expenditures",
        fiscal_year=fiscal_year,
    )

    free_cash_flow = (
        operating_cash_flow - capex
        if operating_cash_flow is not None
        and capex is not None
        else None
    )

    return FundamentalMetrics(
        ticker=ticker,
        fiscal_year=fiscal_year,

        revenue=revenue,
        net_income=net_income,
        operating_income=operating_income,

        total_assets=assets,
        total_liabilities=liabilities,
        stockholders_equity=equity,

        cash_and_equivalents=cash,

        operating_cash_flow=operating_cash_flow,
        capital_expenditures=capex,
        free_cash_flow=free_cash_flow,

        revenue_growth=_growth(
            revenue,
            previous_revenue,
        ),

        net_income_growth=_growth(
            net_income,
            previous_net_income,
        ),

        operating_margin=_safe_divide(
            operating_income,
            revenue,
        ),

        net_margin=_safe_divide(
            net_income,
            revenue,
        ),

        return_on_assets=_safe_divide(
            net_income,
            assets,
        ),

        return_on_equity=_safe_divide(
            net_income,
            equity,
        ),

        liabilities_to_equity=_safe_divide(
            liabilities,
            equity,
        ),
    )