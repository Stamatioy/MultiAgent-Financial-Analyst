from __future__ import annotations

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
)
from financial_analyst.valuation.models import (
    ValuationMetrics,
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

    return float(
        numerator / denominator
    )


def _positive_denominator_ratio(
    numerator: float | None,
    denominator: float | None,
) -> float | None:
    """
    Return a ratio only when the denominator is positive.

    Negative earnings should not produce a conventional P/E ratio.
    """

    if (
        numerator is None
        or denominator is None
        or denominator <= 0
    ):
        return None

    return float(
        numerator / denominator
    )


def calculate_valuation_metrics(
    *,
    market: MarketMetrics,
    fundamentals: FundamentalMetrics,
) -> ValuationMetrics:
    if market.ticker != fundamentals.ticker:
        raise ValueError(
            "Market and fundamental ticker mismatch."
        )

    share_price = market.latest_close
    shares = fundamentals.shares_outstanding

    market_cap = (
        share_price * shares
        if shares is not None
        and shares > 0
        else None
    )

    debt = fundamentals.total_debt
    cash = fundamentals.cash_and_equivalents

    net_cash = (
        cash - debt
        if cash is not None
        and debt is not None
        else None
    )

    enterprise_value = None

    if market_cap is not None:
        if debt is not None and cash is not None:
            enterprise_value = (
                market_cap
                + debt
                - cash
            )

    trailing_pe = _positive_denominator_ratio(
        market_cap,
        fundamentals.net_income,
    )

    earnings_yield = _safe_divide(
        fundamentals.net_income,
        market_cap,
    )

    price_to_sales = _positive_denominator_ratio(
        market_cap,
        fundamentals.revenue,
    )

    price_to_book = _positive_denominator_ratio(
        market_cap,
        fundamentals.stockholders_equity,
    )

    ev_to_sales = _positive_denominator_ratio(
        enterprise_value,
        fundamentals.revenue,
    )

    ev_to_operating_income = (
        _positive_denominator_ratio(
            enterprise_value,
            fundamentals.operating_income,
        )
    )

    free_cash_flow_yield = _safe_divide(
        fundamentals.free_cash_flow,
        market_cap,
    )

    notes: list[str] = []

    if shares is None:
        notes.append(
            "Shares outstanding were unavailable; "
            "market-cap-based ratios could not be calculated."
        )

    if debt is None:
        notes.append(
            "Interest-bearing debt was unavailable; "
            "enterprise value was not calculated."
        )

    if cash is None:
        notes.append(
            "Cash was unavailable; enterprise value "
            "was not calculated."
        )

    if fundamentals.net_income is not None:
        if fundamentals.net_income <= 0:
            notes.append(
                "Net income was non-positive; "
                "trailing P/E is not meaningful."
            )

    if fundamentals.operating_income is not None:
        if fundamentals.operating_income <= 0:
            notes.append(
                "Operating income was non-positive; "
                "EV/operating income is not meaningful."
            )

    return ValuationMetrics(
        ticker=market.ticker,

        fiscal_year=fundamentals.fiscal_year,
        price_date=market.end_date,

        share_price=share_price,

        shares_outstanding=shares,

        market_cap=market_cap,
        enterprise_value=enterprise_value,

        trailing_pe=trailing_pe,
        earnings_yield=earnings_yield,

        price_to_sales=price_to_sales,
        price_to_book=price_to_book,

        ev_to_sales=ev_to_sales,

        ev_to_operating_income=(
            ev_to_operating_income
        ),

        free_cash_flow_yield=(
            free_cash_flow_yield
        ),

        net_cash=net_cash,

        debt_used=debt,
        cash_used=cash,

        shares_missing=shares is None,
        debt_missing=debt is None,
        cash_missing=cash is None,

        notes=notes,
    )