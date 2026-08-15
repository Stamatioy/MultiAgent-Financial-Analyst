from __future__ import annotations

import pandas as pd


REVENUE_CONCEPTS = {
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
}

NET_INCOME_CONCEPTS = {
    "NetIncomeLoss",
    "ProfitLoss",
}

OPERATING_CASH_FLOW_CONCEPTS = {
    "NetCashProvidedByUsedInOperatingActivities",
}

CAPEX_CONCEPTS = {
    "PaymentsToAcquirePropertyPlantAndEquipment",
}


def build_price_history(
    prices: pd.DataFrame,
) -> list[dict]:
    if prices.empty:
        return []

    frame = prices.copy()

    frame = frame.sort_values(
        "trading_date"
    )

    close = frame[
        "adjusted_close"
    ].astype(float)

    frame["ma_50"] = (
        close
        .rolling(
            window=50,
            min_periods=1,
        )
        .mean()
    )

    frame["ma_200"] = (
        close
        .rolling(
            window=200,
            min_periods=1,
        )
        .mean()
    )

    return [
        {
            "date": (
                row.trading_date
                .isoformat()
            ),
            "close": float(
                row.adjusted_close
            ),
            "ma_50": float(
                row.ma_50
            ),
            "ma_200": float(
                row.ma_200
            ),
        }
        for row in frame.itertuples()
    ]


def build_drawdown_history(
    prices: pd.DataFrame,
) -> list[dict]:
    if prices.empty:
        return []

    frame = prices.copy()

    frame = frame.sort_values(
        "trading_date"
    )

    close = frame[
        "adjusted_close"
    ].astype(float)

    running_peak = (
        close.cummax()
    )

    drawdown = (
        close / running_peak
        - 1.0
    )

    return [
        {
            "date": (
                date_value
                .isoformat()
            ),
            "drawdown": float(
                drawdown_value
            ),
        }
        for (
            date_value,
            drawdown_value,
        ) in zip(
            frame[
                "trading_date"
            ],
            drawdown,
            strict=True,
        )
    ]


def build_financial_history(
    facts: pd.DataFrame,
) -> list[dict]:
    if facts.empty:
        return []

    annual = facts[
        (
            facts[
                "fiscal_period"
            ]
            == "FY"
        )
        & (
            facts["form"]
            == "10-K"
        )
    ].copy()

    if annual.empty:
        return []

    years = sorted(
        int(year)
        for year in annual[
            "fiscal_year"
        ]
        .dropna()
        .unique()
    )

    history: list[
        dict
    ] = []

    for year in years:
        year_facts = annual[
            annual[
                "fiscal_year"
            ]
            == year
        ]

        revenue = _find_fact(
            year_facts,
            REVENUE_CONCEPTS,
        )

        net_income = _find_fact(
            year_facts,
            NET_INCOME_CONCEPTS,
        )

        operating_cash_flow = (
            _find_fact(
                year_facts,
                OPERATING_CASH_FLOW_CONCEPTS,
            )
        )

        capex = _find_fact(
            year_facts,
            CAPEX_CONCEPTS,
        )

        free_cash_flow = None

        if (
            operating_cash_flow
            is not None
            and capex is not None
        ):
            free_cash_flow = (
                operating_cash_flow
                - abs(capex)
            )

        if (
            revenue is None
            and net_income is None
            and free_cash_flow
            is None
        ):
            continue

        history.append(
            {
                "fiscal_year": year,
                "revenue": revenue,
                "net_income": (
                    net_income
                ),
                "free_cash_flow": (
                    free_cash_flow
                ),
            }
        )

    return history


def _find_fact(
    facts: pd.DataFrame,
    concepts: set[str],
) -> float | None:
    matches = facts[
        facts["concept"].isin(
            concepts
        )
    ]

    if matches.empty:
        return None

    matches = (
        matches.sort_values(
            [
                "filing_date",
                "period_end",
            ]
        )
    )

    value = matches.iloc[-1][
        "value"
    ]

    if pd.isna(value):
        return None

    return float(value)