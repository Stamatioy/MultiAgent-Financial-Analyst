from financial_analyst.valuation.service import (
    ValuationService,
)

from tests.test_valuation_metrics import (
    make_fundamentals,
    make_market_metrics,
)


def test_valuation_service_returns_metrics() -> None:
    service = ValuationService()

    result = service.analyze(
        market_metrics=make_market_metrics(),
        fundamental_metrics=make_fundamentals(),
    )

    assert result.ticker == "TEST"
    assert result.market_cap == 1000.0