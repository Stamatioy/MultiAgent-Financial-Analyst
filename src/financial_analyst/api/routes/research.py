from __future__ import annotations

import duckdb
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from financial_analyst.api.dependencies import (
    get_database,
)
from financial_analyst.api.models import (
    ResearchRequest,
    ResearchResponse,
)
from financial_analyst.committee.factory import (
    build_investment_pipeline,
)
from financial_analyst.sec.client import (
    SECClient,
)


router = APIRouter(
    prefix="/api/research",
    tags=["research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
)
def research_company(
    request: ResearchRequest,

    connection: duckdb.DuckDBPyConnection = Depends(
        get_database
    ),
) -> ResearchResponse:
    try:
        with SECClient() as sec_client:
            pipeline = build_investment_pipeline(
                connection=connection,
                sec_client=sec_client,
            )

            report = pipeline.analyze(
                ticker=request.ticker,

                fiscal_year=(
                    request.fiscal_year
                ),

                market_years=(
                    request.market_years
                ),

                benchmark_ticker=(
                    request.benchmark_ticker
                ),

                risk_free_rate_annual=(
                    request.risk_free_rate_annual
                ),

                news_query=(
                    request.news_query
                ),

                news_limit=(
                    request.news_limit
                ),

                as_of=request.as_of,

                refresh_market=(
                    request.refresh_market
                ),

                refresh_fundamentals=(
                    request.refresh_fundamentals
                ),
            )

        return ResearchResponse(
            report=report
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Company research failed: "
                f"{exc}"
            ),
        ) from exc