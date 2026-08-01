from __future__ import annotations


CONCEPT_ALIASES: dict[str, list[str]] = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
        "Revenues",
    ],

    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
    ],

    "operating_income": [
        "OperatingIncomeLoss",
    ],

    "total_assets": [
        "Assets",
    ],

    "total_liabilities": [
        "Liabilities",
    ],

    "stockholders_equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],

    "cash_and_equivalents": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],

    "operating_cash_flow": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],

    "capital_expenditures": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
    ],
    "shares_outstanding": [
    "CommonStockSharesOutstanding",
    ],
    "long_term_debt": [
        "LongTermDebtAndFinanceLeaseObligationsCurrent",
        "LongTermDebtCurrent",
        "ShortTermBorrowings",
    ],

    "long_term_debt_noncurrent": [
        "LongTermDebtAndFinanceLeaseObligationsNoncurrent",
        "LongTermDebtNoncurrent",
        "LongTermDebtAndCapitalLeaseObligations",
    ],
}