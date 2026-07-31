import pandas as pd
import pytest

from financial_analyst.fundamentals.metrics import (
    select_annual_fact,
)


def test_later_filing_wins() -> None:
    frame = pd.DataFrame(
        [
            {
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-02-01",
                "value": 1000.0,
            },
            {
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-03-01",
                "value": 1100.0,
            },
        ]
    )

    result = select_annual_fact(
        frame,
        logical_name="revenue",
        fiscal_year=2025,
    )

    assert result == 1100.0

from financial_analyst.fundamentals.metrics import (
    calculate_fundamental_metrics,
)


def make_facts() -> pd.DataFrame:
    rows = [
        {
            "concept": "Revenues",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "value": 1000.0,
        },
        {
            "concept": "Revenues",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 1200.0,
        },
        {
            "concept": "NetIncomeLoss",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "value": 100.0,
        },
        {
            "concept": "NetIncomeLoss",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 150.0,
        },
        {
            "concept": "OperatingIncomeLoss",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 240.0,
        },
        {
            "concept": "Assets",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 3000.0,
        },
        {
            "concept": "Liabilities",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 1800.0,
        },
        {
            "concept": "StockholdersEquity",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 1200.0,
        },
        {
            "concept": "NetCashProvidedByUsedInOperatingActivities",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 300.0,
        },
        {
            "concept": "PaymentsToAcquirePropertyPlantAndEquipment",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "value": 80.0,
        },
    ]

    return pd.DataFrame(rows)


def test_fundamental_calculations() -> None:
    result = calculate_fundamental_metrics(
        ticker="TEST",
        facts=make_facts(),
        fiscal_year=2025,
    )

    assert result.revenue == 1200.0

    assert result.revenue_growth == pytest.approx(
        0.20
    )

    assert result.net_income_growth == pytest.approx(
        0.50
    )

    assert result.operating_margin == pytest.approx(
        0.20
    )

    assert result.net_margin == pytest.approx(
        0.125
    )

    assert result.free_cash_flow == 220.0

    assert result.return_on_assets == pytest.approx(
        0.05
    )

    assert result.return_on_equity == pytest.approx(
        0.125
    )

    assert result.liabilities_to_equity == pytest.approx(
        1.5
    )