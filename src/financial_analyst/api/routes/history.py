from __future__ import annotations

import duckdb

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from financial_analyst.api.dependencies import (
    get_database,
)

from financial_analyst.api.models import (
    ResearchHistoryItem,
    ResearchHistoryReportResponse,
    ResearchHistoryResponse,
)

from financial_analyst.database.research_history_repository import (
    ResearchHistoryRepository,
)


router = APIRouter(
    prefix="/api/history",
    tags=[
        "research-history"
    ],
)


@router.get(
    "",
    response_model=(
        ResearchHistoryResponse
    ),
)
def get_history(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),

    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> ResearchHistoryResponse:
    repository = (
        ResearchHistoryRepository(
            connection
        )
    )

    items = (
        repository.list_history(
            limit=limit
        )
    )

    return ResearchHistoryResponse(
        items=[
            ResearchHistoryItem(
                **item
            )
            for item in items
        ]
    )


@router.get(
    "/{research_id}",
    response_model=(
        ResearchHistoryReportResponse
    ),
)
def get_history_report(
    research_id: str,

    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> ResearchHistoryReportResponse:
    repository = (
        ResearchHistoryRepository(
            connection
        )
    )

    try:
        report = (
            repository.get_report(
                research_id
            )
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                "Research report not found."
            ),
        ) from exc

    return (
        ResearchHistoryReportResponse(
            research_id=research_id,
            report=report,
        )
    )


@router.delete(
    "/{research_id}",
)
def delete_history_report(
    research_id: str,

    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> dict[
    str,
    bool,
]:
    repository = (
        ResearchHistoryRepository(
            connection
        )
    )

    deleted = repository.delete(
        research_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Research report not found."
            ),
        )

    return {
        "deleted": True
    }