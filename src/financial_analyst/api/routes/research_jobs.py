from __future__ import annotations

from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
)

from financial_analyst.api.jobs import (
    research_job_store,
)
from financial_analyst.api.models import (
    ResearchJobCreated,
    ResearchJobResultResponse,
    ResearchJobStatus,
    ResearchJobStatusResponse,
    ResearchRequest,
    ResearchStepStatus,
)
from financial_analyst.committee.factory import (
    build_investment_pipeline,
)
from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.sec.client import (
    SECClient,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)
from typing import Any

from financial_analyst.database.research_history_repository import (
    ResearchHistoryRepository,
)

router = APIRouter(
    prefix="/api/research/jobs",
    tags=["research-jobs"],
)


def run_research_job(
    *,
    job_id: str,
    request: ResearchRequest,
) -> None:
    """
    Run one complete research operation outside
    the original HTTP request lifecycle.

    This function owns its DB connection and SEC client.
    """

    research_job_store.start(
        job_id
    )

    connection = (
        get_database_connection()
    )

    try:
        def progress_callback(
            step: str,
            status: str,
            result: Any | None = None,
        ) -> None:
            research_job_store.update_step(
                job_id=job_id,

                step_name=step,

                status=(
                    ResearchStepStatus(
                        status
                    )
                ),

                result=result,
            )

        with SECClient() as sec_client:
            pipeline = (
                build_investment_pipeline(
                    connection=connection,
                    sec_client=sec_client,
                )
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

                as_of=(
                    request.as_of
                ),

                refresh_market=(
                    request.refresh_market
                ),

                refresh_fundamentals=(
                    request.refresh_fundamentals
                ),

                progress_callback=(
                    progress_callback
                ),
            )

        history_repository = (
            ResearchHistoryRepository(
                connection
            )
        )

        history_repository.save(
            report
        )

        research_job_store.complete(
            job_id=job_id,
            report=report,
        )

    except Exception as exc:
        research_job_store.fail(
            job_id=job_id,
            error=str(exc),
        )

    finally:
        connection.close()


@router.post(
    "",
    response_model=ResearchJobCreated,
    status_code=202,
)
def create_research_job(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
) -> ResearchJobCreated:
    ticker = normalize_ticker(
        request.ticker
    )

    request = request.model_copy(
        update={
            "ticker": ticker
        }
    )

    job_id = (
        research_job_store.create(
            ticker=ticker
        )
    )

    background_tasks.add_task(
        run_research_job,
        job_id=job_id,
        request=request,
    )

    return ResearchJobCreated(
        job_id=job_id,

        status=(
            ResearchJobStatus.QUEUED
        ),
    )


@router.get(
    "/{job_id}",
    response_model=(
        ResearchJobStatusResponse
    ),
)
def get_research_job(
    job_id: str,
) -> ResearchJobStatusResponse:
    try:
        return (
            research_job_store.status(
                job_id
            )
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Research job not found.",
        ) from exc


@router.get(
    "/{job_id}/result",
    response_model=(
        ResearchJobResultResponse
    ),
)
def get_research_result(
    job_id: str,
) -> ResearchJobResultResponse:
    try:
        status = (
            research_job_store.status(
                job_id
            )
        )

        if (
            status.status
            == ResearchJobStatus.FAILED
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    status.error
                    or "Research failed."
                ),
            )

        if (
            status.status
            != ResearchJobStatus.COMPLETED
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    "Research report is not ready."
                ),
            )

        report = (
            research_job_store.result(
                job_id
            )
        )

        return ResearchJobResultResponse(
            job_id=job_id,
            report=report,
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Research job not found.",
        ) from exc