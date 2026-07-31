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
        & (facts["form"] == "10-K")
        & (facts["unit"] == "USD")
        & (facts["fiscal_period"] == "FY")
    ].copy()

    if subset.empty:
        return None

    subset["period_end"] = pd.to_datetime(
        subset["period_end"],
        errors="coerce",
    )

    subset["period_start"] = pd.to_datetime(
        subset["period_start"],
        errors="coerce",
    )

    subset["filing_date"] = pd.to_datetime(
        subset["filing_date"],
        errors="coerce",
    )

    subset = subset.dropna(
        subset=[
            "period_end",
            "filing_date",
        ]
    )

    # Critical:
    # Select the fact whose ACTUAL reporting period ends
    # in the requested fiscal year.
    subset = subset[
        subset["period_end"].dt.year
        == fiscal_year
    ]

    if subset.empty:
        return None

    alias_priority = {
        concept: index
        for index, concept
        in enumerate(aliases)
    }

    subset["concept_priority"] = (
        subset["concept"]
        .map(alias_priority)
        .fillna(999)
    )

    # Duration concepts such as revenue / income / cash flow
    # should represent approximately one full fiscal year.
    duration_rows = subset[
        subset["period_start"].notna()
    ].copy()

    instant_rows = subset[
        subset["period_start"].isna()
    ].copy()

    if not duration_rows.empty:
        duration_rows["duration_days"] = (
            duration_rows["period_end"]
            - duration_rows["period_start"]
        ).dt.days

        annual_rows = duration_rows[
            duration_rows["duration_days"].between(
                300,
                380,
            )
        ]

        if not annual_rows.empty:
            subset = annual_rows
        else:
            subset = duration_rows

    elif not instant_rows.empty:
        subset = instant_rows

    # Prefer our best concept alias.
    # For restated/amended values, prefer the latest filing.
    subset = subset.sort_values(
        by=[
            "concept_priority",
            "filing_date",
        ],
        ascending=[
            True,
            False,
        ],
    )

    return float(
        subset.iloc[0]["value"]
    )


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

    if (
        liabilities is None
        and assets is not None
        and equity is not None
    ):
        liabilities = (
            assets - equity
        )

    previous_assets = select_annual_fact(
        facts,
        logical_name="total_assets",
        fiscal_year=fiscal_year - 1,
    )

    previous_equity = select_annual_fact(
        facts,
        logical_name="stockholders_equity",
        fiscal_year=fiscal_year - 1,
    )

    average_assets = (
        (assets + previous_assets) / 2
        if assets is not None
        and previous_assets is not None
        else assets
    )

    average_equity = (
        (equity + previous_equity) / 2
        if equity is not None
        and previous_equity is not None
        else equity
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
            average_assets,
        ),

        return_on_equity=_safe_divide(
            net_income,
            average_equity,
        ),

        liabilities_to_equity=_safe_divide(
            liabilities,
            equity,
        ),
    )