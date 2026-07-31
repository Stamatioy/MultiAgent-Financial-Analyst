from __future__ import annotations

from datetime import date
from typing import Any

from financial_analyst.fundamentals.models import FinancialFact
from financial_analyst.sec.client import SECClient


class SECCompanyFactsParser:
    """Fetch and normalize standardized US-GAAP company facts."""

    def __init__(
        self,
        client: SECClient,
    ) -> None:
        self.client = client

    def fetch(
        self,
        *,
        ticker: str,
        cik: int,
    ) -> list[FinancialFact]:
        cik_padded = f"{cik:010d}"

        payload = self.client.get_json(
            f"/api/xbrl/companyfacts/CIK{cik_padded}.json"
        )

        return self.parse(
            payload=payload,
            ticker=ticker,
            cik=cik,
        )

    @staticmethod
    def parse(
        *,
        payload: dict[str, Any],
        ticker: str,
        cik: int,
    ) -> list[FinancialFact]:
        facts_root = payload.get("facts", {})
        us_gaap = facts_root.get("us-gaap", {})

        output: list[FinancialFact] = []

        for concept_name, concept_data in us_gaap.items():
            units = concept_data.get("units", {})

            for unit_name, observations in units.items():
                for observation in observations:
                    value = observation.get("val")
                    end = observation.get("end")
                    filed = observation.get("filed")
                    form = observation.get("form")
                    accession = observation.get("accn")

                    if (
                        value is None
                        or end is None
                        or filed is None
                        or form is None
                        or accession is None
                    ):
                        continue

                    # v1: use 10-K/10-Q only.
                    if form not in {"10-K", "10-Q"}:
                        continue

                    try:
                        numeric_value = float(value)
                    except (TypeError, ValueError):
                        continue

                    start = observation.get("start")

                    output.append(
                        FinancialFact(
                            ticker=ticker,
                            cik=cik,
                            concept=concept_name,
                            unit=unit_name,
                            fiscal_year=observation.get("fy"),
                            fiscal_period=observation.get("fp"),
                            form=form,
                            filing_date=date.fromisoformat(filed),
                            period_start=(
                                date.fromisoformat(start)
                                if start
                                else None
                            ),
                            period_end=date.fromisoformat(end),
                            accession_number=accession,
                            value=numeric_value,
                        )
                    )

        return output