from __future__ import annotations

from financial_analyst.fundamentals.models import (
    FundamentalMetrics,
)
from financial_analyst.market_data.models import (
    MarketMetrics,
)
from financial_analyst.valuation.metrics import (
    calculate_valuation_metrics,
)
from financial_analyst.valuation.models import (
    ValuationMetrics,
)


class ValuationService:
    """Coordinates deterministic valuation calculations."""

    def analyze(
        self,
        *,
        market_metrics: MarketMetrics,
        fundamental_metrics: FundamentalMetrics,
    ) -> ValuationMetrics:
        return calculate_valuation_metrics(
            market=market_metrics,
            fundamentals=fundamental_metrics,
        )