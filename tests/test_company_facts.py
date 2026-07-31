from financial_analyst.sec.company_facts import (
    SECCompanyFactsParser,
)


def test_parse_company_fact() -> None:
    payload = {
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "units": {
                        "USD": [
                            {
                                "start": "2025-01-01",
                                "end": "2025-12-31",
                                "val": 1000000,
                                "accn": "0000000000-26-000001",
                                "fy": 2025,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2026-02-01",
                            }
                        ]
                    }
                }
            }
        }
    }

    facts = SECCompanyFactsParser.parse(
        payload=payload,
        ticker="TEST",
        cik=123456,
    )

    assert len(facts) == 1

    fact = facts[0]

    assert fact.concept == "Revenues"
    assert fact.value == 1_000_000
    assert fact.fiscal_year == 2025
    assert fact.form == "10-K"