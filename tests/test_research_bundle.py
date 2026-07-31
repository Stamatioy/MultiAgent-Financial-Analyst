import pytest
from pydantic import ValidationError

from financial_analyst.research.models import (
    ResearchParameters,
)


def test_valid_research_parameters() -> None:
    result = ResearchParameters(
        ticker="AMD",
        fiscal_year=2025,
        market_years=5,
        news_query="AI accelerator demand",
        news_limit=15,
    )

    assert result.ticker == "AMD"


def test_reject_invalid_market_years() -> None:
    with pytest.raises(
        ValidationError
    ):
        ResearchParameters(
            ticker="AMD",
            fiscal_year=2025,
            market_years=0,
            news_query="AI",
            news_limit=15,
        )


def test_reject_empty_news_query() -> None:
    with pytest.raises(
        ValidationError
    ):
        ResearchParameters(
            ticker="AMD",
            fiscal_year=2025,
            market_years=5,
            news_query="",
            news_limit=15,
        )