from __future__ import annotations

from dataclasses import dataclass

from financial_analyst.sec.client import SECClient
from financial_analyst.validation.ticker import normalize_ticker


@dataclass(frozen=True)
class SECCompanyIdentity:
    ticker: str
    cik: int
    cik_padded: str
    company_name: str


class SECTickerNotFoundError(LookupError):
    pass


class SECTickerMapper:
    TICKER_FILE_PATH = (
        "https://www.sec.gov/files/company_tickers.json"
    )

    def __init__(
        self,
        client: SECClient,
    ) -> None:
        self.client = client

    def get_company(
        self,
        ticker: str,
    ) -> SECCompanyIdentity:
        normalized = normalize_ticker(ticker)

        # company_tickers.json is hosted on www.sec.gov rather
        # than data.sec.gov, so use a direct request here.
        response = self.client.client.get(
            self.TICKER_FILE_PATH
        )
        response.raise_for_status()

        payload = self.client.get_absolute_json(
            self.TICKER_FILE_PATH
        )

        for item in payload.values():
            item_ticker = str(item["ticker"]).upper()

            if item_ticker == normalized:
                cik = int(item["cik_str"])

                return SECCompanyIdentity(
                    ticker=normalized,
                    cik=cik,
                    cik_padded=f"{cik:010d}",
                    company_name=str(item["title"]),
                )

        raise SECTickerNotFoundError(
            f"Ticker {normalized} was not found in the SEC ticker map."
        )