import pytest

from financial_analyst.validation.ticker import (
    InvalidTickerError,
    normalize_ticker,
)


@pytest.mark.parametrize(
    ("input_ticker", "expected"),
    [
        ("amd", "AMD"),
        (" AAPL ", "AAPL"),
        ("brk-b", "BRK-B"),
        ("^gspc", "^GSPC"),
        ("eurusd=x", "EURUSD=X"),
    ],
)
def test_normalize_valid_ticker(
    input_ticker: str,
    expected: str,
) -> None:
    assert normalize_ticker(input_ticker) == expected


@pytest.mark.parametrize(
    "ticker",
    [
        "",
        "   ",
        "AMD; DROP TABLE prices_daily;",
        "../AMD",
        "AMD TEST",
        "THIS-TICKER-IS-FAR-TOO-LONG",
    ],
)
def test_reject_invalid_ticker(ticker: str) -> None:
    with pytest.raises(InvalidTickerError):
        normalize_ticker(ticker)