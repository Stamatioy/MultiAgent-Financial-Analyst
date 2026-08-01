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
                "period_start": "2025-01-01",
                "period_end": "2025-12-31",
                "value": 1000.0,
            },
            {
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-03-01",
                "period_start": "2025-01-01",
                "period_end": "2025-12-31",
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
        # Revenue
        {
            "concept": "Revenues",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "period_start": "2024-01-01",
            "period_end": "2024-12-31",
            "value": 1000.0,
        },
        {
            "concept": "Revenues",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": "2025-01-01",
            "period_end": "2025-12-31",
            "value": 1200.0,
        },

        # Net income
        {
            "concept": "NetIncomeLoss",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "period_start": "2024-01-01",
            "period_end": "2024-12-31",
            "value": 100.0,
        },
        {
            "concept": "NetIncomeLoss",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": "2025-01-01",
            "period_end": "2025-12-31",
            "value": 150.0,
        },

        # Operating income
        {
            "concept": "OperatingIncomeLoss",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": "2025-01-01",
            "period_end": "2025-12-31",
            "value": 240.0,
        },

        # Assets
        {
            "concept": "Assets",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "period_start": None,
            "period_end": "2024-12-31",
            "value": 2800.0,
        },
        {
            "concept": "Assets",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 3000.0,
        },

        # Liabilities
        {
            "concept": "Liabilities",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 1800.0,
        },

        # Equity
        {
            "concept": "StockholdersEquity",
            "fiscal_year": 2024,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2025-02-01",
            "period_start": None,
            "period_end": "2024-12-31",
            "value": 1000.0,
        },
        {
            "concept": "StockholdersEquity",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 1200.0,
        },

        # Operating cash flow
        {
            "concept": "NetCashProvidedByUsedInOperatingActivities",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": "2025-01-01",
            "period_end": "2025-12-31",
            "value": 300.0,
        },

        # Capital expenditures
        {
            "concept": "PaymentsToAcquirePropertyPlantAndEquipment",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": "2025-01-01",
            "period_end": "2025-12-31",
            "value": 80.0,
        },

        # Cash
        {
            "concept": "CashAndCashEquivalentsAtCarryingValue",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 500.0,
        },

        {
            "concept": "CommonStockSharesOutstanding",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "shares",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 10.0,
        },
        {
            "concept": "LongTermDebtCurrent",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 5.0,
        },
        {
            "concept": "LongTermDebtNoncurrent",
            "fiscal_year": 2025,
            "fiscal_period": "FY",
            "form": "10-K",
            "unit": "USD",
            "filing_date": "2026-02-01",
            "period_start": None,
            "period_end": "2025-12-31",
            "value": 15.0,
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

    assert result.shares_outstanding == 10.0
    assert result.current_debt == 5.0
    assert result.noncurrent_debt == 15.0
    assert result.total_debt == 20.0

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
        150.0 / 2900.0
    )

    assert result.return_on_equity == pytest.approx(
        150.0 / 1100.0
    )

    assert result.liabilities_to_equity == pytest.approx(
        1.5
    )
    

def test_selects_requested_period_not_old_comparative_value() -> None:
    frame = pd.DataFrame(
        [
            {
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-02-04",
                "period_start": "2025-01-01",
                "period_end": "2025-12-27",
                "value": 34_639.0,
            },
            {
                # Comparative 2024 value appearing in
                # the same later annual filing.
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-02-04",
                "period_start": "2024-01-01",
                "period_end": "2024-12-28",
                "value": 25_785.0,
            },
            {
                # Comparative 2023 value.
                "concept": "Revenues",
                "fiscal_year": 2025,
                "fiscal_period": "FY",
                "form": "10-K",
                "unit": "USD",
                "filing_date": "2026-02-04",
                "period_start": "2023-01-01",
                "period_end": "2023-12-30",
                "value": 22_680.0,
            },
        ]
    )

    result = select_annual_fact(
        frame,
        logical_name="revenue",
        fiscal_year=2025,
    )

    assert result == 34_639.0


def test_derives_liabilities_from_accounting_identity() -> None:
    frame = make_facts()

    frame = pd.concat(
        [
            frame,
            pd.DataFrame(
                [
                    {
                        "concept": "Assets",
                        "fiscal_year": 2025,
                        "fiscal_period": "FY",
                        "form": "10-K",
                        "unit": "USD",
                        "filing_date": "2026-02-01",
                        "period_start": None,
                        "period_end": "2025-12-31",
                        "value": 3000.0,
                    },
                    {
                        "concept": "StockholdersEquity",
                        "fiscal_year": 2025,
                        "fiscal_period": "FY",
                        "form": "10-K",
                        "unit": "USD",
                        "filing_date": "2026-02-01",
                        "period_start": None,
                        "period_end": "2025-12-31",
                        "value": 1200.0,
                    },
                ]
            ),
        ],
        ignore_index=True,
    )

    # Remove explicit Liabilities if make_facts contains it.
    frame = frame[
        frame["concept"] != "Liabilities"
    ]

    result = calculate_fundamental_metrics(
        ticker="TEST",
        facts=frame,
        fiscal_year=2025,
    )

    assert result.total_liabilities == pytest.approx(
        1800.0
    )

    assert result.liabilities_to_equity == pytest.approx(
        1.5
    )