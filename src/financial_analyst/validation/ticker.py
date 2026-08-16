from __future__ import annotations

import re


class InvalidTickerError(ValueError):
    """Raised when a ticker contains unsupported characters."""


_TICKER_PATTERN = re.compile(
    r"^[A-Z0-9^][A-Z0-9.\-^=]{0,14}$"
)


# Common aliases for market indices and instruments.
#
# Normal company tickers such as AMD, NVDA, MSFT,
# AAPL, AMZN, etc. do not need to be listed here.
# They pass through unchanged.
_TICKER_ALIASES: dict[str, str] = {
    # S&P 500
    "SPX500": "^GSPC",
    "SP500": "^GSPC",
    "S&P500": "^GSPC",
    "S&P 500": "^GSPC",

    # Nasdaq Composite
    "NASDAQ": "^IXIC",
    "NASDAQCOMPOSITE": "^IXIC",
    "NASDAQ COMPOSITE": "^IXIC",

    # Nasdaq 100
    "NASDAQ100": "^NDX",
    "NASDAQ 100": "^NDX",
    "NDX100": "^NDX",

    # Dow Jones Industrial Average
    "DJIA": "^DJI",
    "DOW": "^DJI",
    "DOWJONES": "^DJI",
    "DOW JONES": "^DJI",

    # Russell 2000
    "RUSSELL2000": "^RUT",
    "RUSSELL 2000": "^RUT",
    "RUT2000": "^RUT",

    # Volatility Index
    "VIX": "^VIX",

    # Common ETF descriptions
    "S&P500ETF": "SPY",
    "SP500ETF": "SPY",
    "NASDAQ100ETF": "QQQ",
    "DOWETF": "DIA",
    "RUSSELL2000ETF": "IWM",
}
INDEX_TICKERS = {
    "^GSPC",
    "^IXIC",
    "^NDX",
    "^DJI",
    "^RUT",
    "^VIX",
}




def normalize_ticker(
    ticker: str,
) -> str:
    """
    Normalize and validate a market ticker.

    Normal ticker examples:
        amd -> AMD
        nvda -> NVDA
        brk-b -> BRK-B
        ^gspc -> ^GSPC
        eurusd=x -> EURUSD=X

    Alias examples:
        spx500 -> ^GSPC
        sp500 -> ^GSPC
        nasdaq -> ^IXIC
        nasdaq100 -> ^NDX
        dow -> ^DJI
        russell2000 -> ^RUT
        vix -> ^VIX
    """

    normalized = (
        ticker
        .strip()
        .upper()
    )

    if not normalized:
        raise InvalidTickerError(
            "Ticker cannot be empty."
        )

    # First try the alias exactly as entered.
    alias = _TICKER_ALIASES.get(
        normalized
    )

    if alias is not None:
        normalized = alias

    else:
        # Also try a version without spaces.
        #
        # Example:
        # "NASDAQ 100" -> "NASDAQ100"
        compact = normalized.replace(
            " ",
            ""
        )

        alias = _TICKER_ALIASES.get(
            compact
        )

        if alias is not None:
            normalized = alias

    if not _TICKER_PATTERN.fullmatch(
        normalized
    ):
        raise InvalidTickerError(
            "Ticker contains unsupported "
            "characters or is too long."
        )

    return normalized

def validate_company_ticker(
    ticker: str,
) -> str:
    normalized = normalize_ticker(
        ticker
    )

    if normalized in INDEX_TICKERS:
        raise InvalidTickerError(
            f"{normalized} is a market index. "
            "Company research requires an equity ticker."
        )

    return normalized