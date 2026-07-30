from __future__ import annotations

import re


class InvalidTickerError(ValueError):
    """Raised when a ticker contains unsupported characters."""


_TICKER_PATTERN = re.compile(r"^[A-Z0-9^][A-Z0-9.\-^=]{0,14}$")


def normalize_ticker(ticker: str) -> str:
    """
    Normalize and validate a market ticker.

    Examples:
        amd -> AMD
        brk-b -> BRK-B
        ^gspc -> ^GSPC
        eurusd=x -> EURUSD=X
    """

    normalized = ticker.strip().upper()

    if not normalized:
        raise InvalidTickerError("Ticker cannot be empty.")

    if not _TICKER_PATTERN.fullmatch(normalized):
        raise InvalidTickerError(
            "Ticker contains unsupported characters or is too long."
        )

    return normalized